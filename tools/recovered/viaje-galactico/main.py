"""
¡Viaje Galáctico! - version web (Pygame).

Puerto del juego de Marcos Zingaretti. El original era una aplicacion de escritorio
con interfaz Tkinter que ademas pedia a la API de Gemini que generara la voz
que narra cada cuerpo celeste, asi que no podia correr en un navegador.

Aca el sistema solar se dibuja con Pygame y el contenido es el mismo que traia
el ejecutable (`cuerpos_celestes.json`: informacion y datos curiosos de cada
cuerpo). La voz la pone el navegador con speechSynthesis, que es el reemplazo
mas parecido a la narracion original.
"""

import json
import math
import os
import random
import sys

import pygame

ANCHO, ALTO = 1280, 720
FPS = 60

AZUL_ESPACIO = (4, 6, 24)
BLANCO = (240, 245, 255)
CYAN = (90, 220, 255)
ORO = (255, 214, 90)

BASE = os.path.dirname(os.path.abspath(sys.argv[0]))
DATOS = os.path.join(BASE, "cuerpos_celestes.json")

# Las 5 preguntas que traia el cuestionario original.
PREGUNTAS = [
    {"pregunta": "¿Cuál es el planeta más cercano al Sol?", "opciones": ["Mercurio", "Venus", "Marte"], "correcta": "Mercurio"},
    {"pregunta": "¿Qué planeta es el más grande de todos?", "opciones": ["Tierra", "Júpiter", "Saturno"], "correcta": "Júpiter"},
    {"pregunta": "¿Cuántos días dura un año en la Tierra?", "opciones": ["88 días", "365 días", "687 días"], "correcta": "365 días"},
    {"pregunta": "¿Qué planeta tiene anillos muy hermosos?", "opciones": ["Marte", "Saturno", "Urano"], "correcta": "Saturno"},
    {"pregunta": "¿Cuál es nuestro planeta, donde vivimos?", "opciones": ["Marte", "Tierra", "Venus"], "correcta": "Tierra"},
]

MENSAJES_QUIZ = {
    5: "¡Eres un experto del espacio!",
    4: "¡Muy bien! ¡Sabes mucho del espacio!",
    3: "¡Bien! ¡Sigue aprendiendo!",
    2: "¡Algo mal, pero sigue intentando!",
    1: "¡Sigue practicando! ¡Lo harás mejor!",
    0: "¡No te rindas! ¡El espacio es grande!",
}

try:  # la voz la presta el navegador
    from js import SpeechSynthesisUtterance, speechSynthesis

    HAY_VOZ = True
except Exception:  # corriendo en escritorio, sin narracion
    HAY_VOZ = False


def narrar(texto):
    if not HAY_VOZ:
        return
    try:
        speechSynthesis.cancel()
        voz = SpeechSynthesisUtterance.new(texto)
        voz.lang = "es-AR"
        voz.rate = 0.95
        voz.pitch = 1.1
        speechSynthesis.speak(voz)
    except Exception as e:
        print("No se pudo narrar:", e)


def cargar_imagen(nombre, tamano=None):
    # En el ejecutable los logos estan en la raiz; en la version web, en imagenes/.
    for carpeta in (os.path.join(BASE, "imagenes"), BASE):
        for ext in (".png", ".jpg"):
            ruta = os.path.join(carpeta, f"{nombre}{ext}")
            if os.path.exists(ruta):
                imagen = pygame.image.load(ruta).convert_alpha()
                return pygame.transform.smoothscale(imagen, tamano) if tamano else imagen
    return None


def color(hexadecimal, por_defecto=BLANCO):
    try:
        hexadecimal = hexadecimal.lstrip("#")
        return tuple(int(hexadecimal[i : i + 2], 16) for i in (0, 2, 4))
    except Exception:
        return por_defecto


class Cuerpo:
    def __init__(self, datos):
        self.nombre = datos["nombre"]
        self.tipo = datos["tipo"]
        self.color = color(datos.get("color"))
        self.info = datos.get("info", "")
        self.curioso = datos.get("dato_curioso", "")
        self.radio_km = datos.get("radio_km")
        self.periodo = datos.get("periodo_orbital_dias")
        self.distancia = datos.get("distancia_ua") or datos.get("distancia_km")
        self.unidad = "UA" if datos.get("distancia_ua") else "km"

        # Escala visual: las distancias reales no entran en una pantalla.
        if self.tipo == "estrella":
            self.orbita = 0
            self.radio = 46
        elif self.tipo == "satelite":
            self.orbita = 0  # gira alrededor de la Tierra
            self.radio = 9
        else:
            self.orbita = 90 + 105 * math.sqrt(float(datos.get("distancia_ua") or 1))
            self.radio = max(9, min(34, 6 + 34 * math.sqrt(float(self.radio_km or 5000) / 69911)))
        self.visitado = False
        self.angulo = random.uniform(0, math.tau)

    def posicion(self, posiciones):
        if self.tipo == "satelite":
            tierra = posiciones.get("Tierra", (ANCHO // 2, ALTO // 2))
            return (tierra[0] + 34, tierra[1] - 16)
        if self.orbita == 0:
            return (ANCHO // 2, ALTO // 2)
        return (
            ANCHO // 2 + math.cos(self.angulo) * self.orbita * 1.35,
            ALTO // 2 + math.sin(self.angulo) * self.orbita * 0.62,
        )


class ViajeGalactico:
    def __init__(self):
        pygame.init()
        self.pantalla = pygame.display.set_mode((ANCHO, ALTO))
        pygame.display.set_caption("¡Viaje Galáctico!")
        self.reloj = pygame.time.Clock()
        self.estrellas = [
            (random.randrange(ANCHO), random.randrange(ALTO), random.choice((1, 1, 2)))
            for _ in range(220)
        ]
        with open(DATOS, encoding="utf-8") as f:
            crudos = json.load(f)["cuerpos"]
        self.cuerpos = [Cuerpo(c) for c in crudos]
        # La Luna necesita saber donde esta la Tierra, asi que va despues.
        orden = {"estrella": 0, "planeta": 1, "satelite": 2}
        self.cuerpos.sort(key=lambda c: (orden[c.tipo], c.orbita))
        self.logo = cargar_imagen("logo aventura espacial", (300, 300))
        self.seleccionado = None
        self.estado = "titulo"
        self.tiempo = 0
        self.visitados = 0
        self.aviso = ""
        self.aviso_tiempo = 0
        self.pregunta_actual = 0
        self.opciones = []
        self.puntuacion = 0
        self.respuesta_elegida = None
        self.mensaje_resultado = ""

    # ------------------------------------------------------------------ dibujo
    def texto(self, mensaje, tamano, col, centro=None, topleft=None, ancho_max=None):
        fuente = pygame.font.Font(None, tamano)
        if ancho_max:
            lineas, actual = [], ""
            for palabra in mensaje.split():
                prueba = f"{actual} {palabra}".strip()
                if fuente.size(prueba)[0] > ancho_max and actual:
                    lineas.append(actual)
                    actual = palabra
                else:
                    actual = prueba
            lineas.append(actual)
        else:
            lineas = [mensaje]
        superficie = None
        alto = fuente.get_linesize()
        superficie = pygame.Surface((ancho_max or max(fuente.size(l)[0] for l in lineas), alto * len(lineas)), pygame.SRCALPHA)
        for i, linea in enumerate(lineas):
            superficie.blit(fuente.render(linea, True, col), (0, i * alto))
        rect = superficie.get_rect()
        if centro:
            rect.center = centro
        if topleft:
            rect.topleft = topleft
        self.pantalla.blit(superficie, rect)
        return rect

    def boton(self, rect, etiqueta, col=(30, 90, 200)):
        pygame.draw.rect(self.pantalla, col, rect, border_radius=12)
        pygame.draw.rect(self.pantalla, CYAN, rect, 2, border_radius=12)
        self.texto(etiqueta, 30, BLANCO, centro=rect.center)

    def fondo(self):
        self.pantalla.fill(AZUL_ESPACIO)
        for x, y, tam in self.estrellas:
            pygame.draw.circle(self.pantalla, (200, 210, 240), (x, y), tam)

    def posiciones(self):
        return {c.nombre: c.posicion({}) for c in self.cuerpos if c.tipo != "satelite"}

    # --------------------------------------------------------------- pantallas
    def dibujar_titulo(self):
        self.fondo()
        if self.logo:
            self.pantalla.blit(self.logo, ((ANCHO - self.logo.get_width()) // 2, 90))
        self.texto("UN VIAJE POR EL SISTEMA SOLAR", 46, ORO, centro=(ANCHO // 2, 70))
        self.texto("Tocá cada cuerpo celeste para conocerlo", 32, BLANCO, centro=(ANCHO // 2, ALTO - 200))
        self.boton(pygame.Rect(ANCHO // 2 - 150, ALTO - 150, 300, 60), "EMPEZAR EL VIAJE")
        self.texto("ENTER o click", 26, (150, 180, 220), centro=(ANCHO // 2, ALTO - 70))

    def dibujar_mapa(self):
        self.fondo()
        posiciones = {}
        for cuerpo in self.cuerpos:
            if cuerpo.tipo == "planeta":
                cuerpo.angulo += 0.0006 + 0.004 / max(1.0, cuerpo.orbita / 60)
            posiciones[cuerpo.nombre] = cuerpo.posicion(posiciones)

        # orbitas
        for cuerpo in self.cuerpos:
            if cuerpo.orbita:
                pygame.draw.ellipse(
                    self.pantalla,
                    (40, 60, 120),
                    pygame.Rect(
                        ANCHO // 2 - cuerpo.orbita * 1.35,
                        ALTO // 2 - cuerpo.orbita * 0.62,
                        cuerpo.orbita * 2.7,
                        cuerpo.orbita * 1.24,
                    ),
                    1,
                )

        for cuerpo in self.cuerpos:
            x, y = posiciones[cuerpo.nombre]
            radio = cuerpo.radio
            if cuerpo.tipo == "estrella":
                pygame.draw.circle(self.pantalla, (255, 190, 40), (int(x), int(y)), radio + 12)
            pygame.draw.circle(self.pantalla, cuerpo.color, (int(x), int(y)), radio)
            resalte = cuerpo is self.seleccionado
            pygame.draw.circle(self.pantalla, CYAN if resalte else (70, 90, 140), (int(x), int(y)), radio + 4, 2)
            if cuerpo.visitado:
                self.texto("✓", 22, (120, 255, 160), centro=(int(x) + radio + 6, int(y) - radio - 6))
            self.texto(cuerpo.nombre, 24, BLANCO if resalte else (170, 190, 220), centro=(int(x), int(y) + radio + 18))

        self.texto(f"Medallas: {self.visitados}/{len(self.cuerpos)}", 30, ORO, topleft=(20, 20))
        self.boton(pygame.Rect(ANCHO - 340, 16, 310, 52), "CUESTIONARIO (C)", (90, 40, 140))
        self.texto("Tocá un cuerpo para leer su historia  ·  V = escuchar  ·  ESC = volver", 24, (150, 180, 220), centro=(ANCHO // 2, ALTO - 26))

    def dibujar_aviso(self):
        if self.aviso_tiempo <= 0:
            return
        caja = pygame.Rect(0, 0, 620, 66)
        caja.center = (ANCHO // 2, 150)
        capa = pygame.Surface(caja.size, pygame.SRCALPHA)
        capa.fill((20, 10, 60, 230))
        self.pantalla.blit(capa, caja.topleft)
        pygame.draw.rect(self.pantalla, ORO, caja, 2, border_radius=12)
        self.texto(self.aviso, 30, ORO, centro=caja.center)

    def dibujar_ficha(self):
        cuerpo = self.seleccionado
        panel = pygame.Rect(70, 70, ANCHO - 140, ALTO - 140)
        capa = pygame.Surface(panel.size, pygame.SRCALPHA)
        capa.fill((2, 8, 30, 238))
        self.pantalla.blit(capa, panel.topleft)
        pygame.draw.rect(self.pantalla, CYAN, panel, 3, border_radius=16)
        pygame.draw.circle(self.pantalla, cuerpo.color, (panel.x + 90, panel.y + 90), 46)
        self.texto(cuerpo.nombre, 62, ORO, topleft=(panel.x + 165, panel.y + 44))
        self.texto(cuerpo.tipo.capitalize(), 28, CYAN, topleft=(panel.x + 167, panel.y + 108))

        y = panel.y + 175
        self.texto(cuerpo.info, 32, BLANCO, topleft=(panel.x + 60, y), ancho_max=panel.width - 120)
        y += 40 * (1 + len(cuerpo.info) // 74)
        self.texto("Dato curioso", 30, ORO, topleft=(panel.x + 60, y + 20))
        self.texto(cuerpo.curioso, 30, (200, 225, 255), topleft=(panel.x + 60, y + 60), ancho_max=panel.width - 120)

        datos = []
        if cuerpo.radio_km:
            datos.append(f"Radio: {cuerpo.radio_km} km")
        if cuerpo.distancia:
            datos.append(f"Distancia: {cuerpo.distancia} {cuerpo.unidad}")
        if cuerpo.periodo:
            datos.append(f"Vuelta al Sol: {cuerpo.periodo} dias")
        self.texto("   ·   ".join(datos), 26, CYAN, topleft=(panel.x + 60, panel.bottom - 150))

        self.boton(pygame.Rect(panel.x + 60, panel.bottom - 100, 230, 54), "ESCUCHAR (V)")
        self.boton(pygame.Rect(panel.x + 310, panel.bottom - 100, 230, 54), "VOLVER (ESC)", (60, 70, 110))

    def dibujar_final(self):
        self.fondo()
        self.texto("¡COMPLETASTE EL VIAJE!", 70, ORO, centro=(ANCHO // 2, 170))
        self.texto(
            f"Visitaste los {self.visitados} cuerpos celestes del sistema solar.",
            36,
            BLANCO,
            centro=(ANCHO // 2, 270),
        )
        self.texto("Gracias por viajar con nosotros.", 32, CYAN, centro=(ANCHO // 2, 340))
        self.boton(pygame.Rect(ANCHO // 2 - 160, ALTO - 170, 320, 60), "VOLVER A EMPEZAR")

    # ------------------------------------------------------------------ quiz
    def empezar_cuestionario(self):
        self.estado = "cuestionario"
        self.pregunta_actual = 0
        self.puntuacion = 0
        self.respuesta_elegida = None
        self._preparar_pregunta()

    def _preparar_pregunta(self):
        datos = PREGUNTAS[self.pregunta_actual]
        self.opciones = list(datos["opciones"])
        random.shuffle(self.opciones)
        self.respuesta_elegida = None
        narrar(datos["pregunta"])

    def responder(self, opcion):
        if self.respuesta_elegida is not None:
            return
        self.respuesta_elegida = opcion
        correcta = PREGUNTAS[self.pregunta_actual]["correcta"]
        if opcion == correcta:
            self.puntuacion += 1
            narrar("¡Muy bien!")
        else:
            narrar(f"Casi. La respuesta era {correcta}")

    def siguiente_pregunta(self):
        if self.respuesta_elegida is None:
            return
        self.pregunta_actual += 1
        if self.pregunta_actual >= len(PREGUNTAS):
            self.mensaje_resultado = MENSAJES_QUIZ.get(self.puntuacion, "¡Gracias por participar!")
            narrar(f"Puntuación: {self.puntuacion} de {len(PREGUNTAS)}. {self.mensaje_resultado}")
            self.estado = "resultado"
        else:
            self._preparar_pregunta()

    def dibujar_cuestionario(self):
        self.fondo()
        self.texto("CUESTIONARIO ESPACIAL", 54, ORO, centro=(ANCHO // 2, 90))
        datos = PREGUNTAS[self.pregunta_actual]
        self.texto(f"Pregunta {self.pregunta_actual + 1} de {len(PREGUNTAS)}", 28, (150, 180, 220), centro=(ANCHO // 2, 150))
        self.texto(datos["pregunta"], 40, BLANCO, centro=(ANCHO // 2, 230))
        correcta = datos["correcta"]
        for i, opcion in enumerate(self.opciones):
            rect = pygame.Rect(ANCHO // 2 - 280, 300 + i * 90, 560, 70)
            col = (30, 90, 200)
            if self.respuesta_elegida is not None:
                if opcion == correcta:
                    col = (30, 150, 70)
                elif opcion == self.respuesta_elegida:
                    col = (170, 40, 40)
            self.boton(rect, opcion, col)
            self.texto(str(i + 1), 30, ORO, centro=(rect.x - 22, rect.centery))
        if self.respuesta_elegida is not None:
            self.texto("Click o ENTER para seguir", 28, CYAN, centro=(ANCHO // 2, ALTO - 50))
        else:
            self.texto("Elegí una opción (1, 2, 3 o el mouse)", 28, CYAN, centro=(ANCHO // 2, ALTO - 50))

    def dibujar_resultado(self):
        self.fondo()
        self.texto("CUESTIONARIO COMPLETADO", 56, ORO, centro=(ANCHO // 2, 170))
        self.texto(f"Puntuación: {self.puntuacion}/{len(PREGUNTAS)}", 52, (120, 255, 180), centro=(ANCHO // 2, 280))
        self.texto(self.mensaje_resultado, 40, BLANCO, centro=(ANCHO // 2, 360))
        self.boton(pygame.Rect(ANCHO // 2 - 170, ALTO - 170, 340, 60), "VOLVER AL MAPA (ESC)")

    # ------------------------------------------------------------------ logica
    def hablar_seleccionado(self):
        if self.seleccionado:
            narrar(f"{self.seleccionado.nombre}. {self.seleccionado.info} {self.seleccionado.curioso}")

    def elegir(self, pos):
        if self.estado == "mapa":
            if pygame.Rect(ANCHO - 340, 16, 310, 52).collidepoint(pos):
                self.empezar_cuestionario()
                return
            for cuerpo in self.cuerpos:
                x, y = cuerpo.posicion(self.posiciones())
                if math.dist((x, y), pos) <= cuerpo.radio + 12:
                    self.seleccionado = cuerpo
                    if not cuerpo.visitado:
                        cuerpo.visitado = True
                        self.visitados += 1
                        self.aviso = f"¡Descubriste {cuerpo.nombre}!"
                        self.aviso_tiempo = 150
                    self.estado = "ficha"
                    self.hablar_seleccionado()
                    return
        elif self.estado == "ficha":
            panel = pygame.Rect(70, 70, ANCHO - 140, ALTO - 140)
            if pygame.Rect(panel.x + 60, panel.bottom - 100, 230, 54).collidepoint(pos):
                self.hablar_seleccionado()
            elif pygame.Rect(panel.x + 310, panel.bottom - 100, 230, 54).collidepoint(pos):
                self.cerrar_ficha()
        elif self.estado == "cuestionario":
            for i in range(len(self.opciones)):
                rect = pygame.Rect(ANCHO // 2 - 280, 300 + i * 90, 560, 70)
                if rect.collidepoint(pos):
                    if self.respuesta_elegida is None:
                        self.responder(self.opciones[i])
                    else:
                        self.siguiente_pregunta()
                    return
        elif self.estado == "resultado":
            self.estado = "mapa"
        elif self.estado == "titulo":
            self.estado = "mapa"
        elif self.estado == "final":
            for cuerpo in self.cuerpos:
                cuerpo.visitado = False
            self.visitados = 0
            self.estado = "mapa"

    def cerrar_ficha(self):
        if self.visitados >= len(self.cuerpos):
            self.estado = "final"
        else:
            self.estado = "mapa"

    def tecla(self, evento):
        if evento.key == pygame.K_ESCAPE:
            if self.estado == "ficha":
                self.cerrar_ficha()
            elif self.estado in ("cuestionario", "resultado"):
                self.estado = "mapa"
            elif self.estado == "final":
                self.estado = "titulo"
        elif self.estado == "titulo" and evento.key in (pygame.K_RETURN, pygame.K_SPACE):
            self.estado = "mapa"
        elif self.estado == "mapa":
            if evento.key == pygame.K_c:
                self.empezar_cuestionario()
        elif self.estado == "ficha":
            if evento.key == pygame.K_v:
                self.hablar_seleccionado()
            elif evento.key == pygame.K_RETURN:
                self.cerrar_ficha()
        elif self.estado == "cuestionario":
            if evento.key in (pygame.K_1, pygame.K_2, pygame.K_3) and self.respuesta_elegida is None:
                indice = evento.key - pygame.K_1
                if indice < len(self.opciones):
                    self.responder(self.opciones[indice])
            elif evento.key == pygame.K_RETURN and self.respuesta_elegida is not None:
                self.siguiente_pregunta()
        elif self.estado == "resultado" and evento.key == pygame.K_RETURN:
            self.estado = "mapa"

    def correr(self):
        while True:
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    pygame.quit()
                    return
                if evento.type == pygame.KEYDOWN:
                    self.tecla(evento)
                if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
                    self.elegir(evento.pos)
            self.tiempo += 1
            if self.aviso_tiempo > 0:
                self.aviso_tiempo -= 1

            if self.estado == "titulo":
                self.dibujar_titulo()
            elif self.estado == "mapa":
                self.dibujar_mapa()
                self.dibujar_aviso()
            elif self.estado == "ficha":
                self.dibujar_mapa()
                self.dibujar_ficha()
            elif self.estado == "cuestionario":
                self.dibujar_cuestionario()
            elif self.estado == "resultado":
                self.dibujar_resultado()
            elif self.estado == "final":
                self.dibujar_final()
            pygame.display.flip()
            self.reloj.tick(FPS)


if __name__ == "__main__":
    ViajeGalactico().correr()
