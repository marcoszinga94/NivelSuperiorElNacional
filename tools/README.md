# Jugar online: cómo se recuperaron los juegos

Los juegos se entregaron solo como `.exe` (Python + Pygame empaquetados con
PyInstaller), así que no había código fuente. Para que se puedan jugar en el
navegador sin instalar nada se hace esto:

1. **Desempacar** el `.exe` con [pyinstxtractor-ng](https://github.com/pyinstxtractor/pyinstxtractor-ng).
   Adentro quedan el script compilado (`main.pyc`), los módulos propios del
   juego y los assets.
2. **Armar un zip** con ese bytecode original (o con el código recuperado,
   cuando el bytecode no puede correr) más los assets.
3. **Ejecutarlo en el navegador** con [Pyodide](https://pyodide.org): CPython
   compilado a WebAssembly, más el wheel de `pygame-ce` que corresponde a esa
   versión de Python. Eso lo hace `public/jugar/player.js`.

No hay paso de compilación para el sitio: cada juego es una carpeta estática
(`public/jugar/<slug>/juego/`) con un `index.html` y un `game.zip`, y la página
`/jugar/<slug>` la embebe en un iframe.

## Íconos de los ejecutables

Las tarjetas de `/juegos` no usan capturas: muestran el ícono que cada `.exe`
trae embebido en sus recursos de Windows, tal como lo dibuja el Explorador. Los
PNG salen del propio ejecutable:

```bash
# deja public/juegos/icono/<slug>.png (252x252) por cada .exe que traiga ícono
python3 tools/extract-exe-icons.py --png
```

El script lee la tabla de recursos del PE (`RT_GROUP_ICON` + `RT_ICON`) con la
biblioteca estándar, se queda con el frame más grande, le recorta el halo
sobrante y lo centra en un lienzo cuadrado. La ruta de cada PNG vive en el campo
`logo` de `src/data/games.ts`.

Dos casos reales de la muestra, que la página refleja tal cual:

- **ArcSpace**: el `.exe` trae el ícono genérico de PyInstaller, no un logo
  propio. La tarjeta usa `public/juegos/arcspace-logo.png`: un badge circular
  armado con el fondo del menú (`Fondo-Menu.png`) y el título dibujado con la
  Silkscreen que viene en `assets/Fonts/Silkscreen/`, los dos sacados del propio
  ejecutable.
- **Solar Defender**: el recurso de ícono está vacío (0 bytes), así que no hay
  nada que extraer de la tabla de recursos. El logo de la tarjeta sale del arte
  que el juego trae adentro (`assets/splash.png`, 1024x1024): se recorta en
  círculo y se le saca el fondo blanco.

## ¿Por qué hace falta un ajuste en el bucle del juego?

Un bucle de Pygame es bloqueante: si corriera tal cual, el hilo principal del
navegador nunca se libera y la pestaña se congela (sin dibujar y sin recibir
teclado). `player.js` envuelve `pygame.display.update` / `flip`, la espera de
`Clock.tick` y `time.sleep` para ceder el control una vez por frame usando
`run_sync` + asyncify. Con eso el juego corre a su ritmo y la página sigue viva.

## Audio en el celular

Los callbacks de Web Audio corren en el mismo hilo que el juego, así que un
frame lento se escucha como **estática**. `player.js` lo mitiga de tres formas:

1. Abre el mixer a la **frecuencia del dispositivo** (`AudioContext.sampleRate`,
   casi siempre 48000) en vez de los 44100 que piden algunos juegos, así SDL no
   tiene que remuestrear.
2. Pide un **buffer grande** (4096 muestras) para tener margen.
3. Deja **respirar el bucle a mitad de frame** (`js_breathe`): si `pygame.draw.*`
   lleva más de 16 ms dibujando, cede el control para que el audio se rellene.

## Versión de Pyodide según el bytecode

El bytecode solo carga en la misma versión de CPython, así que cada juego usa
la build de Pyodide que coincide con su Python:

| Python | Pyodide  | Juegos                                        |
| ------ | -------- | --------------------------------------------- |
| 3.12   | `0.26.4` | Preguntados Kids                              |
| 3.13   | `0.29.5` | ArcSpace, El Cielo Cordobés                    |
| 3.14   | `314.0.7`| Stellar Scrap                                  |

Pyodide no tiene `pygame-ce` para 3.10 ni 3.11, así que los juegos de esas
versiones se corren desde el código recuperado con
[PyLingual](https://github.com/syssec-utd/pylingual) y se guardan en
`tools/recovered/<slug>/main.py`.

## Cómo reconstruir un juego

```bash
# 1. desempacar el .exe (una vez por juego)
python3 pyinstxtractor-ng.py "public/Ejecutadores/ARCSPACE.exe"
# queda en ARCSPACE.exe_extracted/

# 2. apuntar GAME_EXTRACT_ROOT a esa carpeta (por defecto /tmp/opencode/extract)
GAME_EXTRACT_ROOT=/ruta/a/los/extraidos python3 tools/build-web-games.py arcspace
```

Sin argumentos reconstruye todos. El estado de cada juego está en la tabla de abajo.

## Estado

Los 8 juegos se juegan en el navegador:

| Juego              | Como corre                                                   |
| ------------------ | ------------------------------------------------------------ |
| ArcSpace           | bytecode original (3.13)                                      |
| Boom Cósmico       | codigo recuperado (3.10 no tiene pygame en WASM)              |
| El Cielo Cordobés  | bytecode original (3.13)                                      |
| Preguntados Kids   | bytecode original (3.12)                                      |
| Solar Defender     | codigo recuperado y reparado                                  |
| Stellar Scrap      | bytecode original (3.14)                                      |
| Cartas Espaciales  | puerto a Pygame (el original es una app Tkinter)              |
| ¡Viaje Galáctico!  | puerto a Pygame (el original es Tkinter + API de Gemini)      |

Los dos últimos no eran juegos de Pygame: eran aplicaciones de escritorio con
interfaz Tkinter, y Tkinter no existe en el navegador. Sus puertos viven en
`tools/recovered/<slug>/main.py`, conservan los assets y las reglas del
original, y cambian solo el motor de dibujo:

- **Cartas Espaciales**: mismo mazo (3 aliens + 1 comodin + 7 pares), mismos
  puntajes (+10 par, -1 intento, -3 alien), mismo ranking.
- **¡Viaje Galáctico!**: mismo contenido (`cuerpos_celestes.json`), las 5
  preguntas del cuestionario y las medallas. La narracion que el original le
  pedia a Gemini ahora la hace `speechSynthesis` del navegador.

## Reparaciones manuales

Los decompiladores no son perfectos, asi que algunos archivos recuperados
llevan arreglos a mano:

- **Boom Cósmico**: `Sonido.cargar_sonidos` (el decompilador perdio el bucle) y
  la fuente de emojis `C:\Windows\Fonts\seguiemj.ttf`, que solo existe en Windows.
- **Solar Defender**: `repair.py` reindenta los bloques que el decompilador
  anido de mas (`Game.run`, `Game.check_collisions`) y reescribe los dos
  parsers de guardado (`GameData.load`, `PlayerDB.load`).


