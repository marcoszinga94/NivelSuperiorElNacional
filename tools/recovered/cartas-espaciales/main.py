"""
Choque de Planetas / Memoria Estelar - version web (Pygame).

Puerto del juego original de Ezequiel Strombe, que era una aplicacion de
escritorio con interfaz Tkinter (ventana + botones) y por eso no podia correr
en un navegador. Se conservan las reglas, el mazo, los puntajes y los assets
del ejecutable; lo unico que cambia es el motor de dibujo, que pasa a Pygame.

Reglas (recuperadas del original):

* Mazo de 18 cartas: 3 aliens + 1 comodin (joker) + 7 pares de cartas.
* Tablero de 6 columnas por 3 filas.
* Cada par encontrado suma 10, cada intento resta 1 y cada alien resta 3.
* El comodin espanta a los aliens que ya aparecieron: los vuelve a tapar.
* Si aparecen los 3 aliens, se pierde. Si se descubren todas las cartas que
  no son aliens (los 7 pares y el comodin), se gana.
"""

import os
import random
import sys
import csv

import pygame

ANCHO, ALTO = 1280, 720
COLUMNAS = 6
PARES = 7
FPS = 60

AZUL_FONDO = (0, 31, 63)
CYAN = (0, 255, 255)
ORO = (255, 215, 0)
ROJO = (255, 40, 40)
BLANCO = (240, 248, 255)
AZUL_BOTON = (0, 116, 217)
VERDE = (46, 204, 64)

BASE = os.path.dirname(os.path.abspath(sys.argv[0]))
IMG = os.path.join(BASE, "imagenes")
SON = os.path.join(BASE, "sonidos")
DATOS = os.path.join(BASE, "datos")
RANKING = os.path.join(DATOS, "jugadores.csv")


def ruta_media(nombre, carpeta=IMG):
    for ext in (".png", ".jpg", ".jpeg", ".gif"):
        ruta = os.path.join(carpeta, f"{nombre}{ext}")
        if os.path.exists(ruta):
            return ruta
    return None


def cargar_imagen(ruta, tamano=None):
    if not ruta or not os.path.exists(ruta):
        return None
    imagen = pygame.image.load(ruta).convert_alpha()
    if tamano:
        imagen = pygame.transform.smoothscale(imagen, tamano)
    return imagen


def escalar_a_pantalla(imagen):
    """Encaja una imagen dentro de la ventana manteniendo la proporcion."""
    if not imagen:
        return None
    ancho, alto = imagen.get_size()
    factor = min(ANCHO / ancho, ALTO / alto)
    return pygame.transform.smoothscale(imagen, (int(ancho * factor), int(alto * factor)))


def cargar_ranking():
    jugadores = []
    if os.path.exists(RANKING):
        try:
            with open(RANKING, "r", encoding="utf-8", newline="") as f:
                for fila in csv.DictReader(f, delimiter=";"):
                    fila["puntaje"] = int(fila.get("puntaje", 0))
                    fila["intentos"] = int(fila.get("intentos", 0))
                    fila["partidas"] = int(fila.get("partidas", 0))
                    jugadores.append(fila)
        except Exception:
            return []
    return jugadores


def guardar_puntaje(nombre, puntaje, intentos):
    if not nombre:
        return
    jugadores = cargar_ranking()
    encontrado = False
    for j in jugadores:
        if j["nombre"].lower() == nombre.lower():
            if puntaje > j["puntaje"]:
                j["puntaje"] = puntaje
                j["intentos"] = intentos
            j["partidas"] = int(j.get("partidas", 0)) + 1
            encontrado = True
            break
    if not encontrado:
        jugadores.append({"nombre": nombre, "puntaje": puntaje, "intentos": intentos, "partidas": 1})
    jugadores.sort(key=lambda x: x["puntaje"], reverse=True)
    try:
        os.makedirs(DATOS, exist_ok=True)
        with open(RANKING, "w", encoding="utf-8", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=["nombre", "puntaje", "intentos", "partidas"], delimiter=";")
            writer.writeheader()
            writer.writerows(jugadores)
    except Exception as e:
        print("No se pudo guardar el ranking:", e)


class Juego:
    def __init__(self):
        pygame.init()
        self.pantalla = pygame.display.set_mode((ANCHO, ALTO))
        pygame.display.set_caption("Choque de Planetas - Memoria Estelar")
        self.reloj = pygame.time.Clock()
        self.fuente = lambda tamano, negrita=False: pygame.font.Font(None, tamano)
        self.musica = {}
        self._cargar_sonidos()
        self._cargar_graficos()
        self.estado = "menu"
        self.nombre = ""
        self.puntaje = 0
        self.intentos = 0
        self.mensaje_fin = ""
        self.parpadeo = 0

    # ---------------------------------------------------------------- recursos
    def _cargar_sonidos(self):
        try:
            pygame.mixer.init()
        except Exception as e:
            print("Sin audio:", e)
            return
        for clave, nombre in (
            ("juego", "Kepler_s_Gate.mp3"),
            ("menu", "Gravity_Gardens.mp3"),
            ("instrucciones", "instrucciones.mp3"),
            ("alerta", "LYNC_howler.wav"),
            ("records", "LYNC_ringtone3.wav"),
        ):
            ruta = os.path.join(SON, nombre)
            if os.path.exists(ruta):
                self.musica[clave] = ruta

    def poner_musica(self, clave):
        ruta = self.musica.get(clave)
        if ruta:
            try:
                pygame.mixer.music.load(ruta)
                pygame.mixer.music.set_volume(0.5)
                pygame.mixer.music.play(-1)
            except Exception:
                pass

    def _cargar_graficos(self):
        self.g_menu = escalar_a_pantalla(cargar_imagen(ruta_media("fondo")))
        self.g_instrucciones = escalar_a_pantalla(cargar_imagen(ruta_media("instrucciones")))
        self.g_ganador = escalar_a_pantalla(cargar_imagen(ruta_media("ganador")))
        self.g_perdiste = escalar_a_pantalla(cargar_imagen(ruta_media("perdiste")))
        self.g_records = escalar_a_pantalla(cargar_imagen(ruta_media("records")))
        self.icono_salir = cargar_imagen(ruta_media("salir"), (50, 50))
        self.icono_reiniciar = cargar_imagen(ruta_media("restart"), (60, 60))
        self.icono_menu = cargar_imagen(ruta_media("menu"), (60, 60))
        self.icono_records = cargar_imagen(ruta_media("records"), (60, 60))

        # El mazo: 3 aliens, 1 comodin y 7 pares de cartas distintas.
        carpeta = os.path.join(IMG, "cartas")
        archivos = sorted(
            os.path.join(carpeta, a)
            for a in os.listdir(carpeta)
            if a.lower().endswith((".png", ".jpg", ".jpeg"))
        )
        comodin = next((a for a in archivos if "joker" in os.path.basename(a).lower()), None)
        alien = next((a for a in archivos if "carta_alien" in os.path.basename(a).lower()), None)
        otras = [a for a in archivos if a not in (comodin, alien)]
        self.alien_ruta, self.comodin_ruta = alien, comodin
        self.cartas_distintas = {a: cargar_imagen(a) for a in otras}
        self.dorso = cargar_imagen(ruta_media("dorso_nuevo_1"))

        self.tamano_carta = 150
        self.escaladas = {}

    # ------------------------------------------------------------ utilidades
    def texto(self, mensaje, tamano, color, centro=None, topleft=None, negrita=False):
        superficie = self.fuente(tamano, negrita).render(mensaje, True, color)
        rect = superficie.get_rect()
        if centro:
            rect.center = centro
        if topleft:
            rect.topleft = topleft
        self.pantalla.blit(superficie, rect)
        return rect

    def boton(self, rect, etiqueta, color=AZUL_BOTON):
        pygame.draw.rect(self.pantalla, color, rect, border_radius=12)
        pygame.draw.rect(self.pantalla, CYAN, rect, 3, border_radius=12)
        self.texto(etiqueta, 34, BLANCO, centro=rect.center)

    # ------------------------------------------------------------------ juego
    def nuevo_mazo(self):
        eleccion = random.sample(list(self.cartas_distintas.keys()), PARES)
        mazo = [self.alien_ruta] * 3 + [self.comodin_ruta]
        for carta in eleccion:
            mazo.extend([carta, carta])
        random.shuffle(mazo)
        self.mazo = mazo
        self.total = len(mazo)
        self.filas = (self.total + COLUMNAS - 1) // COLUMNAS
        self.descubiertas = [False] * self.total
        self.seleccionados = []
        self.aliens = set()
        self.intentos = 0
        self.puntaje = 0
        self.pares = 0
        self.bloqueo = 0
        self.parpadeo = 0
        self._calcular_tablero()

    def _calcular_tablero(self):
        margen_sup = 110
        margen_inf = 120
        disponible_alto = ALTO - margen_sup - margen_inf
        disponible_ancho = ANCHO - 80
        bloque = min(
            (disponible_ancho - (COLUMNAS - 1) * 10) // COLUMNAS,
            (disponible_alto - (self.filas - 1) * 10) // self.filas,
        )
        self.tamano_carta = max(60, bloque)
        self.tablero_ancho = COLUMNAS * self.tamano_carta + (COLUMNAS - 1) * 10
        self.tablero_alto = self.filas * self.tamano_carta + (self.filas - 1) * 10
        self.tablero_x = (ANCHO - self.tablero_ancho) // 2
        self.tablero_y = margen_sup + max(0, (disponible_alto - self.tablero_alto) // 2)
        self.escaladas = {}
        for clave, imagen in self.cartas_distintas.items():
            if imagen:
                self.escaladas[clave] = pygame.transform.smoothscale(imagen, (self.tamano_carta, self.tamano_carta))

    def rect_carta(self, indice):
        fila, columna = divmod(indice, COLUMNAS)
        x = self.tablero_x + columna * (self.tamano_carta + 10)
        y = self.tablero_y + fila * (self.tamano_carta + 10)
        return pygame.Rect(x, y, self.tamano_carta, self.tamano_carta)

    def mostrar_carta(self, indice):
        """Voltea una carta. Misma logica que el original."""
        if self.descubiertas[indice] or indice in self.seleccionados or len(self.seleccionados) == 2:
            return
        carta = self.mazo[indice]
        es_alien = carta == self.alien_ruta
        es_comodin = carta == self.comodin_ruta
        if es_alien:
            self.parpadeo = 6
            if "alerta" in self.musica:
                try:
                    pygame.mixer.Sound(self.musica["alerta"]).play()
                except Exception:
                    pass
        self.seleccionados.append(indice)
        if es_comodin:
            # El comodin tapa de nuevo a los aliens que ya habian salido.
            self.descubiertas[indice] = True
            self.aliens.clear()
            if len(self.seleccionados) == 2:
                primero = self.seleccionados[0]
                if self.mazo[primero] not in (self.alien_ruta, self.comodin_ruta):
                    self.seleccionados.remove(primero)
                    self.descubiertas[primero] = False
            self.seleccionados.clear()
            if self.verificar_victoria():
                self.terminar(True)
            return
        if es_alien:
            self.aliens.add(indice)
            self.puntaje -= 3
            if len(self.aliens) >= 3:
                self.bloqueo = 24
        if len(self.seleccionados) == 2:
            self.bloqueo = 42  # ~700 ms a 60 fps

    def comprobar_par(self):
        primero, segundo = self.seleccionados
        self.intentos += 1
        self.puntaje -= 1
        if self.mazo[primero] == self.mazo[segundo]:
            self.descubiertas[primero] = True
            self.descubiertas[segundo] = True
            self.pares += 1
            self.puntaje += 10
        self.seleccionados.clear()
        if self.verificar_victoria():
            self.terminar(True)
        elif len(self.aliens) >= 3:
            self.terminar(False)

    def verificar_victoria(self):
        return all(
            self.descubiertas[i] or self.mazo[i] == self.alien_ruta
            for i in range(self.total)
        )

    def terminar(self, gano):
        self.mensaje_fin = "Ganaste" if gano else "Perdiste"
        guardar_puntaje(self.nombre, self.puntaje, self.intentos)
        self.estado = "ganaste" if gano else "perdiste"

    # ------------------------------------------------------------- pantallas
    def dibujar_menu(self):
        if self.g_menu:
            self.pantalla.blit(self.g_menu, ((ANCHO - self.g_menu.get_width()) // 2, 0))
        else:
            self.pantalla.fill(AZUL_FONDO)
        # Panel oscuro para que el texto se lea sobre la ilustracion.
        panel = pygame.Surface((560, 260), pygame.SRCALPHA)
        panel.fill((0, 10, 25, 190))
        self.pantalla.blit(panel, (ANCHO // 2 - 280, ALTO - 300))
        caja = pygame.Rect(ANCHO // 2 - 220, ALTO - 250, 440, 56)
        pygame.draw.rect(self.pantalla, (0, 20, 45), caja, border_radius=10)
        pygame.draw.rect(self.pantalla, CYAN, caja, 3, border_radius=10)
        self.texto("ESCRIBE TU NOMBRE", 30, CYAN, centro=(ANCHO // 2, caja.y - 30))
        self.texto(self.nombre + ("_" if pygame.time.get_ticks() // 500 % 2 == 0 else ""), 36, BLANCO, centro=caja.center)
        jugar = pygame.Rect(ANCHO // 2 - 140, ALTO - 170, 280, 56)
        self.boton(jugar, "JUGAR", VERDE if self.nombre else (60, 70, 90))
        self.texto("Escribi tu nombre y apreta ENTER", 26, BLANCO, centro=(ANCHO // 2, ALTO - 96))
        self.texto("M = instrucciones   R = records", 24, CYAN, centro=(ANCHO // 2, ALTO - 60))

    def dibujar_juego(self):
        color = ROJO if (self.parpadeo > 0 and self.parpadeo % 2 == 1) else AZUL_FONDO
        self.pantalla.fill(color)
        for i in range(self.total):
            rect = self.rect_carta(i)
            # Un alien revelado queda a la vista hasta que aparece el comodin.
            visible = self.descubiertas[i] or i in self.seleccionados or i in self.aliens
            imagen = None
            if visible:
                imagen = self.escaladas.get(self.mazo[i])
                if imagen is None:
                    imagen = cargar_imagen(self.mazo[i], (self.tamano_carta, self.tamano_carta))
                    self.escaladas[self.mazo[i]] = imagen
            else:
                imagen = self.dorso
                if imagen:
                    imagen = pygame.transform.smoothscale(imagen, (self.tamano_carta, self.tamano_carta))
            if imagen:
                self.pantalla.blit(imagen, rect)
            if visible and self.mazo[i] == self.alien_ruta:
                pygame.draw.rect(self.pantalla, ROJO, rect, 5, border_radius=8)
            else:
                pygame.draw.rect(self.pantalla, AZUL_BOTON, rect, 4, border_radius=8)

        self.texto(f"PUNTOS: {self.puntaje}", 34, ORO, topleft=(16, ALTO - 60))
        self.texto(f"INTENTOS: {self.intentos}", 34, CYAN, topleft=(ANCHO - 250, ALTO - 60))
        self.texto(f"PARES: {self.pares}/{PARES}   ALIENS: {len(self.aliens)}/3", 30, BLANCO, centro=(ANCHO // 2, 60))

        if self.icono_salir:
            self.pantalla.blit(self.icono_salir, (16, ALTO - 130))
        for i, icono in enumerate((self.icono_reiniciar, self.icono_menu, self.icono_records)):
            if icono:
                self.pantalla.blit(icono, (ANCHO // 2 - 100 + i * 70, ALTO - 110))
        self.texto("flechas + ENTER no hacen falta: se juega con el mouse", 22, (130, 160, 200), centro=(ANCHO // 2, 26))

    def dibujar_fin(self, gano):
        fondo = self.g_ganador if gano else self.g_perdiste
        self.pantalla.fill(AZUL_FONDO)
        if fondo:
            self.pantalla.blit(fondo, ((ANCHO - fondo.get_width()) // 2, 0))
        titulo = "GANASTE" if gano else "PERDISTE"
        self.texto(titulo, 90, ORO if gano else ROJO, centro=(ANCHO // 2, 90))
        self.texto(f"PUNTAJE: {self.puntaje}   INTENTOS: {self.intentos}", 44, BLANCO, centro=(ANCHO // 2, ALTO - 120))
        self.texto("ENTER para volver a jugar", 30, CYAN, centro=(ANCHO // 2, ALTO - 60))

    def dibujar_instrucciones(self):
        self.pantalla.fill(AZUL_FONDO)
        if self.g_instrucciones:
            self.pantalla.blit(self.g_instrucciones, ((ANCHO - self.g_instrucciones.get_width()) // 2, (ALTO - self.g_instrucciones.get_height()) // 2))
        self.texto("ENTER o click para empezar", 30, CYAN, centro=(ANCHO // 2, ALTO - 30))

    def dibujar_records(self):
        self.pantalla.fill(AZUL_FONDO)
        if self.g_records:
            self.pantalla.blit(self.g_records, ((ANCHO - self.g_records.get_width()) // 2, 0))
        self.texto("MEJORES PUNTAJES", 46, ORO, centro=(ANCHO // 2, 70))
        jugadores = cargar_ranking()[:7]
        if not jugadores:
            self.texto("Todavia no hay partidas guardadas", 32, BLANCO, centro=(ANCHO // 2, ALTO // 2))
        for i, j in enumerate(jugadores):
            color = CYAN if j["nombre"].lower() == self.nombre.lower() else BLANCO
            self.texto(f"{i + 1}. {j['nombre']}", 34, color, topleft=(ANCHO // 2 - 220, 150 + i * 52))
            self.texto(f"{j['puntaje']} puntos", 34, color, topleft=(ANCHO // 2 + 60, 150 + i * 52))
        self.texto("ENTER para volver", 30, CYAN, centro=(ANCHO // 2, ALTO - 40))

    # ------------------------------------------------------------------ bucle
    def correr(self):
        self.poner_musica("menu")
        while True:
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    pygame.quit()
                    return
                if evento.type == pygame.KEYDOWN:
                    self.tecla(evento)
                if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
                    self.click(evento.pos)
            if self.estado == "juego":
                if self.bloqueo > 0:
                    self.bloqueo -= 1
                    if self.bloqueo == 0:
                        if len(self.aliens) >= 3:
                            self.terminar(False)
                        elif self.seleccionados:
                            self.comprobar_par()
                if self.parpadeo > 0:
                    self.parpadeo -= 1

            if self.estado == "menu":
                self.dibujar_menu()
            elif self.estado == "instrucciones":
                self.dibujar_instrucciones()
            elif self.estado == "juego":
                self.dibujar_juego()
            elif self.estado == "records":
                self.dibujar_records()
            elif self.estado in ("ganaste", "perdiste"):
                self.dibujar_fin(self.estado == "ganaste")
            pygame.display.flip()
            self.reloj.tick(FPS)

    def tecla(self, evento):
        if self.estado == "menu":
            if evento.key == pygame.K_RETURN:
                self.empezar()
            elif evento.key == pygame.K_BACKSPACE:
                self.nombre = self.nombre[:-1]
            elif len(self.nombre) < 14 and evento.unicode and evento.unicode.isprintable():
                self.nombre += evento.unicode
            elif evento.key == pygame.K_m:
                self.estado = "instrucciones"
                self.poner_musica("instrucciones")
            elif evento.key == pygame.K_r:
                self.estado = "records"
                self.poner_musica("records")
        elif self.estado == "instrucciones":
            if evento.key in (pygame.K_RETURN, pygame.K_ESCAPE):
                self.estado = "menu"
                self.poner_musica("menu")
        elif self.estado == "records":
            if evento.key in (pygame.K_RETURN, pygame.K_ESCAPE):
                self.estado = "menu"
                self.poner_musica("menu")
        elif self.estado in ("ganaste", "perdiste"):
            if evento.key == pygame.K_RETURN:
                self.empezar()
            elif evento.key == pygame.K_ESCAPE:
                self.estado = "menu"
                self.poner_musica("menu")

    def click(self, pos):
        if self.estado == "juego":
            if self.icono_salir and pygame.Rect(16, ALTO - 130, 50, 50).collidepoint(pos):
                self.estado = "menu"
                self.poner_musica("menu")
                return
            botones = {
                "reiniciar": pygame.Rect(ANCHO // 2 - 100, ALTO - 110, 60, 60),
                "menu": pygame.Rect(ANCHO // 2 - 30, ALTO - 110, 60, 60),
                "records": pygame.Rect(ANCHO // 2 + 40, ALTO - 110, 60, 60),
            }
            for accion, rect in botones.items():
                if rect.collidepoint(pos):
                    if accion == "reiniciar":
                        self.nuevo_mazo()
                        self.poner_musica("juego")
                    elif accion == "menu":
                        self.estado = "menu"
                        self.poner_musica("menu")
                    else:
                        self.estado = "records"
                        self.poner_musica("records")
                    return
            for i in range(self.total):
                if self.rect_carta(i).collidepoint(pos):
                    self.mostrar_carta(i)
                    return
        elif self.estado == "instrucciones":
            self.estado = "menu"
            self.poner_musica("menu")
        elif self.estado == "records":
            self.estado = "menu"
            self.poner_musica("menu")
        elif self.estado in ("ganaste", "perdiste"):
            self.empezar()

    def empezar(self):
        if not self.nombre.strip():
            self.nombre = "Jugador"
        self.nuevo_mazo()
        self.estado = "juego"
        self.poner_musica("juego")


if __name__ == "__main__":
    Juego().correr()
