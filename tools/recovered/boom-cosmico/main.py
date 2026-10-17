# Decompiled with PyLingual (https://pylingual.io)
# Internal filename: 'juegopicante.py'
# Bytecode version: 3.10.b1 (3439)
# Source timestamp: 1970-01-01 00:00:00 UTC (0)

import pygame
import random
import math
import sys
import json
import os
if getattr(sys, 'frozen', False):
    BASE_DIR = os.path.dirname(sys.executable)
    MEIPASS_DIR = sys._MEIPASS
else:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    MEIPASS_DIR = BASE_DIR
ARCHIVO_REGISTRO = os.path.join(BASE_DIR, 'registro_jugadores.json')
ARCHIVO_REGISTRO_TEMP = os.path.join(BASE_DIR, 'registro_temporal.json')
def cargar_registro():
    # irreducible cflow, using cdg fallback
    if os.path.exists(ARCHIVO_REGISTRO):
        try:
            with open(ARCHIVO_REGISTRO, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return []
    else:
        return []
    return []
def cargar_registro_temporal():
    # irreducible cflow, using cdg fallback
    # ***<module>.cargar_registro_temporal: Failure: Different bytecode
    try:
        if os.path.exists(ARCHIVO_REGISTRO_TEMP):
            with open(ARCHIVO_REGISTRO_TEMP, 'r', encoding='utf-8') as f:
                registro = json.load(f)
                if isinstance(registro, list):
                    registro = [e for e in registro if e.get('nombre', '').lower() != 'jaja']
                    with open(ARCHIVO_REGISTRO_TEMP, 'w', encoding='utf-8') as f:
                        json.dump(registro, f, ensure_ascii=False, indent=2)
                return registro
    except:
        return []
    return []
def guardar_registro(registro):
    try:
        with open(ARCHIVO_REGISTRO, 'w', encoding='utf-8') as f:
            json.dump(registro, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print(f'Error guardando registro: {e}')
def guardar_registro_temporal(registro):
    try:
        with open(ARCHIVO_REGISTRO_TEMP, 'w', encoding='utf-8') as f:
            json.dump(registro, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print(f'Error guardando temporal: {e}')
def nombre_en_top(nombre, cache_extra=None):
    historial = cargar_registro()
    if isinstance(historial, list):
        historial = historial[:5]
    else:
        historial = []
    temp = cargar_registro_temporal()
    if not isinstance(temp, list):
        temp = []
    nombre_lower = nombre.strip().lower()
    for entry in historial:
        if isinstance(entry, dict) and entry.get('nombre', '').lower() == nombre_lower:
                return True
    for entry in temp:
        if isinstance(entry, dict) and entry.get('nombre', '').lower() == nombre_lower:
                return True
    if cache_extra:
        for entry in cache_extra:
            if isinstance(entry, dict) and entry.get('nombre', '').lower() == nombre_lower:
                    return True
    return False
def agregar_puntuacion_temporal(nombre, puntos, nivel, tiempo):
    try:
        if os.path.exists(ARCHIVO_REGISTRO_TEMP):
            with open(ARCHIVO_REGISTRO_TEMP, 'r', encoding='utf-8') as f:
                registro = json.load(f)
        else:
            registro = []
        nuevo = {'nombre': nombre, 'puntos': puntos, 'nivel': nivel, 'tiempo': tiempo}
        registro.append(nuevo)
        with open(ARCHIVO_REGISTRO_TEMP, 'w', encoding='utf-8') as f:
            json.dump(registro, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print(f'Error: {e}')
def agregar_puntuacion(nombre, puntos, nivel, tiempo):
    registro = cargar_registro()
    if len(registro) >= 5:
        menor_puntos = min((entry['puntos'] for entry in registro))
        if puntos <= menor_puntos:
            return
    existente = None
    for i, entry in enumerate(registro):
        if entry['nombre'] == nombre:
            existente = i
            break
    if existente is not None:
        if puntos > registro[existente]['puntos']:
            registro[existente] = {'nombre': nombre, 'puntos': puntos, 'nivel': nivel, 'tiempo': tiempo}
    else:
        registro.append({'nombre': nombre, 'puntos': puntos, 'nivel': nivel, 'tiempo': tiempo})
    registro = sorted(registro, key=lambda x: x['puntos'], reverse=True)[:5]
    guardar_registro(registro)
def limpiar_registro():
    if os.path.exists(ARCHIVO_REGISTRO):
        os.remove(ARCHIVO_REGISTRO)
    if os.path.exists(ARCHIVO_REGISTRO_TEMP):
        os.remove(ARCHIVO_REGISTRO_TEMP)
pygame.init()
pygame.mixer.init()
info = pygame.display.Info()
ESCALA_RENDER = 1.0
ANCHO = int(info.current_w * ESCALA_RENDER)
ALTO = int(info.current_h * ESCALA_RENDER)
pantalla = pygame.display.set_mode((ANCHO, ALTO), pygame.FULLSCREEN)
try:
    ruta_sprite = os.path.join(MEIPASS_DIR, 'arrows.png')
    sprite_flechas = pygame.image.load(ruta_sprite).convert_alpha()
    orig_w, orig_h = (sprite_flechas.get_width(), sprite_flechas.get_height())
    proporcion = orig_w / orig_h
    nuevo_ancho = 240
    nuevo_alto = int(nuevo_ancho / proporcion)
    sprite_flechas = pygame.transform.scale(sprite_flechas, (nuevo_ancho, nuevo_alto))
except Exception as e:
    print(f'Error cargando sprite flechas: {e}')
    sprite_flechas = None
try:
    ruta_icono = os.path.join(MEIPASS_DIR, 'icono.png')
    icono = pygame.image.load(ruta_icono).convert_alpha()
    icono = pygame.transform.scale(icono, (32, 32))
    pygame.display.set_icon(icono)
except Exception as e:
    print(f'Error cargando icono: {e}')
pygame.display.set_caption('¡BOOM CÓSMICO! - Sobrevive, explora y conquista el universo')
reloj = pygame.time.Clock()
NEGRO = (5, 5, 15)
AZUL_OSCURO = (10, 10, 30)
COLORES = {'Aries': (255, 68, 68), 'Tauro': (68, 255, 68), 'Geminis': (255, 255, 68), 'Cancer': (68, 255, 255), 'Leo': (255, 170, 0), 'Virgo': (170, 136, 102), 'Libra': (255, 136, 255), 'Escorpio': (136, 0, 255), 'Sagitario': (255, 0, 136), 'Capricornio': (102, 102, 102), 'Acuario': (0, 170, 255), 'Piscis': (170, 68, 255)}
constelaciones = {'Orion': [(-100, 50), (-50, 80), (0, 60), (50, 70), (100, 40), (0, 0), (-30, -30), (30, -30)], 'Osa Mayor': [(-150, 50), (-100, 30), (-50, 40), (0, 20), (50, 30), (100, 10), (120, -20)], 'Osa Menor': [(-30, 80), (0, 60), (30, 50), (20, 20), (-20, -10), (-40, -30), (0, 0)], 'Cassiopeia': [(-120, 60), (-60, 30), (0, 50), (60, 20), (120, 40)], 'Leo': [(-100, 60), (-50, 80), (0, 50), (50, 60), (100, 40), (30, 0), (0, -40), (-30, -20)], 'Escorpio': [(-120, 40), (-80, 20), (-40, 10), (0, 0), (40, -10), (80, 0), (120, 20), (100, -30)], 'Cygnus': [(-100, 60), (-50, 40), (0, 50), (50, 40), (100, 60), (0, 0), (0, -40)], 'Gemelos': [(-60, 80), (-40, 60), (-20, 70), (20, 70), (40, 60), (60, 80), (-20, 20), (20, 20)], 'Tauro': [(-80, 40), (-40, 20), (0, 30), (40, 20), (80, 40), (0, -20), (-20, -40)], 'Virgo': [(-100, 50), (-50, 30), (0, 40), (50, 20), (100, 30), (20, -20), (-20, -40)], 'Pegaso': [(-100, 40), (-50, 60), (0, 40), (50, 60), (100, 40), (0, 0), (-50, -20), (50, -20)], 'Andromeda': [(-100, 50), (-50, 70), (0, 50), (50, 30), (100, 50), (50, 0), (0, -30)]}
EMOJIS_CONSTELACIONES = {'Orion': '🎯', 'Osa Mayor': '🐻', 'Osa Menor': '🐻', 'Cassiopeia': '👸', 'Leo': '🦁', 'Escorpio': '🦂', 'Cygnus': '🦢', 'Gemelos': '👫', 'Tauro': '🐂', 'Virgo': '👩', 'Pegaso': '🐎', 'Andromeda': '🧚'}
_cache_fuentes = {}
try:
    fuente_emoji = pygame.font.Font('C:\\Windows\\Fonts\\seguiemj.ttf', 36)
except Exception:
    # Web port: that font only exists on Windows, and the original fallback
    # referenced a helper defined further down the file.
    fuente_emoji = pygame.font.Font(None, 36)
def obtener_fuente(tamano):
    if tamano not in _cache_fuentes:
        _cache_fuentes[tamano] = pygame.font.Font(None, tamano)
    return _cache_fuentes[tamano]
def render_emoji(superficie, emoji, x, y, tamano=36, color=(255, 255, 255)):
    try:
        texto = fuente_emoji.render(emoji, True, color)
        rect = texto.get_rect(center=(x, y))
        superficie.blit(texto, rect)
        return True
    except:
        return False
datos = ['Aries: El carnero de oro!', 'Tauro: Fuerte y determinado!', 'Geminis: Mente aguda!', 'Cancer: Protector del hogar!', 'Leo: El rey del zodiaco!', 'Virgo: Perfectionista!', 'Libra: Buscando equilibrio!', 'Escorpio: Misterioso!', 'Sagitario: El aventuras!', 'Capricornio: Ambicioso!', 'Acuario: Revolucionario!', 'Piscis: Intuitivo!']
class Sonido:
    def __init__(self):
        self.sonidos = {}
        self.musica_cargada = False
        self.musica_archivo = None
        self.ambiente_cargado = False
        self.base_path = MEIPASS_DIR
        self.sonidos = {'estrella': None, 'powerup': None, 'golpe': None, 'combo': None, 'constelacion': None, 'gameover': None}
        self.cargar_sonidos()
        self.cargar_musica()
        self.cargar_ambiente()
    def cargar_sonidos(self):
        archivos = {'estrella': ['constelacion.wav', 'estrella.wav', 'estrella_nueva.wav', 'coin.wav'], 'powerup': ['powerup.wav', 'power.wav'], 'golpe': ['golpe.wav', 'hit.wav', 'damage.wav'], 'combo': ['combo.wav'], 'constelacion': ['constelacion.wav', 'complete.wav'], 'gameover': ['gameover.wav', 'over.wav']}
        for clave, nombres in archivos.items():
            for nombre in nombres:
                ruta = os.path.join(self.base_path, nombre)
                if os.path.exists(ruta):
                    try:
                        self.sonidos[clave] = pygame.mixer.Sound(ruta)
                    except Exception as e:
                        print(f'Error cargando sonido {nombre}: {e}')
                    break
    def cargar_musica(self):
        # ***<module>.Sonido.cargar_musica: Failure: Different control flow
        try:
            for nombre in ['musica.mp3', 'musica.wav']:
                ruta_musica = os.path.join(self.base_path, nombre)
                if os.path.exists(ruta_musica):
                    pygame.mixer.music.load(ruta_musica)
                    pygame.mixer.music.set_volume(1.0)
                    self.musica_cargada = True
        except Exception as e:
            print(f'Error cargando musica: {e}')
    def cargar_ambiente(self):
        try:
            ruta = os.path.join(self.base_path, 'ambiente_menu.wav')
            if os.path.exists(ruta):
                self.ambiente = pygame.mixer.Sound(ruta)
                self.ambiente.set_volume(1.0)
                self.ambiente_cargado = True
        except Exception as e:
            print(f'Error cargando ambiente: {e}')
    def iniciar_ambiente(self):
        if self.ambiente_cargado:
            try:
                self.ambiente.play((-1))
            except:
                return
    def detener_ambiente(self):
        if self.ambiente_cargado:
            try:
                self.ambiente.stop()
            except:
                return
    def play(self, tipo='estrella'):
        try:
            if self.sonidos.get(tipo):
                if self.musica_cargada:
                    pygame.mixer.music.set_volume(0.3)
                self.sonidos[tipo].set_volume(0.5)
                self.sonidos[tipo].play(0, 0, 0)
                if self.musica_cargada:
                    pygame.mixer.music.set_volume(1.0)
        except Exception as e:
            print(f'Error sonido {tipo}: {e}')
    def play_estrella(self):
        self.play('estrella')
    def play_powerup(self):
        self.play('powerup')
    def play_golpe(self):
        self.play('golpe')
    def play_combo(self):
        self.play('combo')
    def play_constelacion(self):
        self.play('constelacion')
    def play_gameover(self):
        self.play('gameover')
    def play_escudo(self):
        self.play('golpe')
    def iniciar_musica(self):
        if self.musica_cargada:
            try:
                pygame.mixer.music.play((-1))
                print('Musica iniciada')
            except Exception as e:
                print(f'Error reproduciendo musica: {e}')
    def detener_musica(self):
        try:
            pygame.mixer.music.stop()
        except:
            return None
    def silenciar(self):
        pygame.mixer.pause()
    def activar(self):
        pygame.mixer.unpause()
sonido = Sonido()
class Cohete:
    def __init__(self):
        self.x = ANCHO // 2
        self.y = ALTO // 2
        self.velocidad_base = 6
        self.velocidad = 6
        self.vidas = 3
        self.escudo = 0
        self.multiplicador = 1
        self.puntuacion_combo = 0
        self.invulnerable = 0
        self.turbo = 0
        self.rect = pygame.Rect(self.x - 20, self.y - 15, 40, 30)
        self.angulo = 0
        self._nave_cache = None
        self._crear_nave_cache()
    def _crear_nave_cache(self):
        temp_surf = pygame.Surface((50, 50), pygame.SRCALPHA)
        cx, cy = (25, 25)
        pygame.draw.polygon(temp_surf, (80, 80, 80), [(cx - 12, cy - 10), (cx, cy - 25), (cx + 12, cy - 10)])
        pygame.draw.polygon(temp_surf, (200, 200, 200), [(cx - 15, cy + 5), (cx, cy - 20), (cx + 15, cy + 5), (cx, cy + 15)])
        pygame.draw.polygon(temp_surf, (220, 220, 220), [(cx, cy - 20), (cx - 8, cy + 5), (cx + 8, cy + 5)], 2)
        pygame.draw.circle(temp_surf, (0, 180, 255), (cx, cy - 5), 8)
        pygame.draw.circle(temp_surf, (100, 220, 255), (cx, cy - 5), 6)
        pygame.draw.circle(temp_surf, (200, 240, 255), (cx, cy - 5), 3)
        pygame.draw.circle(temp_surf, (255, 255, 255), (cx, cy - 5), 1)
        pygame.draw.polygon(temp_surf, (150, 50, 0), [(cx - 6, cy + 12), (cx, cy + 20), (cx + 6, cy + 12)])
        self._nave_cache = temp_surf
    def mover(self, teclas):
        dx, dy = (0, 0)
        velocidad = self.velocidad
        if teclas[pygame.K_UP]:
            dy = -velocidad
            self.angulo = 0
        if teclas[pygame.K_DOWN]:
            dy = velocidad
            self.angulo = 180
        if teclas[pygame.K_LEFT]:
            dx = -velocidad
            self.angulo = 270
        if teclas[pygame.K_RIGHT]:
            dx = velocidad
            self.angulo = 90
        if dx != 0 and dy == 0:
            pass
        else:
            if dy != 0 and dx == 0:
                pass
            else:
                if dx != 0 and dy != 0:
                        if dx > 0 and dy < 0:
                            self.angulo = 45
                        else:
                            if dx > 0 and dy > 0:
                                self.angulo = 135
                            else:
                                if dx < 0 and dy > 0:
                                    self.angulo = 225
                                else:
                                    if dx < 0 and dy < 0:
                                            self.angulo = 315
                        dx = int(dx * 0.707)
                        dy = int(dy * 0.707)
        if dx != 0 or dy != 0:
            self.x = max(20, min(ANCHO - 20, self.x + dx))
            self.y = max(80, min(ALTO - 20, self.y + dy))
        self.rect = pygame.Rect(self.x - 20, self.y - 15, 40, 30)
        if self.invulnerable > 0:
            self.invulnerable -= 1
        if self.escudo > 0:
            self.escudo -= 1
        if self.turbo > 0:
            self.turbo -= 1
    def dibujar(self, superficie):
        if self.invulnerable > 0 and pygame.time.get_ticks() % 100 < 50:
                return
        if self.angulo == 0:
            fx_dir, fy_dir = (0, 25)
        else:
            if self.angulo == 180:
                fx_dir, fy_dir = (0, (-25))
            else:
                if self.angulo == 90:
                    fx_dir, fy_dir = ((-25), 0)
                else:
                    if self.angulo == 270:
                        fx_dir, fy_dir = (25, 0)
                    else:
                        if self.angulo == 45:
                            fx_dir, fy_dir = ((-15), 20)
                        else:
                            if self.angulo == 135:
                                fx_dir, fy_dir = ((-15), (-20))
                            else:
                                if self.angulo == 225:
                                    fx_dir, fy_dir = (15, (-20))
                                else:
                                    if self.angulo == 315:
                                        fx_dir, fy_dir = (15, 20)
        for _ in range(4):
            dist = random.randint(18, 35)
            fx = int(self.x + fx_dir * dist / 25 + random.randint((-8), 8))
            fy = int(self.y + fy_dir * dist / 25 + random.randint((-8), 8))
            tamano = random.randint(6, 14)
            color = random.choice([(255, 100, 0), (255, 150, 0), (255, 180, 0), (255, 80, 0), (200, 40, 0)])
            pygame.draw.circle(superficie, color, (fx, fy), tamano)
        for _ in range(3):
            dist = random.randint(10, 28)
            fx = int(self.x + fx_dir * dist / 25 + random.randint((-6), 6))
            fy = int(self.y + fy_dir * dist / 25 + random.randint((-6), 6))
            tamano = random.randint(4, 10)
            color = random.choice([(255, 220, 50), (255, 255, 100), (255, 200, 0)])
            pygame.draw.circle(superficie, color, (fx, fy), tamano)
        nave_rotada = pygame.transform.rotate(self._nave_cache, -self.angulo)
        rect = nave_rotada.get_rect(center=(self.x, self.y))
        superficie.blit(nave_rotada, rect)
        if self.escudo > 0:
            pygame.draw.circle(superficie, (0, 200, 255), (self.x, self.y), 35, 3)
            for i in range(0, 360, 45):
                x = int(self.x + 32 * math.cos(math.radians(i + pygame.time.get_ticks() // 20)))
                y = int(self.y + 32 * math.sin(math.radians(i + pygame.time.get_ticks() // 20)))
                pygame.draw.circle(superficie, (100, 255, 255), (x, y), 2)
class Estrella:
    def __init__(self, x, y, color, especial=False):
        self.x = x
        self.y = y
        self.color = color
        self.especial = especial
        self.radio = 18 if especial else 12
        self.rect = pygame.Rect(x - 20, y - 20, 40, 40)
        self.pulso = random.uniform(0, 2 * math.pi)
    def dibujar(self, superficie):
        self.pulso += 0.1
        tamano_pulso = int(math.sin(self.pulso) * 3)
        if self.especial:
            for i in range(5, 35, 10):
                pygame.draw.circle(superficie, self.color, (self.x, self.y), i + tamano_pulso)
            for i in range(8, 20, 8):
                pygame.draw.circle(superficie, self.color, (self.x, self.y), i + tamano_pulso)
        pygame.draw.circle(superficie, (255, 255, 255), (self.x, self.y), 6)
        pygame.draw.circle(superficie, self.color, (self.x, self.y), 10)
        self.rect = pygame.Rect(self.x - 20, self.y - 20, 40, 40)
class Particula:
    def __init__(self, x, y, color, explosion=False):
        self.x = x
        self.y = y
        self.color = color
        if explosion:
            angulo = random.uniform(0, 2 * math.pi)
            velocidad = random.uniform(3, 10)
        else:
            angulo = random.uniform(-math.pi / 3, math.pi / 3) + random.choice([0, math.pi])
            velocidad = random.uniform(2, 6)
        self.vx = math.cos(angulo) * velocidad
        self.vy = math.sin(angulo) * velocidad
        self.vida = 50
        self.tamano = random.randint(4, 10)
        self.gravedad = 0.15 if explosion else 0.05
    def actualizar(self):
        self.x += self.vx
        self.y += self.vy
        self.vy += self.gravedad
        self.vida -= 1
        self.tamano = max(1, self.tamano - 0.15)
    def dibujar(self, superficie):
        if self.vida > 0:
            pygame.draw.circle(superficie, self.color, (int(self.x), int(self.y)), int(self.tamano))
class Asteroid:
    def __init__(self, desde_menu=False):
        lado = random.choice(['arriba', 'abajo', 'izquierda', 'derecha'])
        velocidad = random.uniform(2, 5) if desde_menu else random.uniform(1, 3)
        if lado == 'izquierda':
            self.x = (-60)
            self.y = random.randint(100, ALTO - 100)
            self.vx = velocidad
            self.vy = random.uniform((-0.5), 0.5)
        else:
            if lado == 'derecha':
                self.x = ANCHO + 60
                self.y = random.randint(100, ALTO - 100)
                self.vx = -velocidad
                self.vy = random.uniform((-0.5), 0.5)
            else:
                if lado == 'arriba':
                    self.x = random.randint(100, ANCHO - 100)
                    self.y = (-60)
                    self.vx = random.uniform((-0.5), 0.5)
                    self.vy = velocidad
                else:
                    self.x = random.randint(100, ANCHO - 100)
                    self.y = ALTO + 60
                    self.vx = random.uniform((-0.5), 0.5)
                    self.vy = -velocidad
        self.tamano = random.randint(25, 55)
        self.rotacion = random.uniform(0, 360)
        self.velocidad_rotacion = random.uniform((-2), 2)
        tono_base = random.randint(90, 130)
        self.color_principal = (tono_base - 20, tono_base - 15, tono_base - 10)
        self.color_alto = (tono_base + 30, tono_base + 25, tono_base + 20)
        self.color_sombra = (tono_base - 40, tono_base - 35, tono_base - 30)
        self.puntos = []
        num_puntos = random.randint(6, 10)
        for i in range(num_puntos):
            angle = i / num_puntos * 2 * math.pi
            radio = self.tamano * random.uniform(0.7, 1.0)
            self.puntos.append((math.cos(angle) * radio, math.sin(angle) * radio))
        self.crateres = []
        for _ in range(random.randint(1, 3)):
            angle = random.uniform(0, 2 * math.pi)
            dist = random.uniform(0.2, 0.6)
            self.crateres.append({'angle': angle, 'dist': dist, 'radio': random.uniform(0.15, 0.3)})
        self.estela = []
    def actualizar(self):
        self.x += self.vx
        self.y += self.vy
        self.rotacion += self.velocidad_rotacion
        self.estela.append({'x': self.x - self.vx * 4, 'y': self.y - self.vy * 4, 'vida': 80, 'tamano': self.tamano * 0.8})
        if random.random() < 0.4:
            self.estela.append({'x': self.x - self.vx * 5 + random.uniform((-10), 10), 'y': self.y - self.vy * 5 + random.uniform((-10), 10), 'vida': 70, 'tamano': self.tamano * 0.6})
        if random.random() < 0.25:
            self.estela.append({'x': self.x - self.vx * 6 + random.uniform((-15), 15), 'y': self.y - self.vy * 6 + random.uniform((-15), 15), 'vida': 60, 'tamano': self.tamano * 0.4})
        for p in self.estela:
            p['vida'] -= 1.0
            p['tamano'] *= 0.95
        self.estela = [p for p in self.estela if p['vida'] > 0]
        if len(self.estela) > 80:
            self.estela = self.estela[(-80):]
        if self.x < (-150) or self.x > ANCHO + 150 or self.y < (-150) or (self.y > ALTO + 150):
            return True
        else:
            return False
    def dibujar(self, superficie):
        for p in self.estela:
            if p['vida'] > 15 and p['tamano'] > 2:
                    vida_ratio = p['vida'] / 80
                    if vida_ratio > 0.6:
                        r = 255
                        g = int(200 + 55 * (vida_ratio - 0.6) / 0.4)
                        b = int(50 + 100 * (vida_ratio - 0.6) / 0.4)
                    else:
                        if vida_ratio > 0.3:
                            r = 255
                            g = int(100 + 100 * (vida_ratio - 0.3) / 0.3)
                            b = 0
                        else:
                            r = int(150 + 105 * vida_ratio / 0.3)
                            g = int(30 * vida_ratio / 0.3)
                            b = 0
                    pygame.draw.circle(superficie, (r, g, b), (int(p['x']), int(p['y'])), max(1, int(p['tamano'])))
        puntos_rotados = []
        for px, py in self.puntos:
            rad = math.radians(self.rotacion)
            rx = px * math.cos(rad) - py * math.sin(rad)
            ry = px * math.sin(rad) + py * math.cos(rad)
            puntos_rotados.append((self.x + rx, self.y + ry))
        if len(puntos_rotados) >= 3:
            pygame.draw.polygon(superficie, self.color_sombra, puntos_rotados)
            pygame.draw.polygon(superficie, self.color_principal, puntos_rotados, 3)
            puntos_medios = []
            for i in range(len(puntos_rotados)):
                p1 = puntos_rotados[i]
                p2 = puntos_rotados[(i + 1) % len(puntos_rotados)]
                pm = ((p1[0] + p2[0]) / 2, (p1[1] + p2[1]) / 2)
                puntos_medios.append(pm)
            if len(puntos_medios) >= 3:
                pygame.draw.polygon(superficie, self.color_alto, puntos_medios)
        for crater in self.crateres:
            rad = math.radians(self.rotacion)
            cx = self.x + math.cos(crater['angle']) * crater['dist'] * self.tamano
            cy = self.y + math.sin(crater['angle']) * crater['dist'] * self.tamano
            radio_crater = crater['radio'] * self.tamano
            pygame.draw.circle(superficie, self.color_sombra, (int(cx), int(cy)), int(radio_crater))
            pygame.draw.circle(superficie, self.color_principal, (int(cx), int(cy)), int(radio_crater * 0.7))
class Meteorito:
    def __init__(self, juego=None, nivel=1):
        self.juego = juego
        self.nivel = nivel
        lado = random.choice(['arriba', 'abajo', 'izquierda', 'derecha'])
        velocidad_base = 2 + (nivel - 1) * 0.5
        if lado == 'arriba':
            self.x = random.randint(0, ANCHO)
            self.y = (-30)
            self.vy = random.uniform(velocidad_base * 0.5, velocidad_base)
            self.vx = random.uniform(-velocidad_base * 0.5, velocidad_base * 0.5)
        else:
            if lado == 'abajo':
                self.x = random.randint(0, ANCHO)
                self.y = ALTO + 30
                self.vy = random.uniform(-velocidad_base, -velocidad_base * 0.5)
                self.vx = random.uniform(-velocidad_base * 0.5, velocidad_base * 0.5)
            else:
                if lado == 'izquierda':
                    self.x = (-30)
                    self.y = random.randint(0, ALTO)
                    self.vx = random.uniform(velocidad_base * 0.5, velocidad_base)
                    self.vy = random.uniform(-velocidad_base * 0.5, velocidad_base * 0.5)
                else:
                    self.x = ANCHO + 30
                    self.y = random.randint(0, ALTO)
                    self.vx = random.uniform(-velocidad_base, -velocidad_base * 0.5)
                    self.vy = random.uniform(-velocidad_base * 0.5, velocidad_base * 0.5)
        self.tamano = min(15 + nivel, 30)
        self.rect = pygame.Rect(self.x - self.tamano, self.y - self.tamano, self.tamano * 2, self.tamano * 2)
        self.rotacion = 0
        self.velocidad_rotacion = random.uniform((-5), 5)
        self.tamano_rojo = False
        self.fuego_estela = []
    def actualizar(self):
        slowmo = 0.35 if self.juego and self.juego.cohete.turbo > 0 else 1.0
        self.x += self.vx * slowmo
        self.y += self.vy * slowmo
        self.rotacion += self.velocidad_rotacion * slowmo
        self.rect = pygame.Rect(self.x - self.tamano, self.y - self.tamano, self.tamano * 2, self.tamano * 2)
        if self.tamano_rojo:
            for _ in range(2):
                offset_ang = random.uniform(0, 2 * math.pi)
                dist = random.uniform(2, self.tamano * 0.8)
                fx = self.x - self.vx * random.uniform(1, 4) + math.cos(offset_ang) * dist
                fy = self.y - self.vy * random.uniform(1, 4) + math.sin(offset_ang) * dist
                self.fuego_estela.append({'x': fx, 'y': fy, 'vida': random.uniform(15, 30), 'tamano': random.uniform(3, self.tamano * 0.5), 'fase': random.uniform(0, 6.28)})
            for p in self.fuego_estela:
                p['vida'] -= random.uniform(0.5, 1.5)
                p['tamano'] *= 0.96
                p['x'] += random.uniform((-0.3), 0.3)
                p['y'] += random.uniform((-0.3), 0.3)
            self.fuego_estela = [p for p in self.fuego_estela if p['vida'] > 0]
            if len(self.fuego_estela) > 40:
                self.fuego_estela = self.fuego_estela[(-40):]
    def dibujar(self, superficie):
        if self.tamano_rojo:
            for p in self.fuego_estela:
                vida_ratio = p['vida'] / 30
                if vida_ratio > 0.6:
                    r, g, b = (255, int(200 * (vida_ratio - 0.6) / 0.4), 0)
                else:
                    if vida_ratio > 0.3:
                        r, g, b = (255, int(100 * (vida_ratio - 0.3) / 0.3), 0)
                    else:
                        r, g, b = (int(200 * vida_ratio / 0.3), 0, 0)
                pygame.draw.circle(superficie, (r, g, b), (int(p['x']), int(p['y'])), max(1, int(p['tamano'])))
            for radio in range(self.tamano + 8, self.tamano - 2, (-6)):
                alpha_ratio = 1 - (radio - self.tamano + 2) / 12
                rojo = 255
                verde = int(max(0, 80 - (radio - self.tamano + 2) * 7))
                pygame.draw.circle(superficie, (rojo, verde, 0), (int(self.x), int(self.y)), radio, 2)
            pygame.draw.circle(superficie, (255, 255, 200), (int(self.x), int(self.y)), int(self.tamano * 0.3))
            pygame.draw.circle(superficie, (255, 200, 50), (int(self.x), int(self.y)), int(self.tamano * 0.5))
            pygame.draw.circle(superficie, (255, 80, 0), (int(self.x), int(self.y)), int(self.tamano * 0.7))
            pygame.draw.circle(superficie, (180, 20, 0), (int(self.x), int(self.y)), self.tamano)
        else:
            pygame.draw.circle(superficie, (150, 50, 30), (int(self.x), int(self.y)), self.tamano)
            pygame.draw.circle(superficie, (100, 30, 20), (int(self.x), int(self.y)), self.tamano - 5)
        self.rect = pygame.Rect(self.x - self.tamano, self.y - self.tamano, self.tamano * 2, self.tamano * 2)
class Potenciador:
    def __init__(self, x, y):
        self.tipo = random.choice(['escudo', 'slowmo', 'vida', 'multi'])
        self.x = x
        self.y = y
        self.rect = pygame.Rect(x - 25, y - 25, 50, 50)
        self.tiempo = 600
    def dibujar(self, superficie):
        if self.tiempo < 120 and pygame.time.get_ticks() // 200 % 2 == 0:
                return
        colores = {'escudo': ((0, 150, 255), (0, 200, 255), (150, 220, 255)), 'slowmo': ((70, 70, 200), (100, 100, 255), (180, 180, 255)), 'vida': ((0, 200, 50), (0, 255, 100), (150, 255, 150)), 'multi': ((200, 0, 200), (255, 50, 255), (255, 150, 255))}
        color_oscuro, color_principal, color_claro = colores[self.tipo]
        for i in range(30, 15, (-8)):
            pygame.draw.circle(superficie, color_oscuro, (self.x, self.y), i)
        pygame.draw.circle(superficie, color_principal, (self.x, self.y), 18)
        pygame.draw.circle(superficie, color_claro, (self.x, self.y), 12)
        pygame.draw.circle(superficie, (255, 255, 255), (self.x, self.y), 10)
        letras = {'escudo': 'E', 'slowmo': 'S', 'vida': 'V', 'multi': 'M'}
        fuente = obtener_fuente(32)
        texto = fuente.render(letras[self.tipo], True, (0, 0, 0))
        rect_texto = texto.get_rect(center=(self.x, self.y))
        superficie.blit(texto, rect_texto)
class Juego:
    def __init__(self):
        self.cohete = Cohete()
        self.estrellas = []
        self.particulas = []
        self.meteoritos = []
        self.potenciadores = []
        self.constelacion_actual = None
        self.puntos = 0
        self.puntuacion_total = 0
        self.nivel = 1
        self.mostrando_constelacion = False
        self.tiempo_inicio_pausa = 0
        self.fondo_estrellas = []
        self.nebulosas = []
        self.combo_actual = 0
        self.tiempo_combo = 0
        self.meteoritos_creados = 0
        self.pausado = False
        self.juego_terminado = False
        self.menu = True
        self.logueando = True
        self.nombre_jugador = ''
        self.error_nombre = None
        self.estrellas_en_pausa = []
        self.color_en_pausa = (255, 255, 0)
        self.tiempo_inicio = pygame.time.get_ticks()
        self.tiempo_final = 0
        self.nivel_altermino = 1
        self.tiempo_nivel = 1800
        self.alien_aparecio = False
        self.asteroides_menu = []
        for _ in range(5):
            self.asteroides_menu.append(Asteroid(desde_menu=True))
        self._overlay_constelacion = pygame.Surface((ANCHO, ALTO), pygame.SRCALPHA)
        self._overlay_gameover = pygame.Surface((ANCHO, ALTO), pygame.SRCALPHA)
        self._overlay_constelacion.fill((5, 0, 25, 220))
        self._overlay_gameover.fill((0, 0, 0, 230))
        self.crear_fondo()
        self.nueva_constelacion()
    def crear_fondo(self):
        for _ in range(120):
            x = random.randint(0, ANCHO)
            y = random.randint(0, ALTO)
            color = random.choice([(255, 107, 157), (157, 107, 255), (107, 255, 157), (157, 255, 255), (255, 255, 107), (255, 200, 100), (100, 200, 255)])
            tamano = random.randint(1, 2)
            self.fondo_estrellas.append([x, y, color, tamano, random.uniform(0, 2 * math.pi)])
        for _ in range(8):
            x = random.randint(0, ANCHO)
            y = random.randint(0, ALTO)
            radio = random.randint(100, 250)
            color = random.choice([(26, 10, 58), (32, 10, 74), (21, 10, 53)])
            self.nebulosas.append([x, y, radio, color])
    def nueva_constelacion(self):
        if self.nivel > 1:
            self.puntos += 500 * self.nivel
        self.constelacion_actual = random.choice(list(constelaciones.keys()))
        self.estrellas.clear()
        posiciones = constelaciones[self.constelacion_actual]
        escala = 3.0
        centro_x = ANCHO // 2 - 100
        centro_y = ALTO // 2 - 100
        color = COLORES.get(self.constelacion_actual, (255, 255, 0))
        especial = random.random() < 0.1 + self.nivel * 0.05
        for i, pos in enumerate(posiciones):
            x = pos[0] * escala + centro_x
            y = pos[1] * escala + centro_y
            self.estrellas.append(Estrella(x, y, color, especial=i == 0 and especial))
        self.nivel += 1
        self.tiempo_nivel = 1800
        self.alien_aparecio = False
        self.modo_furia = False
        for meteorito in self.meteoritos:
            meteorito.tamano_rojo = False
    def cap_particulas(self):
        if len(self.particulas) > 150:
            self.particulas = self.particulas[(-150):]
    def verificar_colisiones(self):
        for estrella in self.estrellas[:]:
            if self.cohete.rect.colliderect(estrella.rect):
                multiplicador = self.cohete.multiplicador
                if estrella.especial:
                    self.puntuacion_total += 100 * multiplicador
                else:
                    self.puntuacion_total += 25 * multiplicador
                colores = [(255, 0, 255), (255, 102, 255), (255, 170, 0), (255, 255, 0), (0, 255, 255), (255, 20, 147), (0, 255, 127)]
                for _ in range(15):
                    self.particulas.append(Particula(estrella.x, estrella.y, random.choice(colores), True))
                self.combo_actual += 1
                self.tiempo_combo = 60
                self.estrellas.remove(estrella)
                sonido.play_estrella()
        for potenciador in self.potenciadores[:]:
            if self.cohete.rect.colliderect(potenciador.rect):
                if potenciador.tipo == 'escudo':
                    self.cohete.escudo = 300
                else:
                    if potenciador.tipo == 'slowmo':
                        self.cohete.turbo = 180
                    else:
                        if potenciador.tipo == 'vida':
                            self.cohete.vidas = min(5, self.cohete.vidas + 1)
                        else:
                            if potenciador.tipo == 'multi':
                                self.cohete.multiplicador = 2
                                self.cohete.puntuacion_combo = 180
                for _ in range(10):
                    self.particulas.append(Particula(potenciador.x, potenciador.y, (0, 255, 0), True))
                self.potenciadores.remove(potenciador)
                sonido.play_powerup()
                self.puntuacion_total += 50
        for meteorito in self.meteoritos[:]:
            if self.cohete.invulnerable == 0 and self.cohete.rect.colliderect(meteorito.rect):
                if self.cohete.escudo > 0:
                    for _ in range(12):
                        self.particulas.append(Particula(meteorito.x, meteorito.y, (0, 200, 255), True))
                    self.meteoritos.remove(meteorito)
                    sonido.play_escudo()
                else:
                    self.cohete.vidas -= 1
                    self.cohete.invulnerable = 90
                    self.combo_actual = 0
                    sonido.play_golpe()
                    for _ in range(18):
                        self.particulas.append(Particula(self.cohete.x, self.cohete.y, (255, 50, 0), True))
                    if self.cohete.vidas <= 0:
                        self.juego_terminado = True
                        sonido.play_gameover()
                        self.tiempo_final = pygame.time.get_ticks()
                        self.nivel_altermino = self.nivel - 1
                        tiempo_partida = max(0, self.tiempo_final - self.tiempo_inicio)
                        agregar_puntuacion_temporal(self.nombre_jugador, self.puntuacion_total, self.nivel_altermino, tiempo_partida)
                        agregar_puntuacion(self.nombre_jugador, self.puntuacion_total, self.nivel_altermino, tiempo_partida)
                        self.puntuacion_guardada = True
                        sonido.detener_musica()
                        sonido.iniciar_ambiente()
                        if not hasattr(self, '_registro_temporal_cache'):
                            self._registro_temporal_cache = cargar_registro_temporal() or []
                        entry_actual = {'nombre': self.nombre_jugador, 'puntos': self.puntuacion_total, 'nivel': self.nivel_altermino, 'tiempo': tiempo_partida}
                        if not any((e.get('nombre') == entry_actual['nombre'] and e.get('puntos') == entry_actual['puntos'] for e in self._registro_temporal_cache)):
                            self._registro_temporal_cache.append(entry_actual)
                            self._registro_temporal_cache = sorted(self._registro_temporal_cache, key=lambda x: x['puntos'], reverse=True)
                    else:
                        self.cohete.x = ANCHO // 2
                        self.cohete.y = ALTO // 2
    def actualizar(self, teclas):
        if self.pausado or self.juego_terminado or self.menu:
            return None
        else:
            if self.mostrando_constelacion:
                if pygame.time.get_ticks() - self.tiempo_inicio_pausa >= 3000:
                    self.mostrando_constelacion = False
                    self.nueva_constelacion()
                return None
            else:
                self.cohete.mover(teclas)
                self.tiempo_nivel -= 1
                if self.tiempo_nivel <= 0:
                    self.modo_furia = True
                if hasattr(self, 'modo_furia') and self.modo_furia:
                        for meteorito in self.meteoritos:
                            meteorito.vx *= 1.02
                            meteorito.vy *= 1.02
                            meteorito.tamano_rojo = True
                        if random.random() < 0.2:
                            self.meteoritos.append(Meteorito(self, self.nivel))
                if self.combo_actual > 0:
                    self.tiempo_combo -= 1
                    if self.tiempo_combo <= 0:
                        self.combo_actual = 0
                if self.cohete.puntuacion_combo > 0:
                    self.cohete.puntuacion_combo -= 1
                    if self.cohete.puntuacion_combo <= 0:
                        self.cohete.multiplicador = 1
                prob_meteorito = min(0.015 + (self.nivel - 1) * 0.025, 0.18)
                if random.random() < prob_meteorito:
                    self.meteoritos.append(Meteorito(self, self.nivel))
                for meteorito in self.meteoritos[:]:
                    meteorito.actualizar()
                    if meteorito.x < (-50) or meteorito.x > ANCHO + 50 or meteorito.y < (-50) or (meteorito.y > ALTO + 50):
                        self.meteoritos.remove(meteorito)
                prob_potenciador = max(0.006 - (self.nivel - 1) * 0.0005, 0.003)
                if random.random() < prob_potenciador:
                    x = random.randint(50, ANCHO - 50)
                    y = random.randint(100, ALTO - 50)
                    self.potenciadores.append(Potenciador(x, y))
                for potenciador in self.potenciadores[:]:
                    potenciador.tiempo -= 1
                    if potenciador.tiempo <= 0:
                        self.potenciadores.remove(potenciador)
                for particula in self.particulas[:]:
                    particula.actualizar()
                    if particula.vida <= 0:
                        self.particulas.remove(particula)
                self.verificar_colisiones()
                self.cap_particulas()
                if len(self.estrellas) == 0:
                    if not self.mostrando_constelacion:
                        self.mostrando_constelacion = True
                        self.tiempo_inicio_pausa = pygame.time.get_ticks()
                        self.constelacion_mostrada = self.constelacion_actual
                        self.color_en_pausa = COLORES.get(self.constelacion_actual, (255, 255, 0))
                        sonido.play_constelacion()
                        self.puntuacion_total += self.puntos
                        self.meteoritos.clear()
                        self.puntos = 0
    def dibujar_fondo(self, superficie):
        superficie.fill(NEGRO)
        for nebulosa in self.nebulosas:
            pygame.draw.circle(superficie, nebulosa[3], (nebulosa[0], nebulosa[1]), nebulosa[2])
        for estrella in self.fondo_estrellas:
            estrella[4] += 0.02
            brillo = int(127 + 127 * math.sin(estrella[4]))
            color = list(estrella[2])
            color = tuple((min(255, c + brillo // 4) for c in color))
            if estrella[1] < ALTO + 5:
                pygame.draw.circle(superficie, color, (estrella[0], estrella[1]), estrella[3])
    def dibujar(self, superficie):
        self.dibujar_fondo(superficie)
        for meteorito in self.meteoritos:
            meteorito.dibujar(superficie)
        for potenciador in self.potenciadores:
            potenciador.dibujar(superficie)
        for estrella in self.estrellas:
            estrella.dibujar(superficie)
        for i in range(len(self.estrellas) - 1):
            pygame.draw.line(superficie, COLORES.get(self.constelacion_actual, (255, 255, 0)), (self.estrellas[i].x, self.estrellas[i].y), (self.estrellas[i + 1].x, self.estrellas[i + 1].y), 2)
        for particula in self.particulas:
            particula.dibujar(superficie)
        self.cohete.dibujar(superficie)
        fuente = obtener_fuente(36)
        fuente_peque = obtener_fuente(24)
        if self.constelacion_actual:
            const_texto = fuente_peque.render(f'Constelacion: {self.constelacion_actual}', True, (255, 255, 255))
            superficie.blit(const_texto, (ANCHO // 2 - const_texto.get_width() // 2, 15))
        pts = fuente.render(f'Puntos: {self.puntuacion_total}', True, (255, 0, 255))
        superficie.blit(pts, (20, ALTO - 55))
        rest = fuente.render(f'Restantes: {len(self.estrellas)}', True, (255, 255, 0))
        superficie.blit(rest, (ANCHO - 170, ALTO - 55))
        segundos = max(0, self.tiempo_nivel // 60)
        completar_texto = fuente_peque.render('Complete el nivel', True, (255, 255, 255))
        superficie.blit(completar_texto, (ANCHO - 165, ALTO - 115))
        tiempo_texto = fuente.render(f'Tiempo: {segundos}', True, (255, 100, 100) if self.tiempo_nivel < 600 else (255, 255, 255))
        superficie.blit(tiempo_texto, (ANCHO - 160, ALTO - 90))
        rect_vidas_x = 10
        rect_vidas_y = ALTO - 115
        rect_vidas_w = 160
        rect_vidas_h = 50
        pygame.draw.rect(superficie, (10, 5, 15), (rect_vidas_x, rect_vidas_y, rect_vidas_w, rect_vidas_h), 0, 8)
        pygame.draw.rect(superficie, (220, 100, 100), (rect_vidas_x, rect_vidas_y, rect_vidas_w, rect_vidas_h), 2, 8)
        fuente_vidas = obtener_fuente(24)
        texto_vidas = fuente_vidas.render('VIDAS', True, (255, 200, 200))
        superficie.blit(texto_vidas, (rect_vidas_x + 52, rect_vidas_y + 6))
        corazon_centro_x = rect_vidas_x + rect_vidas_w // 2
        corazon_inicio_x = corazon_centro_x - (self.cohete.vidas - 1) * 28 // 2 if self.cohete.vidas > 0 else corazon_centro_x
        for i in range(self.cohete.vidas):
            cx = corazon_inicio_x + i * 28
            cy = rect_vidas_y + 32
            pygame.draw.circle(superficie, (220, 50, 50), (cx - 6, cy), 8)
            pygame.draw.circle(superficie, (220, 50, 50), (cx + 6, cy), 8)
            pygame.draw.polygon(superficie, (220, 50, 50), [(cx - 10, cy + 6), (cx, cy + 14), (cx + 10, cy + 6)])
            pygame.draw.polygon(superficie, (255, 100, 100), [(cx - 5, cy + 3), (cx, cy + 9), (cx + 5, cy + 3)])
        if self.combo_actual >= 3:
            combo_texto = fuente.render(f'COMBO x{self.combo_actual}!', True, (255, 200, 0))
            superficie.blit(combo_texto, (ANCHO // 2 - combo_texto.get_width() // 2, ALTO - 80))
        if self.mostrando_constelacion and self.constelacion_mostrada:
                tiempo = pygame.time.get_ticks()
                color = COLORES.get(self.constelacion_mostrada, (255, 255, 0))
                overlay = self._overlay_constelacion
                superficie.blit(overlay, (0, 0))
                for i in range(5):
                    x = random.randint(0, ANCHO)
                    y = random.randint(0, ALTO)
                    brillo = int(100 + 100 * math.sin(tiempo * 0.003 + i))
                    pygame.draw.circle(superficie, (brillo // 3, brillo // 3, brillo // 2 + 30), (x, y), random.randint(1, 2))
                emoji = EMOJIS_CONSTELACIONES.get(self.constelacion_mostrada, '✨')
                pygame.draw.circle(superficie, (30, 10, 50), (150, 180), 100, 3)
                render_emoji(superficie, emoji, 150, 180, 72)
                pygame.draw.circle(superficie, (30, 10, 50), (ANCHO - 150, 180), 100, 3)
                render_emoji(superficie, emoji, ANCHO - 150, 180, 72)
                titulo = obtener_fuente(56).render(self.constelacion_mostrada, True, (255, 255, 255))
                superficie.blit(titulo, (ANCHO // 2 - titulo.get_width() // 2, 25))
                titulo_brillo = obtener_fuente(56).render(self.constelacion_mostrada, True, color)
                superficie.blit(titulo_brillo, (ANCHO // 2 - titulo.get_width() // 2 + 2, 27))
                pygame.draw.line(superficie, color, (ANCHO // 2 - 130, 60), (ANCHO // 2 - 50, 60), 2)
                pygame.draw.line(superficie, color, (ANCHO // 2 + 50, 60), (ANCHO // 2 + 130, 60), 2)
                mensaje = obtener_fuente(26).render(f'¡CONSTELACION COMPLETADA! - NIVEL {self.nivel - 1}', True, (255, 220, 100))
                superficie.blit(mensaje, (ANCHO // 2 - mensaje.get_width() // 2, ALTO - 80))
                puntos_msg = obtener_fuente(22).render(f'Puntos: {self.puntuacion_total}', True, (255, 200, 255))
                superficie.blit(puntos_msg, (ANCHO // 2 - puntos_msg.get_width() // 2, ALTO - 55))
                posiciones = constelaciones.get(self.constelacion_mostrada, [])
                escala = 3.0
                centro_x = ANCHO // 2
                centro_y = ALTO // 2
                for pos in posiciones:
                    x = pos[0] * escala + centro_x
                    y = pos[1] * escala + centro_y
                    pygame.draw.circle(superficie, (255, 255, 255), (int(x), int(y)), 14)
                    pygame.draw.circle(superficie, color, (int(x), int(y)), 10)
                    radio_brillo = 6 + math.sin(tiempo * 0.01) * 2
                    pygame.draw.circle(superficie, (255, 255, 255), (int(x), int(y)), int(radio_brillo))
                for i in range(len(posiciones) - 1):
                    x1 = posiciones[i][0] * escala + centro_x
                    y1 = posiciones[i][1] * escala + centro_y
                    x2 = posiciones[i + 1][0] * escala + centro_x
                    y2 = posiciones[i + 1][1] * escala + centro_y
                    pygame.draw.line(superficie, color, (int(x1), int(y1)), (int(x2), int(y2)), 4)
        if self.juego_terminado:
            overlay = self._overlay_gameover
            superficie.blit(overlay, (0, 0))
            titre = obtener_fuente(56).render('JUEGO TERMINADO', True, (255, 50, 50))
            superficie.blit(titre, (ANCHO // 2 - titre.get_width() // 2, 60))
            pts_final = obtener_fuente(44).render(f'Puntuacion: {self.puntuacion_total}', True, (255, 255, 0))
            superficie.blit(pts_final, (ANCHO // 2 - pts_final.get_width() // 2, 130))
            nivel_logro = fuente_peque.render(f'Nivel: {self.nivel_altermino}', True, (150, 200, 255))
            superficie.blit(nivel_logro, (ANCHO // 2 - nivel_logro.get_width() // 2, 185))
            tiempo_juego = max(0, self.tiempo_final - self.tiempo_inicio)
            minutos = tiempo_juego // 60000
            segundos = tiempo_juego % 60000 // 1000
            tiempo_str = f'{minutos}:{segundos:02d}'
            tiempo_display = fuente_peque.render(f'Tiempo: {tiempo_str}', True, (200, 200, 100))
            superficie.blit(tiempo_display, (ANCHO // 2 - tiempo_display.get_width() // 2, 215))
            pygame.draw.line(superficie, (100, 100, 150), (ANCHO // 2 - 200, 255), (ANCHO // 2 + 200, 255), 2)
            top_label = fuente.render('TOP PUNTUACIONES', True, (255, 200, 0))
            superficie.blit(top_label, (ANCHO // 2 - top_label.get_width() // 2, 280))
            registro = self._registro_temporal_cache or cargar_registro_temporal() or []
            entry_actual = {'nombre': self.nombre_jugador, 'puntos': self.puntuacion_total, 'nivel': self.nivel_altermino, 'tiempo': max(0, self.tiempo_final - self.tiempo_inicio)}
            if not any((e.get('nombre') == entry_actual['nombre'] and e.get('puntos') == entry_actual['puntos'] for e in registro)):
                registro.append(entry_actual)
                registro = sorted(registro, key=lambda x: x['puntos'], reverse=True)
            fuente_top_gameover = obtener_fuente(28)
            cx = ANCHO // 2
            colores_top = [(255, 50, 50), (255, 100, 50), (255, 150, 50), (255, 200, 100), (255, 220, 150)]
            for i, entry in enumerate(registro):
                if i < 5:
                    c = colores_top[i]
                else:
                    if entry['nombre'] == self.nombre_jugador and entry['puntos'] == self.puntuacion_total:
                        c = (255, 255, 150)
                    else:
                        c = (180, 180, 180)
                tiempo_val = entry.get('tiempo', entry.get('fecha', 0))
                minutos_t = int(tiempo_val) // 60000
                segundos_t = int(tiempo_val) % 60000 // 1000
                tiempo_fmt = f'{minutos_t}:{segundos_t:02d}'
                y = 320 + i * 30
                rank_txt = fuente_top_gameover.render(f'{i + 1}.', True, c)
                nombre_txt = fuente_top_gameover.render(entry['nombre'][:12], True, c)
                pts_txt = fuente_top_gameover.render(f"{entry['puntos']} pts", True, c)
                nivel_txt = fuente_top_gameover.render(f"Nv {entry.get('nivel', 1)}", True, c)
                tiempo_txt = fuente_top_gameover.render(tiempo_fmt, True, c)
                superficie.blit(rank_txt, (cx - 250, y))
                superficie.blit(nombre_txt, (cx - 200, y))
                superficie.blit(pts_txt, (cx - 20, y))
                superficie.blit(nivel_txt, (cx + 80, y))
                superficie.blit(tiempo_txt, (cx + 170, y))
            reinicio = fuente_peque.render('Presiona ESPACIO para reiniciar', True, (255, 255, 255))
            superficie.blit(reinicio, (ANCHO // 2 - reinicio.get_width() // 2, ALTO - 40))
        if self.menu and self.logueando:
            superficie.fill(NEGRO)
            tiempo_actual = pygame.time.get_ticks()
            for nebulosa in self.nebulosas[:5]:
                pygame.draw.circle(superficie, nebulosa[3], (nebulosa[0] // 3, nebulosa[1] // 3), nebulosa[2] // 3)
            for ast in self.asteroides_menu:
                ast.actualizar()
                ast.dibujar(superficie)
                if ast.x < (-150) or ast.x > ANCHO + 150 or ast.y < (-150) or (ast.y > ALTO + 150):
                    self.asteroides_menu.remove(ast)
                    self.asteroides_menu.append(Asteroid(desde_menu=True))
            fase_color = math.sin(tiempo_actual * 0.004)
            r = 255
            g = max(80, min(180, int(130 + 50 * fase_color)))
            b = max(30, min(100, int(65 + 35 * fase_color)))
            offset_y = int(8 * math.sin(tiempo_actual * 0.003))
            for glow in [12, 8, 5]:
                color_glow = (max(0, min(255, r // 3 + glow * 5)), max(0, min(255, g // 3 + glow * 5)), max(0, min(255, b // 3 + glow * 5)))
                titulo_glow = obtener_fuente(90).render('¡BOOM CÓSMICO!', True, color_glow)
                superficie.blit(titulo_glow, (ANCHO // 2 - titulo_glow.get_width() // 2, 55 + offset_y + glow))
            titulo = obtener_fuente(85).render('¡BOOM CÓSMICO!', True, (r, g, b))
            superficie.blit(titulo, (ANCHO // 2 - titulo.get_width() // 2, 55 + offset_y))
            titulo_brillo = obtener_fuente(85).render('¡BOOM CÓSMICO!', True, (255, 220, 150))
            superficie.blit(titulo_brillo, (ANCHO // 2 - titulo_brillo.get_width() // 2 + 2, 57 + offset_y))
            ciclo_sub = math.sin(tiempo_actual * 0.002)
            color_sub = (150 + int(20 * ciclo_sub), 200 + int(20 * ciclo_sub), 255)
            subtitulo = obtener_fuente(36).render('Sobrevive, explora y conquista el universo', True, color_sub)
            superficie.blit(subtitulo, (ANCHO // 2 - subtitulo.get_width() // 2, 130))
            nombre_label = fuente.render('Ingresa tu nombre:', True, (200, 200, 255))
            superficie.blit(nombre_label, (ANCHO // 2 - nombre_label.get_width() // 2, 240))
            nombre_input = obtener_fuente(44).render(self.nombre_jugador + '_', True, (255, 255, 255))
            superficie.blit(nombre_input, (ANCHO // 2 - nombre_input.get_width() // 2, 290))
            pygame.draw.rect(superficie, (100, 100, 150), (ANCHO // 2 - 140, 275, 280, 45), 2)
            if self.error_nombre:
                error_texto = fuente_peque.render(self.error_nombre, True, (255, 50, 50))
                superficie.blit(error_texto, (ANCHO // 2 - error_texto.get_width() // 2, 330))
            if len(self.nombre_jugador) > 0:
                iniciar = fuente.render('Presiona ENTER para comenzar', True, (0, 255, 255))
                superficie.blit(iniciar, (ANCHO // 2 - iniciar.get_width() // 2, 380))
            else:
                iniciar = fuente_peque.render('Escribe tu nombre (min 3 letras) y presiona ENTER', True, (150, 150, 150))
                superficie.blit(iniciar, (ANCHO // 2 - iniciar.get_width() // 2, 380))
            registro = cargar_registro()
            if registro:
                fuente_top = obtener_fuente(28)
                top_label = fuente_top.render('Top de Puntuaciones Históricas', True, (255, 200, 100))
                superficie.blit(top_label, (ANCHO // 2 - top_label.get_width() // 2, 440))
                cx = ANCHO // 2
                colores_top = [(255, 50, 50), (255, 100, 50), (255, 150, 50), (255, 200, 100), (255, 220, 150)]
                for i, entry in enumerate(registro[:5]):
                    tiempo_val = entry.get('tiempo', entry.get('fecha', 0))
                    minutos = int(tiempo_val) // 60000
                    segundos = int(tiempo_val) % 60000 // 1000
                    tiempo_fmt = f'{minutos}:{segundos:02d}'
                    y = 475 + i * 30
                    c = colores_top[i]
                    rank_txt = fuente_top.render(f'{i + 1}.', True, c)
                    nombre_txt = fuente_top.render(entry['nombre'][:12], True, c)
                    pts_txt = fuente_top.render(f"{entry['puntos']} pts", True, c)
                    nivel_txt = fuente_top.render(f"Nv {entry.get('nivel', 1)} - {tiempo_fmt}", True, c)
                    superficie.blit(rank_txt, (cx - 220, y))
                    superficie.blit(nombre_txt, (cx - 170, y))
                    superficie.blit(pts_txt, (cx - 10, y))
                    superficie.blit(nivel_txt, (cx + 110, y))
            creado = fuente_peque.render('Hecho por Benja Basiluk.', True, (100, 100, 100))
            superficie.blit(creado, (ANCHO // 2 - creado.get_width() // 2, 650))
            fuente_escuela = obtener_fuente(30)
            escuela = fuente_escuela.render('Escuela Superior', True, (100, 200, 255))
            superficie.blit(escuela, (30, 680))
            nacional1 = fuente_escuela.render('El Na', True, (255, 255, 255))
            nacional2 = fuente_escuela.render('cio', True, (255, 255, 0))
            nacional3 = fuente_escuela.render('nal', True, (255, 255, 255))
            superficie.blit(nacional1, (30, 710))
            superficie.blit(nacional2, (30 + nacional1.get_width(), 710))
            superficie.blit(nacional3, (30 + nacional1.get_width() + nacional2.get_width(), 710))
            desarrollo = fuente_escuela.render('Desarrollo de Software', True, (100, 200, 255))
            superficie.blit(desarrollo, (30, 740))
        else:
            if self.menu:
                superficie.fill(NEGRO)
                tiempo_actual = pygame.time.get_ticks()
                for nebulosa in self.nebulosas[:5]:
                    pygame.draw.circle(superficie, nebulosa[3], (nebulosa[0] // 3, nebulosa[1] // 3), nebulosa[2] // 3)
                for ast in self.asteroides_menu:
                    ast.actualizar()
                    ast.dibujar(superficie)
                    if ast.x < (-150) or ast.x > ANCHO + 150 or ast.y < (-150) or (ast.y > ALTO + 150):
                        self.asteroides_menu.remove(ast)
                        self.asteroides_menu.append(Asteroid(desde_menu=True))
                fase_color = math.sin(tiempo_actual * 0.004)
                r = 255
                g = max(80, min(180, int(130 + 50 * fase_color)))
                b = max(30, min(100, int(65 + 35 * fase_color)))
                offset_y = int(8 * math.sin(tiempo_actual * 0.003))
                for glow in [12, 8, 5]:
                    color_glow = (max(0, min(255, r // 3 + glow * 5)), max(0, min(255, g // 3 + glow * 5)), max(0, min(255, b // 3 + glow * 5)))
                    titulo_glow = obtener_fuente(90).render('¡BOOM CÓSMICO!', True, color_glow)
                    superficie.blit(titulo_glow, (ANCHO // 2 - titulo_glow.get_width() // 2, 55 + offset_y + glow))
                titulo = obtener_fuente(85).render('¡BOOM CÓSMICO!', True, (r, g, b))
                superficie.blit(titulo, (ANCHO // 2 - titulo.get_width() // 2, 55 + offset_y))
                titulo_brillo = obtener_fuente(85).render('¡BOOM CÓSMICO!', True, (255, 220, 150))
                superficie.blit(titulo_brillo, (ANCHO // 2 - titulo_brillo.get_width() // 2 + 2, 57 + offset_y))
                ciclo_sub = math.sin(tiempo_actual * 0.002)
                color_sub = (150 + int(20 * ciclo_sub), 200 + int(20 * ciclo_sub), 255)
                subtitulo = obtener_fuente(32).render('Sobrevive, explora y conquista el universo', True, color_sub)
                superficie.blit(subtitulo, (ANCHO // 2 - subtitulo.get_width() // 2, 130))
                if sprite_flechas:
                    sw, sh = (sprite_flechas.get_width(), sprite_flechas.get_height())
                    superficie.blit(sprite_flechas, (ANCHO // 2 - sw // 2, 250))
                else:
                    pygame.draw.rect(superficie, (50, 50, 80), (ANCHO // 2 - 40, 260, 80, 80), 3)
                    pygame.draw.polygon(superficie, (100, 200, 255), [(ANCHO // 2, 265), (ANCHO // 2 - 15, 285), (ANCHO // 2 + 15, 285)])
                    pygame.draw.polygon(superficie, (100, 200, 255), [(ANCHO // 2, 335), (ANCHO // 2 - 15, 315), (ANCHO // 2 + 15, 315)])
                    pygame.draw.polygon(superficie, (100, 200, 255), [(ANCHO // 2 - 25, 300), (ANCHO // 2 - 5, 300), (ANCHO // 2 - 15, 285)])
                    pygame.draw.polygon(superficie, (100, 200, 255), [(ANCHO // 2 + 25, 300), (ANCHO // 2 + 5, 300), (ANCHO // 2 + 15, 285)])
                instru = fuente.render('MOVER con flechas del teclado', True, (150, 220, 255))
                superficie.blit(instru, (ANCHO // 2 - instru.get_width() // 2, 410))
                pygame.draw.rect(superficie, (30, 30, 50), (ANCHO // 2 - 280, 445, 560, 45), 2, 10)
                x_base = ANCHO // 2 - 200
                for r in range(18, 10, (-4)):
                    pygame.draw.circle(superficie, (0, 150, 255), (x_base, 467), r)
                pygame.draw.circle(superficie, (255, 255, 255), (x_base, 467), 7)
                t_escudo = obtener_fuente(28).render('E', True, (0, 0, 0))
                superficie.blit(t_escudo, (x_base - 8, 456))
                nombre_escudo = fuente_peque.render('Escudo', True, (150, 200, 255))
                superficie.blit(nombre_escudo, (x_base - nombre_escudo.get_width() // 2, 495))
                x_base = ANCHO // 2 - 60
                for r in range(18, 10, (-4)):
                    pygame.draw.circle(superficie, (100, 100, 255), (x_base, 467), r)
                pygame.draw.circle(superficie, (255, 255, 255), (x_base, 467), 7)
                t_slow = obtener_fuente(28).render('S', True, (0, 0, 0))
                superficie.blit(t_slow, (x_base - 8, 456))
                nombre_slow = fuente_peque.render('Slow', True, (150, 150, 255))
                superficie.blit(nombre_slow, (x_base - nombre_slow.get_width() // 2, 495))
                x_base = ANCHO // 2 + 80
                for r in range(18, 10, (-4)):
                    pygame.draw.circle(superficie, (0, 200, 50), (x_base, 467), r)
                pygame.draw.circle(superficie, (255, 255, 255), (x_base, 467), 7)
                t_vida = obtener_fuente(28).render('V', True, (0, 0, 0))
                superficie.blit(t_vida, (x_base - 8, 456))
                nombre_vida = fuente_peque.render('Vida', True, (150, 255, 150))
                superficie.blit(nombre_vida, (x_base - nombre_vida.get_width() // 2, 495))
                x_base = ANCHO // 2 + 220
                for r in range(18, 10, (-4)):
                    pygame.draw.circle(superficie, (200, 0, 200), (x_base, 467), r)
                pygame.draw.circle(superficie, (255, 255, 255), (x_base, 467), 7)
                t_multi = obtener_fuente(28).render('M', True, (0, 0, 0))
                superficie.blit(t_multi, (x_base - 8, 456))
                nombre_multi = fuente_peque.render('Multi', True, (255, 150, 255))
                superficie.blit(nombre_multi, (x_base - nombre_multi.get_width() // 2, 495))
                iniciar = fuente.render('Presiona ESPACIO para comenzar', True, (0, 255, 255))
                superficie.blit(iniciar, (ANCHO // 2 - iniciar.get_width() // 2, 530))
                creado = fuente_peque.render('Hecho por Benja Basiluk.', True, (100, 100, 100))
                superficie.blit(creado, (ANCHO // 2 - creado.get_width() // 2, 590))
                fuente_escuela = obtener_fuente(30)
                escuela = fuente_escuela.render('Escuela Superior', True, (100, 200, 255))
                superficie.blit(escuela, (30, 620))
                nacional1 = fuente_escuela.render('El Na', True, (255, 255, 255))
                nacional2 = fuente_escuela.render('cio', True, (255, 255, 0))
                nacional3 = fuente_escuela.render('nal', True, (255, 255, 255))
                superficie.blit(nacional1, (30, 650))
                superficie.blit(nacional2, (30 + nacional1.get_width(), 650))
                superficie.blit(nacional3, (30 + nacional1.get_width() + nacional2.get_width(), 650))
                desarrollo = fuente_escuela.render('Desarrollo de Software', True, (100, 200, 255))
                superficie.blit(desarrollo, (30, 680))
def main():
    juego = Juego()
    sonido.iniciar_ambiente()
    ejecutando = True
    while ejecutando:
        reloj.tick(60)
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                sonido.detener_ambiente()
                if os.path.exists(ARCHIVO_REGISTRO_TEMP):
                    os.remove(ARCHIVO_REGISTRO_TEMP)
                ejecutando = False
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:
                    sonido.detener_ambiente()
                    if os.path.exists(ARCHIVO_REGISTRO_TEMP):
                        os.remove(ARCHIVO_REGISTRO_TEMP)
                    ejecutando = False
                if juego.logueando and juego.menu:
                    if evento.key == pygame.K_BACKSPACE:
                        juego.nombre_jugador = juego.nombre_jugador[:(-1)]
                        juego.error_nombre = None
                    else:
                        if evento.key == pygame.K_RETURN:
                            if len(juego.nombre_jugador.strip()) >= 3:
                                if nombre_en_top(juego.nombre_jugador.strip(), getattr(juego, '_registro_temporal_cache', None)):
                                    juego.error_nombre = 'Nombre ya en uso'
                                else:
                                    juego.logueando = False
                        else:
                            if evento.unicode.isalnum() or evento.unicode in ['_', '-']:
                                if len(juego.nombre_jugador) < 15:
                                    juego.nombre_jugador += evento.unicode
                                    juego.error_nombre = None
                else:
                    if evento.key == pygame.K_SPACE:
                        if juego.menu:
                            juego.menu = False
                            sonido.detener_ambiente()
                            sonido.iniciar_musica()
                        else:
                            if juego.juego_terminado:
                                juego.__init__()
                                sonido.iniciar_ambiente()
                                juego.error_nombre = None
                                if hasattr(juego, 'puntuacion_guardada'):
                                    delattr(juego, 'puntuacion_guardada')
                if evento.key == pygame.K_p:
                    if not juego.menu and (not juego.juego_terminado):
                            juego.pausado = not juego.pausado
        teclas = pygame.key.get_pressed()
        juego.actualizar(teclas)
        juego.dibujar(pantalla)
        if juego.pausado:
            pausa = obtener_fuente(48).render('PAUSADO', True, (255, 255, 0))
            pantalla.blit(pausa, (ANCHO // 2 - pausa.get_width() // 2, ALTO // 2))
        pygame.display.flip()
    pygame.quit()
    sys.exit()
if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        print(f'Error: {e}')
        pygame.quit()
        sys.exit()