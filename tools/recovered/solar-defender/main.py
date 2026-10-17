# Decompiled with PyLingual (https://pylingual.io)
# Internal filename: 'main.py'
# Bytecode version: 3.10.b1 (3439)
# Source timestamp: 1970-01-01 00:00:00 UTC (0)

global game_slow_active
import pygame
import random
import math
import os
import sys
WIDTH, HEIGHT = (1280, 720)
FPS = 30
WHITE = (255, 255, 255)
YELLOW = (255, 255, 50)
RED = (255, 80, 80)
GREEN = (80, 255, 80)
BLUE = (80, 150, 255)
CYAN = (50, 255, 255)
ORANGE = (255, 180, 50)
PURPLE = (200, 100, 255)
GRAY = (180, 180, 200)
DARK_GRAY = (60, 60, 80)
BLACK = (10, 10, 30)
PINK = (255, 150, 200)
GOLD = (255, 215, 0)
pygame.init()
pygame.mixer.init(frequency=44100, size=(-16), channels=2, buffer=512)
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN | pygame.HWSURFACE | pygame.DOUBLEBUF)
pygame.display.set_caption('Solar Defender - Earth Edition')
pygame.mouse.set_visible(True)
clock = pygame.time.Clock()
FONT = pygame.font.SysFont('consolas', 16, bold=True)
TITLE_FONT = pygame.font.SysFont('consolas', 48, bold=True)
BIG_TITLE = pygame.font.SysFont('impact', 72, bold=True)
CREDIT_FONT = pygame.font.SysFont('impact', 20, bold=False)
SMALL_FONT = pygame.font.SysFont('consolas', 13, bold=False)
print('CWD:', os.getcwd())
print('Script:', sys.argv[0])
if getattr(sys, 'frozen', False):
    script_dir = sys._MEIPASS
else:
    script_dir = os.path.dirname(os.path.abspath(sys.argv[0]))
ASSETS_PATH = os.path.join(script_dir, 'assets', 'spacegame_asset_pack')
print('Assets path:', ASSETS_PATH)
print('Path exists:', os.path.exists(ASSETS_PATH))
def load_asteroids():
    asteroids = {}
    for i in range(1, 6):
        try:
            path = os.path.join(ASSETS_PATH, f'asteroid_{i}.png')
            if os.path.exists(path):
                img = pygame.image.load(path).convert_alpha()
                asteroids[i] = pygame.transform.scale(img, (64, 64))
                print(f'Asteroid {i} loaded')
            else:
                print(f'Asteroid {i} NOT FOUND at {path}')
                asteroids[i] = None
        except Exception as e:
            print(f'Error asteroid {i}: {e}')
            asteroids[i] = None
    return asteroids
def load_planets():
    planets = {}
    for i in range(1, 8):
        try:
            path = os.path.join(ASSETS_PATH, f'planet_{i}.png')
            if os.path.exists(path):
                img = pygame.image.load(path).convert_alpha()
                planets[i] = pygame.transform.scale(img, (150, 150))
                print(f'Planet {i} loaded')
            else:
                planets[i] = None
        except:
            planets[i] = None
    return planets
def load_player_ships():
    ships = {}
    for i in range(1, 3):
        try:
            path = os.path.join(ASSETS_PATH, f'player_spaceship_{i}.png')
            if os.path.exists(path):
                img = pygame.image.load(path).convert_alpha()
                frame_w = img.get_width() // 7
                frame = img.subsurface((0, 0, frame_w, img.get_height()))
                ships[i] = pygame.transform.scale(frame, (60, 70))
                print(f'SHIP {i} loaded! Size: {ships[i].get_size()}')
            else:
                print(f'SHIP {i} NOT FOUND: {path}')
                ships[i] = None
        except Exception as e:
            print(f'SHIP {i} ERROR: {e}')
            ships[i] = None
    return ships
def load_enemy_ships():
    ships = {}
    for i in range(1, 8):
        try:
            path = os.path.join(ASSETS_PATH, f'enemy_spaceship_{i}.png')
            if os.path.exists(path):
                img = pygame.image.load(path).convert_alpha()
                frame_w = img.get_width() // 7
                frame = img.subsurface((0, 0, frame_w, img.get_height()))
                ships[i] = pygame.transform.scale(frame, (60, 70))
                print(f'ENEMY SHIP {i} loaded! Size: {ships[i].get_size()}')
            else:
                print(f'ENEMY SHIP {i} NOT FOUND: {path}')
                ships[i] = None
        except Exception as e:
            print(f'ENEMY SHIP {i} ERROR: {e}')
            ships[i] = None
    return ships
ENEMY_TYPE_SHIP = {'fast': 1, 'tank': 5, 'shooter': 4, 'asteroid': None}
print('Loading assets...')
ASTEROID_SPRITES = load_asteroids()
PLANET_SPRITES = load_planets()
PLAYER_SHIPS = load_player_ships()
ENEMY_SHIPS = load_enemy_ships()
print('ENEMY_SHIPS loaded:', {k: 'OK' if v else 'FAIL' for k, v in ENEMY_SHIPS.items()})
VOID_PATH = os.path.join(script_dir, 'assets', 'Foozle_2DS0015_Void_EnvironmentPack')
def load_void_earth():
    try:
        path = os.path.join(VOID_PATH, 'Planets', 'PNGs', 'Earth-Like planet.png')
        if os.path.exists(path):
            img = pygame.image.load(path).convert_alpha()
            print(f'VOID_EARTH loaded! Size: {img.get_size()}')
            return img
    except Exception as e:
        print(f'VOID_EARTH error: {e}')
        return None
VOID_EARTH = load_void_earth()
VOID_EARTH_GAME = None
if VOID_EARTH:
    fw = VOID_EARTH.get_width() // 77
    VOID_EARTH_GAME = pygame.transform.scale(VOID_EARTH.subsurface((0, 0, fw, VOID_EARTH.get_height())), (300, 300))
class SoundManager:
    def __init__(self):
        self.sounds = {}
        self.enabled = True
        self.load_sounds()
    def load_sounds(self):
        sound_files = {'shoot': 'sounds/shoot.wav', 'explosion': 'sounds/explosion.wav', 'powerup': 'sounds/powerup.wav', 'menu_select': 'sounds/menu_select.wav', 'hit': 'sounds/hit.wav', 'victory': 'sounds/victory.wav', 'gameover': 'sounds/gameover.wav', 'ambient': 'sounds/ambient.wav'}
        for name, path in sound_files.items():
            try:
                if os.path.exists(path):
                    self.sounds[name] = pygame.mixer.Sound(path)
                    vol = 1.0 if name == 'ambient' else 0.5
                    self.sounds[name].set_volume(vol)
            except:
                continue
    def play(self, name):
        if not self.enabled or name not in self.sounds:
            return
        try:
            self.sounds[name].play()
        except Exception:
            pass
    def start_ambient(self):
        if self.enabled and 'ambient' in self.sounds:
                try:
                    if hasattr(self, 'ambient_channel') and self.ambient_channel and self.ambient_channel.get_busy():
                        return
                    else:
                        self.ambient_channel = pygame.mixer.find_channel()
                        if self.ambient_channel:
                            self.ambient_channel.play(self.sounds['ambient'], loops=(-1))
                            self.ambient_channel.set_volume(0.8)
                except:
                    return
    def stop_ambient(self):
        try:
            if hasattr(self, 'ambient_channel') and self.ambient_channel:
                    self.ambient_channel.stop()
        except:
            return None
sound_manager = SoundManager()
SHIPS = {'rapido': {'name': 'Velociraptor', 'color': (0, 255, 200), 'speed': 5, 'delay': 200, 'damage': 1, 'bullets': 1, 'desc': 'Rapido, liviano, versatil'}, 'potente': {'name': 'Titan', 'color': (255, 100, 50), 'speed': 5, 'delay': 240, 'damage': 3, 'bullets': 1, 'desc': 'Golpea duro, velocidad media'}, 'doble': {'name': 'Doble', 'color': (100, 150, 255), 'speed': 4.5, 'delay': 170, 'damage': 1, 'bullets': 2, 'desc': 'Dos disparos a la vez'}}
PLANETS = [{'name': 'Mercurio', 'color': (255, 160, 60), 'size': 25, 'enemies': 30}, {'name': 'Venus', 'color': (255, 200, 80), 'size': 40, 'enemies': 35}, {'name': 'Marte', 'color': (255, 80, 40), 'size': 35, 'enemies': 45}, {'name': 'Jupiter', 'color': (200, 120, 60), 'size': 55, 'enemies': 55}, {'name': 'Saturno', 'color': (200, 150, 100), 'size': 50, 'enemies': 70}]
game_slow_active = False
QUIZ_QUESTIONS = [{'q': 'El Sol es...', 'opts': ['una estrella', 'un planeta', 'una flor'], 'ans': 0}, {'q': '¿Cuál es el planeta más grande?', 'opts': ['Júpiter', 'Marte', 'La Tierra'], 'ans': 0}, {'q': '¿De qué color es Marte?', 'opts': ['Rojo', 'Azul', 'Amarillo'], 'ans': 0}, {'q': '¿Qué planeta tiene anillos?', 'opts': ['Saturno', 'Venus', 'Marte'], 'ans': 0}, {'q': '¿Cuál es el planeta más cerca del Sol?', 'opts': ['Mercurio', 'Neptuno', 'La Tierra'], 'ans': 0}, {'q': '¿Cuántos planetas hay?', 'opts': ['8', '3', '100'], 'ans': 0}, {'q': 'La Tierra gira alrededor de...', 'opts': ['el Sol', 'la Luna', 'una nube'], 'ans': 0}, {'q': '¿Cómo se llama el planeta rojo?', 'opts': ['Marte', 'Venus', 'Júpiter'], 'ans': 0}, {'q': '¿Qué vemos en el cielo de noche?', 'opts': ['La Luna', 'El Sol', 'Un arcoíris'], 'ans': 0}, {'q': '¿Dónde vivimos?', 'opts': ['En la Tierra', 'En Marte', 'En la Luna'], 'ans': 0}]
def draw_text(text, font, color, x, y, center=False):
    img = font.render(text, True, color)
    if center:
        screen.blit(img, (x - img.get_width() // 2, y - img.get_height() // 2))
    else:
        screen.blit(img, (x, y))
SHIP_SPRITE_MAP = {'rapido': 1, 'potente': 2, 'doble': 1}
def draw_ship_icon(x, y, color, ship_type, scale=1.0):
    sprite_idx = SHIP_SPRITE_MAP.get(ship_type, 1)
    ship_loaded = PLAYER_SHIPS.get(sprite_idx)
    if ship_loaded:
        try:
            ship_img = PLAYER_SHIPS[sprite_idx]
            if scale != 1.0:
                w = int(ship_img.get_width() * scale)
                h = int(ship_img.get_height() * scale)
                ship_img = pygame.transform.scale(ship_img, (w, h))
            dest_rect = ship_img.get_rect()
            dest_rect.center = (x, y)
            screen.blit(ship_img, dest_rect)
            if ship_type == 'doble':
                ghost = pygame.transform.flip(ship_img, True, False)
                ghost.set_alpha(140)
                r2 = ghost.get_rect()
                r2.center = (x + int(20 * scale), y - int(4 * scale))
                screen.blit(ghost, r2)
            return None
        except Exception as e:
            print(f'Error drawing ship: {e}')
    s = scale
    if ship_type == 'rapido':
        pygame.draw.polygon(screen, color, [(x, y - 25 * s), (x + 20 * s, y + 15 * s), (x, y + 10 * s), (x - 20 * s, y + 15 * s)])
        pygame.draw.polygon(screen, (255, 200, 100), [(x, y + 10 * s), (x - 8 * s, y + 20 * s), (x + 8 * s, y + 20 * s)])
    else:
        if ship_type == 'potente':
            pygame.draw.rect(screen, color, (x - 18 * s, y - 10 * s, 36 * s, 25 * s), border_radius=3)
            pygame.draw.polygon(screen, color, [(x, y - 25 * s), (x + 15 * s, y - 10 * s), (x - 15 * s, y - 10 * s)])
            pygame.draw.polygon(screen, (255, 150, 50), [(x - 10 * s, y + 15 * s), (x, y + 28 * s), (x + 10 * s, y + 15 * s)])
        else:
            if ship_type == 'doble':
                pygame.draw.polygon(screen, color, [(x, y - 30 * s), (x + 18 * s, y + 10 * s), (x, y + 5 * s), (x - 18 * s, y + 10 * s)])
                pygame.draw.rect(screen, color, (x - 12 * s, y - 5 * s, 8 * s, 12 * s))
                pygame.draw.rect(screen, color, (x + 4 * s, y - 5 * s, 8 * s, 12 * s))
                pygame.draw.polygon(screen, (255, 180, 80), [(x - 15 * s, y + 10 * s), (x - 15 * s, y + 20 * s), (x - 5 * s, y + 15 * s)])
                pygame.draw.polygon(screen, (255, 180, 80), [(x + 5 * s, y + 15 * s), (x + 15 * s, y + 20 * s), (x + 15 * s, y + 10 * s)])
    pygame.draw.circle(screen, (255, 255, 200), (x - 3 * s, y - 8 * s), 4 * s)
class Star:
    def __init__(self):
        self.x = random.randint(0, WIDTH)
        self.y = random.randint(0, HEIGHT)
        self.size = random.choice([1, 2])
        self.speed = random.uniform(0.5, 2)
    def move(self):
        self.y += self.speed
        if self.y > HEIGHT:
            self.y = 0
            self.x = random.randint(0, WIDTH)
    def draw(self):
        pygame.draw.rect(screen, (255, 255, 255), (self.x, int(self.y), self.size, self.size))
class Background:
    def __init__(self):
        self.stars = [Star() for _ in range(30)]
        self.bg_planets = []
        self.planet_cache = {}
        for _ in range(5):
            self.bg_planets.append({'x': random.randint(0, WIDTH), 'y': random.randint(0, HEIGHT // 2), 'size': random.randint(30, 80), 'idx': random.randint(3, 7), 'speed': random.uniform(0.3, 1.0)})
    def update(self):
        for star in self.stars:
            star.move()
        for p in self.bg_planets:
            p['y'] += p['speed']
            if p['y'] > HEIGHT + p['size']:
                p['y'] = -p['size']
                p['x'] = random.randint(0, WIDTH)
                p['idx'] = random.randint(3, 7)
                self.planet_cache.pop((p['idx'], p['size']), None)
    def draw(self):
        screen.fill(BLACK)
        for p in self.bg_planets:
            if PLANET_SPRITES.get(p['idx']):
                key = (p['idx'], p['size'])
                if key not in self.planet_cache:
                    self.planet_cache[key] = pygame.transform.scale(PLANET_SPRITES[p['idx']], (p['size'], p['size']))
                screen.blit(self.planet_cache[key], (int(p['x']), int(p['y'])))
        for star in self.stars:
            star.draw()
class SolarMenu:
    def __init__(self):
        self.center_x, self.center_y = (WIDTH // 2, HEIGHT // 2)
        self.anim = 0
        self.stars = [(random.randint(0, WIDTH), random.randint(0, HEIGHT), random.randint(1, 2)) for _ in range(50)]
        self.earth_pulse = 0
        self.planet_cache = {}
        self.bg_planets = []
        for _ in range(4):
            self.bg_planets.append({'x': random.randint(0, WIDTH), 'y': random.randint(0, HEIGHT), 'size': random.randint(40, 100), 'idx': random.randint(1, 7), 'speed': random.uniform(0.2, 0.8)})
    def update(self):
        self.anim += 1
        self.earth_pulse += 0.05
        for p in self.bg_planets:
            p['y'] += p['speed']
            if p['y'] > HEIGHT + p['size']:
                p['y'] = -p['size']
                p['x'] = random.randint(0, WIDTH)
                self.planet_cache.pop((p['idx'], p['size']), None)
    def draw(self):
        screen.fill((3, 5, 15))
        for sx, sy, ss in self.stars:
            pygame.draw.circle(screen, (200, 200, 220), (sx, sy), ss)
        for p in self.bg_planets:
            if PLANET_SPRITES.get(p['idx']):
                key = (p['idx'], p['size'])
                if key not in self.planet_cache:
                    self.planet_cache[key] = pygame.transform.scale(PLANET_SPRITES[p['idx']], (p['size'], p['size']))
                screen.blit(self.planet_cache[key], (int(p['x']), int(p['y'])))
        if PLANET_SPRITES.get(1):
            sun_scaled = pygame.transform.scale(PLANET_SPRITES[1], (80, 80))
            screen.blit(sun_scaled, (self.center_x - 40, self.center_y - 40))
        else:
            pygame.draw.circle(screen, (255, 180, 50), (self.center_x, self.center_y), 40)
            pygame.draw.circle(screen, (255, 200, 80), (self.center_x, self.center_y), 35)
        earth_dist = 70
        earth_x = int(self.center_x + math.cos(self.anim * 0.02) * earth_dist)
        earth_y = int(self.center_y + math.sin(self.anim * 0.02) * earth_dist)
        pulse = int(math.sin(self.earth_pulse) * 3)
        if VOID_EARTH:
            frame_w = VOID_EARTH.get_width() // 77
            frame = VOID_EARTH.subsurface((0, 0, frame_w, VOID_EARTH.get_height()))
            earth_scaled = pygame.transform.scale(frame, (44 + pulse * 2, 44 + pulse * 2))
            screen.blit(earth_scaled, (earth_x - 22 - pulse, earth_y - 22 - pulse))
        else:
            if PLANET_SPRITES.get(2):
                earth_scaled = pygame.transform.scale(PLANET_SPRITES[2], (44 + pulse * 2, 44 + pulse * 2))
                screen.blit(earth_scaled, (earth_x - 22 - pulse, earth_y - 22 - pulse))
            else:
                pygame.draw.circle(screen, (30, 60, 130), (earth_x, earth_y), 22 + pulse)
                pygame.draw.circle(screen, (0, 120, 255), (earth_x, earth_y), 18 + pulse)
                for i in range(3):
                    angle = self.anim * 0.03 + i * 2.1
                    cx = earth_x + int(math.cos(angle) * 12)
                    cy = earth_y + int(math.sin(angle) * 8)
                    pygame.draw.ellipse(screen, (80, 160, 80), (cx - 6, cy - 4, 12, 8))
                pygame.draw.circle(screen, (200, 230, 255), (earth_x - 5, earth_y - 5), 5)
class Button:
    def __init__(self, x, y, w, h, text, bg, border):
        self.rect = pygame.Rect(x, y, w, h)
        self.text = text
        self.bg = bg
        self.border = border
    def draw(self, surface):
        hover = self.rect.collidepoint(pygame.mouse.get_pos())
        color = self.bg if not hover else tuple((min(255, c + 30) for c in self.bg))
        pygame.draw.rect(surface, color, self.rect, border_radius=8)
        pygame.draw.rect(surface, self.border, self.rect, 2, border_radius=8)
        draw_text(self.text, FONT, WHITE, self.rect.centerx, self.rect.centery, center=True)
    def clicked(self, pos):
        return self.rect.collidepoint(pos)
class Player(pygame.sprite.Sprite):
    def __init__(self, ship_type='falcon', size_lvl=0, speed_lvl=0, dmg_lvl=0, health_lvl=0):
        super().__init__()
        data = SHIPS[ship_type]
        self.ship_data = data
        self.ship_type = ship_type
        base_size = 55 + size_lvl * 5
        sprite_idx = SHIP_SPRITE_MAP.get(ship_type, 1)
        if PLAYER_SHIPS.get(sprite_idx):
            self.base_image = pygame.transform.scale(PLAYER_SHIPS[sprite_idx], (base_size, int(base_size * 1.2)))
            self.image = self.base_image.copy()
        else:
            self.image = pygame.Surface((base_size, 50), pygame.SRCALPHA)
            self.draw_ship(data['color'], base_size)
            self.base_image = None
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH // 2
        self.rect.bottom = HEIGHT - 40
        self.speed = data['speed'] + speed_lvl * 0.5
        self.last_shot = 0
        self.shoot_delay = max(80, data['delay'] - speed_lvl * 15)
        self.damage = data['damage'] + dmg_lvl
        self.lives = 5
        self.health = 80 + health_lvl * 15
        self.max_health = self.health
        self.invincible = False
        self.invincible_timer = 0
    def draw_ship(self, color, size):
        cx = size // 2
        pygame.draw.polygon(self.image, color, [(cx, 0), (cx + 15, 40), (cx, 35), (cx - 15, 40)])
        pygame.draw.circle(self.image, YELLOW, (cx, 20), 5)
        pygame.draw.rect(self.image, ORANGE, (cx - 8, 35, 4, 5))
        pygame.draw.rect(self.image, ORANGE, (cx + 4, 35, 4, 5))
    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.rect.left > 0:
                self.rect.x -= self.speed
        if keys[pygame.K_RIGHT] and self.rect.right < WIDTH:
                self.rect.x += self.speed
        if keys[pygame.K_UP] and self.rect.top > 0:
                self.rect.y -= self.speed
        if keys[pygame.K_DOWN] and self.rect.bottom < HEIGHT:
                self.rect.y += self.speed
        if self.invincible:
            self.invincible_timer -= 1
            if self.invincible_timer <= 0:
                self.invincible = False
    def shoot(self, triple=False):
        now = pygame.time.get_ticks()
        if now - self.last_shot > self.shoot_delay:
            self.last_shot = now
            sound_manager.play('shoot')
            if triple:
                return [Bullet(self.rect.centerx, self.rect.top - 5, self.damage), Bullet(self.rect.centerx - 18, self.rect.top - 5, self.damage), Bullet(self.rect.centerx + 18, self.rect.top - 5, self.damage)]
            else:
                return [Bullet(self.rect.centerx, self.rect.top - 5, self.damage)]
        else:
            return []
class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, damage=1):
        super().__init__()
        self.image = pygame.Surface((4, 10))
        self.image.fill(YELLOW)
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y
        self.speed = (-12)
        self.damage = damage
    def update(self):
        self.rect.y += self.speed
        if self.rect.bottom < 0:
            self.kill()
class Enemy(pygame.sprite.Sprite):
    def __init__(self, planet_idx):
        super().__init__()
        p = PLANETS[planet_idx]
        self.planet_color = p['color']
        self.planet_idx = planet_idx
        self.enemy_type = random.choice(['fast', 'tank', 'shooter', 'asteroid'])
        self.ship_idx = ENEMY_TYPE_SHIP.get(self.enemy_type)
        self.size = int(max(15, p['size'] // 2 + random.randint((-3), 5)) * 1.5)
        if self.enemy_type == 'fast':
            self.speed_y = random.uniform(4, 7) + planet_idx * 0.3
            self.health = 3
            self.points = 20 * (planet_idx + 1)
        else:
            if self.enemy_type == 'tank':
                self.size = int(max(30, p['size'] // 1.3) * 1.5)
                self.speed_y = random.uniform(1.2, 2) + planet_idx * 0.1
                self.health = 8 + planet_idx
                self.points = 40 * (planet_idx + 1)
            else:
                if self.enemy_type == 'shooter':
                    self.speed_y = random.uniform(1.5, 3) + planet_idx * 0.2
                    self.health = 4 + planet_idx
                    self.points = 25 * (planet_idx + 1)
                    self.shoot_timer = 0
                    self.shoot_delay = max(1000, 2000 - planet_idx * 100)
                else:
                    if self.enemy_type == 'asteroid':
                        self.asteroid_sprite_idx = random.randint(1, 5)
                        tamano_tipo = random.choice(['chico', 'mediano', 'grande', 'gigante'])
                        if tamano_tipo == 'chico':
                            self.size = random.randint(16, 26)
                            self.speed_y = random.uniform(5, 7)
                            self.health = 1
                            self.points = 30
                        else:
                            if tamano_tipo == 'mediano':
                                self.size = random.randint(30, 44)
                                self.speed_y = random.uniform(3.5, 5)
                                self.health = 2
                                self.points = 50
                            else:
                                if tamano_tipo == 'grande':
                                    self.size = random.randint(50, 64)
                                    self.speed_y = random.uniform(2, 3.5)
                                    self.health = 4
                                    self.points = 80
                                else:
                                    self.size = random.randint(74, 96)
                                    self.speed_y = random.uniform(1.2, 2)
                                    self.health = 7
                                    self.points = 150
                        self.rotation = 0
                        self.rotation_speed = random.uniform((-8), 8)
                    else:
                        self.speed_y = random.uniform(2, 4) + planet_idx * 0.2
                        self.health = 3 + planet_idx
                        self.points = 15 * (planet_idx + 1)
        self.max_health = self.health
        self.wobble = random.random() * 6.28
        self.base_x = random.randint(50, WIDTH - 50)
        self.hurt_timer = 0
        self.image = pygame.Surface((self.size * 2 + 20, self.size * 2 + 20), pygame.SRCALPHA)
        self.draw_enemy()
        self.rect = self.image.get_rect()
        self.rect.x = self.base_x
        self.rect.y = random.randint((-100), (-30))
    def draw_enemy(self):
        self.image.fill((0, 0, 0, 0))
        if self.enemy_type == 'asteroid':
            scale = int(self.size * 1.5)
            if scale < 20:
                scale = 20
            else:
                if scale > 80:
                    scale = 80
            asteroid_idx = getattr(self, 'asteroid_sprite_idx', random.randint(1, 5))
            if ASTEROID_SPRITES.get(asteroid_idx):
                scaled = pygame.transform.scale(ASTEROID_SPRITES[asteroid_idx], (scale, scale))
                self.image.blit(scaled, (self.image.get_width() // 2 - scale // 2, self.image.get_height() // 2 - scale // 2))
            else:
                cx, cy = (self.image.get_width() // 2, self.image.get_height() // 2)
                color = (100, 80, 60)
                dark = (60, 50, 30)
                pygame.draw.circle(self.image, dark, (cx, cy), self.size)
                pygame.draw.circle(self.image, color, (cx, cy), self.size - 3)
                for _ in range(4):
                    rx = cx + random.randint(-self.size // 2, self.size // 2)
                    ry = cy + random.randint(-self.size // 2, self.size // 2)
                    pygame.draw.circle(self.image, dark, (rx, ry), random.randint(2, 5))
        else:
            ship_sprite = ENEMY_SHIPS.get(self.ship_idx) if self.ship_idx else None
            if ship_sprite:
                s = int(self.size * 1.8)
                scaled = pygame.transform.scale(ship_sprite, (s, s))
                cx = self.image.get_width() // 2 - s // 2
                cy = self.image.get_height() // 2 - s // 2
                self.image.blit(scaled, (cx, cy))
            else:
                color = self.planet_color
                dark = tuple((max(0, c - 40) for c in color))
                cx, cy = (self.image.get_width() // 2, self.image.get_height() // 2)
                pygame.draw.circle(self.image, dark, (cx, cy), self.size)
                pygame.draw.circle(self.image, color, (cx, cy), self.size - 2)
                pygame.draw.circle(self.image, WHITE, (cx - self.size // 3, cy - self.size // 3), self.size // 6)
    def update(self):
        self.wobble += 0.08
        speed_y = self.speed_y
        if game_slow_active:
            speed_y *= 0.5
        self.rect.y += speed_y
        if self.enemy_type == 'asteroid':
            self.rotation += self.rotation_speed
            self.draw_enemy()
            old_center = self.rect.center
            self.image = pygame.transform.rotate(self.image, self.rotation)
            self.rect = self.image.get_rect()
            self.rect.center = old_center
        self.rect.x = self.base_x + math.sin(self.wobble) * 25
        if self.rect.left < 10:
            self.rect.left = 10
        else:
            if self.rect.right > WIDTH - 10:
                self.rect.right = WIDTH - 10
        if self.hurt_timer > 0:
            self.hurt_timer -= 1
        if self.rect.top > HEIGHT + 50:
            self.kill()
    def hit(self):
        return True
    def shoot(self):
        if self.enemy_type == 'shooter':
            now = pygame.time.get_ticks()
            if now - self.shoot_timer > self.shoot_delay:
                self.shoot_timer = now
                return EnemyBullet(self.rect.centerx, self.rect.bottom, self.planet_color)
        return None
class EnemyBullet(pygame.sprite.Sprite):
    def __init__(self, x, y, color=(255, 50, 0)):
        super().__init__()
        self.image = pygame.Surface((10, 10))
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.top = y
        self.speed = 6
        self.vx = 0
        self.vy = 0
    def update(self):
        if self.vy:
            self.rect.y += self.vy
        else:
            self.rect.y += self.speed
        self.rect.x += self.vx
        if self.rect.top > HEIGHT or self.rect.right < 0 or self.rect.left > WIDTH:
            self.kill()
BOSS_NAMES = ['VELOCIRAPTOR', 'SIRENA', 'MARTILLO', 'TITAN', 'SEÑOR DE LOS ANILLOS']
BOSS_SPRITE_MAP = [1, 2, 3, 5, 7]
class Boss(pygame.sprite.Sprite):
    def __init__(self, planet_idx):
        super().__init__()
        p = PLANETS[planet_idx]
        self.planet_idx = planet_idx
        self.planet_color = p['color']
        self.size = 60 + planet_idx * 8
        self.boss_sprite_idx = BOSS_SPRITE_MAP[planet_idx]
        self.boss_name = BOSS_NAMES[planet_idx]
        self.image = pygame.Surface((self.size * 2 + 40, self.size * 2 + 40), pygame.SRCALPHA)
        self.health = (50 + planet_idx * 35) * 2
        self.max_health = self.health
        self.speed_y = 1.5
        self.horizontal_speed = 2 + planet_idx * 0.3
        self.direction = 1
        self.last_shot = 0
        self.shoot_delay = max(300, 900 - planet_idx * 80)
        self.points = 500 + planet_idx * 200
        self.anim_timer = 0
        self.phase = 0
        self.shoot_angle = 0
        self.move_pattern = 0
        self.move_timer = 0
        self.attack_cooldown = 0
        self.current_attack = 0
        self.draw_boss()
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH // 2
        self.rect.y = -self.size * 2 - 30
        self.hurt_timer = 0
        self.entering = True
    def get_phase(self):
        ratio = self.health / self.max_health
        if ratio <= 0.25:
            return 2
        else:
            if ratio <= 0.5:
                return 1
            else:
                return 0
    def draw_boss(self):
        self.image.fill((0, 0, 0, 0))
        cx, cy = (self.image.get_width() // 2, self.image.get_height() // 2)
        boss_sprite = ENEMY_SHIPS.get(self.boss_sprite_idx)
        phase = self.get_phase()
        tint = self.planet_color
        if phase == 1:
            tint = tuple((min(255, c + 60) for c in tint))
        else:
            if phase == 2:
                tint = (255, max(50, tint[1] // 2), max(50, tint[2] // 2))
        if boss_sprite:
            s = int(self.size * 1.6)
            scaled = pygame.transform.scale(boss_sprite, (s, s))
            if phase == 2:
                flash = pygame.transform.rotate(scaled, math.sin(self.anim_timer * 4) * 5)
                self.image.blit(flash, (cx - s // 2, cy - s // 2))
            else:
                self.image.blit(scaled, (cx - s // 2, cy - s // 2))
            for i in range(4, 0, (-1)):
                glow = tuple((min(255, c + 40 + phase * 30) for c in tint))
                pygame.draw.circle(self.image, glow, (cx, cy), self.size + i * 3, 2)
        else:
            dark = tuple((max(0, c - 40) for c in tint))
            for i in range(4, 0, (-1)):
                glow = tuple((min(255, c + 20 + phase * 20) for c in tint))
                pygame.draw.circle(self.image, glow, (cx, cy), self.size + i * 3, 1)
            pygame.draw.circle(self.image, dark, (cx, cy), self.size)
            pygame.draw.circle(self.image, tint, (cx, cy), self.size - 3)
            pygame.draw.circle(self.image, WHITE, (cx - self.size // 3, cy - self.size // 3), self.size // 4)
        if phase >= 1:
            for i in range(6):
                a = self.anim_timer * 3 + i * 1.047
                px = cx + int(math.cos(a) * (self.size + 8))
                py = cy + int(math.sin(a) * (self.size + 8))
                pygame.draw.circle(self.image, (255, max(50, 200 - phase * 80), 0), (px, py), 3 + phase)
    def update_movement(self):
        self.move_timer += 1
        phase = self.get_phase()
        if self.rect.top < 60:
            self.rect.y += self.speed_y
            return
        else:
            self.entering = False
            speed_mult = 1.0 + phase * 0.3
            if phase == 0:
                self.rect.x += self.horizontal_speed * self.direction * speed_mult
                if self.rect.right > WIDTH - 30 or self.rect.left < 30:
                    self.direction *= (-1)
            else:
                if phase == 1:
                    pulse = math.sin(self.move_timer * 0.03) * 2
                    self.rect.x += (self.horizontal_speed + pulse) * self.direction * speed_mult
                    self.rect.y += math.sin(self.move_timer * 0.05) * 0.5
                    if self.rect.right > WIDTH - 30 or self.rect.left < 30:
                        self.direction *= (-1)
                    if self.rect.top < 30 or self.rect.bottom > HEIGHT // 3:
                        self.rect.y = max(30, min(HEIGHT // 3, self.rect.y))
                else:
                    self.rect.x += (self.horizontal_speed + math.sin(self.move_timer * 0.04) * 3) * self.direction * speed_mult
                    self.rect.y += math.sin(self.move_timer * 0.06) * 1.5
                    if self.rect.right > WIDTH - 30 or self.rect.left < 30:
                        self.direction *= (-1)
                    if self.rect.top < 10 or self.rect.bottom > HEIGHT // 2:
                        self.rect.y = max(10, min(HEIGHT // 2, self.rect.y))
    def update(self):
        self.anim_timer += 0.05
        if self.hurt_timer > 0:
            self.hurt_timer -= 1
        self.update_movement()
        self.draw_boss()
    def shoot(self):
        now = pygame.time.get_ticks()
        phase = self.get_phase()
        delay = self.shoot_delay - phase * 100
        if delay < 150:
            delay = 150
        if now - self.last_shot > delay and (not self.entering):
            self.last_shot = now
            bullets = []
            cx, cy = (self.rect.centerx, self.rect.centery)
            idx = self.planet_idx
            self.current_attack = (self.current_attack + 1) % (3 + phase)
            if idx == 0:
                if self.current_attack == 0:
                    for i in range((-2), 3):
                        b = EnemyBullet(cx + i * 25, cy, self.planet_color)
                        b.speed = 7 + phase
                        b.rect.centerx = cx + i * 25
                        bullets.append(b)
                    return bullets
                else:
                    if self.current_attack == 1:
                        for i in range(5):
                            b = EnemyBullet(cx + i * 60 - 120, cy, YELLOW)
                            b.speed = 5 + phase
                            b.vy = 4 + phase
                            b.vx = (-2) + i
                            bullets.append(b)
                        return bullets
                    else:
                        for i in range((-3), 4):
                            a = 1.57 + i * 0.15
                            b = EnemyBullet(cx, cy, (255, 100, 100))
                            b.speed = 6 + phase
                            b.vx = math.cos(a) * 3
                            b.vy = math.sin(a) * 6
                            bullets.append(b)
                        return bullets
            else:
                if idx == 1:
                    self.shoot_angle += 0.15 + phase * 0.05
                    if self.current_attack == 0:
                        for i in range(3 + phase):
                            a = 1.57 + math.sin(self.shoot_angle + i * 2.1) * 0.8
                            b = EnemyBullet(cx, cy, self.planet_color)
                            b.speed = 5 + phase
                            b.vx = math.cos(a) * 2
                            b.vy = math.sin(a) * 5
                            b.rect.centerx = cx
                            bullets.append(b)
                        return bullets
                    else:
                        if self.current_attack == 1:
                            for i in range(6 + phase * 2):
                                a = self.shoot_angle + i * 1.047
                                b = EnemyBullet(cx, cy, PINK)
                                b.speed = 3 + phase
                                b.vx = math.cos(a) * 2
                                b.vy = math.sin(a) * 2
                                bullets.append(b)
                            return bullets
                        else:
                            target_x = WIDTH // 2
                            for i in range((-1), 2):
                                a = 1.57 + i * 0.3
                                b = EnemyBullet(cx + i * 30, cy, (255, 200, 100))
                                b.speed = 6 + phase
                                b.vx = math.cos(a) * 1.5
                                b.vy = math.sin(a) * 5
                                bullets.append(b)
                            return bullets
                else:
                    if idx == 2:
                        self.shoot_angle += 0.12
                        if self.current_attack == 0:
                            spread = 0.2 + phase * 0.05
                            for i in range(5 + phase * 2):
                                a = 1.57 + (i - (2 + phase)) * spread
                                b = EnemyBullet(cx, cy, self.planet_color)
                                b.speed = 4 + phase
                                b.vx = math.cos(a) * 2
                                b.vy = math.sin(a) * 5
                                b.rect.centerx = cx + int(math.cos(a) * 15 * (i - 2))
                                bullets.append(b)
                            return bullets
                        else:
                            if self.current_attack == 1:
                                for i in range(3):
                                    a = 1.57 + math.sin(self.shoot_angle + i * 0.5) * 0.5
                                    b = EnemyBullet(cx + i * 40 - 40, cy, RED)
                                    b.speed = 6 + phase
                                    b.vx = math.cos(a) * 2
                                    b.vy = math.sin(a) * 6
                                    bullets.append(b)
                                return bullets
                            else:
                                for i in range(4 + phase * 2):
                                    a = 1.57 + (i - (1.5 + phase)) * 0.2
                                    b = EnemyBullet(cx, cy, ORANGE)
                                    b.speed = 5 + phase
                                    b.vx = math.cos(a) * 1.5
                                    b.vy = math.sin(a) * 4
                                    bullets.append(b)
                                return bullets
                    else:
                        if idx == 3:
                            self.shoot_angle += 0.18 + phase * 0.04
                            if self.current_attack == 0:
                                for i in range(8 + phase * 2):
                                    a = self.shoot_angle + i * 0.785
                                    b = EnemyBullet(cx, cy, self.planet_color)
                                    b.speed = 4 + phase
                                    b.vx = math.cos(a) * 3
                                    b.vy = math.sin(a) * 3
                                    bullets.append(b)
                                return bullets
                            else:
                                if self.current_attack == 1:
                                    for col in range(3 + phase):
                                        bx = 100 + col * (WIDTH - 200) // (2 + phase)
                                        b = EnemyBullet(bx, cy + 20, CYAN)
                                        b.speed = 4 + phase
                                        b.vy = 4 + phase
                                        bullets.append(b)
                                    return bullets
                                else:
                                    spread_bullets = 6 + phase * 2
                                    for i in range(spread_bullets):
                                        a = self.shoot_angle + i * (6.28 / spread_bullets)
                                        b = EnemyBullet(cx, cy, (200, 200, 50))
                                        b.speed = 5 + phase
                                        b.vx = math.cos(a) * 3
                                        b.vy = math.sin(a) * 3
                                        bullets.append(b)
                                    return bullets
                        else:
                            self.shoot_angle += 0.2 + phase * 0.06
                            if self.current_attack == 0:
                                for i in range(5 + phase):
                                    a = 1.57 + (i - (2 + phase // 2)) * (0.25 + phase * 0.03)
                                    b = EnemyBullet(cx, cy, self.planet_color)
                                    b.speed = 5 + phase
                                    b.vx = math.cos(a) * 2
                                    b.vy = math.sin(a) * 5
                                    b.rect.centerx = cx + int(math.cos(a) * 20 * (i - 2))
                                    bullets.append(b)
                                return bullets
                            else:
                                if self.current_attack == 1:
                                    for i in range(6 + phase * 2):
                                        a = self.shoot_angle + i * 1.047
                                        b = EnemyBullet(cx, cy, (255, 100, 100))
                                        b.speed = 3 + phase
                                        b.vx = math.cos(a) * 2
                                        b.vy = math.sin(a) * 2
                                        bullets.append(b)
                                    return bullets
                                else:
                                    if self.current_attack == 2:
                                        for i in range(3):
                                            bx = cx + (i - 1) * 80
                                            b = EnemyBullet(bx, cy, GOLD)
                                            b.speed = 7 + phase
                                            b.vy = 7 + phase
                                            bullets.append(b)
                                        return bullets
                                    else:
                                        extra = 8 + phase * 4
                                        for i in range(extra):
                                            a = self.shoot_angle + i * (6.28 / extra)
                                            b = EnemyBullet(cx, cy, PURPLE)
                                            b.speed = 4 + phase
                                            b.vx = math.cos(a) * 2.5 + math.sin(self.anim_timer * 2) * 0.5
                                            b.vy = math.sin(a) * 2.5
                                            bullets.append(b)
                                        return bullets
        else:
            return []
EXPLOSION_FRAMES = []
for f in range(6):
    size = 10 + f * 6
    surf = pygame.Surface((size, size), pygame.SRCALPHA)
    alpha = 255 - f * 45
    pygame.draw.circle(surf, (255, 150, 0, alpha), (size // 2, size // 2), size // 2)
    EXPLOSION_FRAMES.append(surf)
class Explosion(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.frames = EXPLOSION_FRAMES
        self.image = self.frames[0]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.frame = 0
        self.timer = pygame.time.get_ticks()
        self.delay = 40
    def update(self):
        now = pygame.time.get_ticks()
        if now - self.timer > self.delay:
            self.timer = now
            self.frame += 1
            if self.frame >= len(self.frames):
                self.kill()
            else:
                self.image = self.frames[self.frame]
class PowerUp(pygame.sprite.Sprite):
    TYPES = ['shield', 'bomb', 'triple', 'rapido', 'slow', 'score']
    COLORS = {'shield': (100, 200, 255), 'bomb': (255, 100, 50), 'triple': (255, 150, 255), 'rapido': (255, 255, 100), 'slow': (100, 255, 255), 'score': (255, 255, 50)}
    GLOW_COLORS = {'shield': (150, 230, 255), 'bomb': (255, 150, 100), 'triple': (255, 200, 255), 'rapido': (255, 255, 180), 'slow': (180, 255, 255), 'score': (255, 255, 150)}
    def __init__(self, x, y):
        super().__init__()
        self.power_type = random.choice(self.TYPES)
        self.color = self.COLORS[self.power_type]
        self.glow_color = self.GLOW_COLORS[self.power_type]
        self.anim_timer = random.randint(0, 100)
        self.image = pygame.Surface((48, 48), pygame.SRCALPHA)
        self.draw_powerup(1.0)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.speed_y = 1.5
    def draw_powerup(self, pulse):
        self.image.fill((0, 0, 0, 0))
        cx, cy = (24, 24)
        r = int(16 * pulse)
        glow_radius = r + 8
        glow_alpha = int(60 * pulse)
        for i in range(3):
            gr = glow_radius + i * 3
            gsurf = pygame.Surface((gr * 2, gr * 2), pygame.SRCALPHA)
            gs = gr * 2
            pygame.draw.circle(gsurf, (*self.glow_color, glow_alpha // (i + 1)), (gr, gr), gr)
            self.image.blit(gsurf, (cx - gr, cy - gr), special_flags=pygame.BLEND_ALPHA_SDL2)
        pygame.draw.circle(self.image, WHITE, (cx, cy), r)
        pygame.draw.circle(self.image, self.color, (cx, cy), r - 2)
        inner = r - 6
        if self.power_type == 'shield':
            pts = [(cx, cy - inner), (cx + inner, cy), (cx, cy + inner), (cx - inner, cy)]
            pygame.draw.polygon(self.image, WHITE, pts, 2)
            pts2 = [(cx, cy - inner + 3), (cx + inner - 3, cy), (cx, cy + inner - 3), (cx - inner + 3, cy)]
            pygame.draw.polygon(self.image, (*self.color, 160), pts2, 1)
        else:
            if self.power_type == 'bomb':
                for ang in range(0, 360, 45):
                    a = math.radians(ang + self.anim_timer * 3)
                    ex = cx + int(math.cos(a) * inner * 0.8)
                    ey = cy + int(math.sin(a) * inner * 0.8)
                    pygame.draw.line(self.image, (255, 255, 200), (cx, cy), (ex, ey), 2)
                pygame.draw.circle(self.image, (255, 200, 100), (cx, cy), inner // 2)
            else:
                if self.power_type == 'triple':
                    for i in range(3):
                        a = math.radians((-90) + i * 120)
                        tx = cx + int(math.cos(a) * inner * 0.5)
                        ty = cy + int(math.sin(a) * inner * 0.5)
                        pts = [(tx, ty - 6), (tx + 5, ty + 4), (tx - 5, ty + 4)]
                        pygame.draw.polygon(self.image, WHITE, pts)
                else:
                    if self.power_type == 'rapido':
                        pts = [(cx - 2, cy - inner), (cx + 6, cy - 2), (cx, cy - 2), (cx + 2, cy + inner), (cx - 6, cy + 2), (cx, cy + 2)]
                        pygame.draw.polygon(self.image, (255, 255, 255), pts)
                    else:
                        if self.power_type == 'slow':
                            for ang in range(0, 360, 90):
                                a = math.radians(ang + self.anim_timer * 2)
                                sx = cx + int(math.cos(a) * inner)
                                sy = cy + int(math.sin(a) * inner)
                                pygame.draw.line(self.image, (200, 255, 255), (cx, cy), (sx, sy), 2)
                            for ang in range(45, 360, 90):
                                a = math.radians(ang + self.anim_timer * 2)
                                sx = cx + int(math.cos(a) * inner * 0.7)
                                sy = cy + int(math.sin(a) * inner * 0.7)
                                pygame.draw.line(self.image, (200, 255, 255), (cx, cy), (sx, sy), 1)
                        else:
                            if self.power_type == 'score':
                                pts = [(cx, cy - inner), (cx + inner * 0.6, cy - inner * 0.3), (cx + inner * 0.4, cy + inner * 0.7), (cx - inner * 0.4, cy + inner * 0.7), (cx - inner * 0.6, cy - inner * 0.3)]
                                pygame.draw.polygon(self.image, WHITE, pts)
                                pygame.draw.polygon(self.image, (255, 255, 200), [(cx, cy - inner + 3), (cx + int(inner * 0.5), cy - int(inner * 0.2)), (cx - int(inner * 0.3), cy + int(inner * 0.5)), (cx - int(inner * 0.5), cy - int(inner * 0.2))])
    def update(self):
        self.anim_timer += 1
        pulse = 1.0 + math.sin(self.anim_timer * 0.08) * 0.08
        self.draw_powerup(pulse)
        self.rect.y += self.speed_y
        if self.rect.top > HEIGHT + 30:
            self.kill()
MEDAL_DESIGNS = [{'name': 'BRONCE', 'color': (205, 127, 50), 'glow': (255, 180, 80), 'star_color': (255, 220, 150), 'size': 80}, {'name': 'PLATA', 'color': (192, 192, 192), 'glow': (220, 220, 255), 'star_color': (255, 255, 255), 'size': 85}, {'name': 'ORO', 'color': (255, 215, 0), 'glow': (255, 255, 100), 'star_color': (255, 255, 200), 'size': 90}, {'name': 'RUBI', 'color': (200, 30, 50), 'glow': (255, 100, 100), 'star_color': (255, 200, 200), 'size': 95}, {'name': 'DIAMANTE', 'color': (150, 220, 255), 'glow': (200, 240, 255), 'star_color': (255, 255, 255), 'size': 100}]
class MedalAnimation:
    def __init__(self, planet_idx):
        design = MEDAL_DESIGNS[planet_idx]
        self.name = design['name']
        self.color = design['color']
        self.glow = design['glow']
        self.star_color = design['star_color']
        self.medal_size = design['size']
        self.timer = 180
        self.max_timer = 180
        self.angle = 0
        self.sparkles = []
        for _ in range(12):
            self.sparkles.append({'angle': random.uniform(0, 6.28), 'dist': random.randint(self.medal_size + 10, self.medal_size + 40), 'speed': random.uniform(0.02, 0.05), 'size': random.randint(2, 5)})
    def update(self):
        self.timer -= 1
        self.angle += 0.03
        for sp in self.sparkles:
            sp['angle'] += sp['speed']
    def draw(self, surface):
        cx, cy = (WIDTH // 2, HEIGHT // 2 - 30)
        alpha = min(255, int(self.timer / self.max_timer * 255))
        if self.timer < 30:
            alpha = int(self.timer / 30 * 255)
        if alpha <= 0:
            return
        else:
            surf = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            for sp in self.sparkles:
                px = cx + int(math.cos(sp['angle'] + self.angle) * sp['dist'])
                py = cy + int(math.sin(sp['angle'] + self.angle) * sp['dist'])
                c = tuple((min(255, c + 50) for c in self.glow))
                pygame.draw.circle(surf, (*c, alpha // 2), (px, py), sp['size'])
            pulse = math.sin(self.angle * 2) * 10
            for r in range(5, 0, (-1)):
                rad = self.medal_size + r * 8 + int(pulse)
                glow_a = alpha // (r + 1)
                pygame.draw.circle(surf, (*self.glow, glow_a), (cx, cy), rad, 3)
            pygame.draw.circle(surf, (*self.color, alpha), (cx, cy), self.medal_size)
            pygame.draw.circle(surf, (*self.glow, alpha), (cx, cy), self.medal_size, 4)
            inner = self.medal_size - 10
            pygame.draw.circle(surf, (*self.star_color, alpha // 2), (cx, cy), inner, 2)
            star_points = []
            for i in range(10):
                a = (-1.57) + i * 0.6283
                r2 = 25 if i % 2 == 0 else 12
                star_points.append((cx + math.cos(a + self.angle) * r2, cy + math.sin(a + self.angle) * r2))
            pygame.draw.polygon(surf, (*self.star_color, alpha), star_points)
            pygame.draw.circle(surf, (*self.glow, alpha // 3), (cx, cy), 8)
            if alpha > 100:
                txt_surf = TITLE_FONT.render(f'MEDALLA DE {self.name}', True, (*self.star_color, alpha))
                txt_rect = txt_surf.get_rect(center=(cx, cy + self.medal_size + 40))
                surface.blit(txt_surf, txt_rect)
            surface.blit(surf, (0, 0))
    def is_alive(self):
        return self.timer > 0
    def kill(self):
        self.timer = 0
class ParticleSystem:
    def __init__(self):
        self.particles = []
    def emit(self, x, y, color, count=5):
        for _ in range(count):
            self.particles.append({'x': x + random.randint((-10), 10), 'y': y + random.randint((-10), 10), 'vx': random.uniform((-2), 2), 'vy': random.uniform((-2), 2), 'life': 15, 'color': color})
    def update(self):
        for p in self.particles[:]:
            p['x'] += p['vx']
            p['y'] += p['vy']
            p['life'] -= 1
            if p['life'] <= 0:
                self.particles.remove(p)
    def draw(self, surface):
        for p in self.particles:
            pygame.draw.circle(surface, p['color'], (int(p['x']), int(p['y'])), 2)
class GameData:
    SAVE_FILE = 'datos-de-jugadores/config.txt'
    @staticmethod
    def ensure_dir():
        os.makedirs(os.path.dirname(GameData.SAVE_FILE), exist_ok=True)
    @staticmethod
    def load():
        GameData.ensure_dir()
        data = {'high_score': 0, 'upgrades': {'size': 0, 'speed': 0, 'damage': 0, 'health': 0}, 'difficulty': 'normal'}
        try:
            if os.path.exists(GameData.SAVE_FILE):
                with open(GameData.SAVE_FILE, 'r') as f:
                    for line in f:
                        if ':' not in line:
                            continue
                        k, v = line.strip().split(':', 1)
                        k = k.strip()
                        v = v.strip()
                        if k == 'HIGH_SCORE':
                            data['high_score'] = int(v)
                        elif k in ['SIZE_LEVEL', 'SPEED_LEVEL', 'DAMAGE_LEVEL', 'HEALTH_LEVEL']:
                            data['upgrades'][k.lower().replace('_level', '')] = int(v)
                        elif k == 'DIFFICULTY':
                            data['difficulty'] = v
        except Exception as e:
            import traceback
            traceback.print_exc()
        return data
    @staticmethod
    def save(high_score, upgrades, difficulty):
        try:
            with open(GameData.SAVE_FILE, 'w') as f:
                f.write('==============================\n')
                f.write('SOLAR DEFENDER - CONFIGURACION\n')
                f.write('==============================\n\n')
                f.write(f'HIGH_SCORE: {high_score}\n')
                f.write(f'DIFFICULTY: {difficulty}\n\n')
                f.write('-- MEJORAS DE NAVE --\n')
                f.write(f"SIZE_LEVEL: {upgrades.get('size', 0)}\n")
                f.write(f"SPEED_LEVEL: {upgrades.get('speed', 0)}\n")
                f.write(f"DAMAGE_LEVEL: {upgrades.get('damage', 0)}\n")
                f.write(f"HEALTH_LEVEL: {upgrades.get('health', 0)}\n")
        except Exception as e:
            import traceback
            traceback.print_exc()
class PlayerDB:
    DB_FILE = 'datos-de-jugadores/players_data.txt'
    @staticmethod
    def ensure_dir():
        os.makedirs(os.path.dirname(PlayerDB.DB_FILE), exist_ok=True)
    @staticmethod
    def load():
        PlayerDB.ensure_dir()
        players = []
        try:
            if os.path.exists(PlayerDB.DB_FILE):
                with open(PlayerDB.DB_FILE, 'r') as f:
                    p = None
                    for line in f:
                        s = line.strip()
                        if s.startswith('JUGADOR:'):
                            if p is not None:
                                players.append(p)
                            p = {'name': s.split(':', 1)[1].strip(), 'color': '', 'score': 0, 'ship': '', 'gender': '', 'age': 0, 'level': 0, 'medals': 0, 'status': ''}
                        elif p is not None and ':' in s:
                            k, v = s.split(':', 1)
                            k = k.strip().lower()
                            v = v.strip()
                            if k == 'puntaje':
                                p['score'] = int(v)
                            elif k == 'nave':
                                p['color'] = v
                                p['ship'] = v
                            elif k == 'genero':
                                p['gender'] = v
                            elif k == 'edad':
                                p['age'] = int(v)
                            elif k == 'planeta':
                                p['level'] = int(v)
                            elif k == 'medallas':
                                p['medals'] = int(v)
                            elif k == 'estado':
                                p['status'] = v
                    if p is not None:
                        players.append(p)
        except Exception as e:
            import traceback
            traceback.print_exc()
        return sorted(players, key=lambda x: x['score'], reverse=True)
    @staticmethod
    def save(name, color, score, ship='', gender='', age=0, level=0, medals=0, status=''):
        PlayerDB.ensure_dir()
        players = PlayerDB.load()
        players.append({'name': name, 'color': color, 'score': score, 'ship': ship, 'gender': gender, 'age': age, 'level': level, 'medals': medals, 'status': status})
        try:
            with open(PlayerDB.DB_FILE, 'w') as f:
                f.write('==================================\n')
                f.write('SOLAR DEFENDER - REGISTRO JUGADORES\n')
                f.write('==================================\n\n')
                for p in players:
                    f.write(f"JUGADOR: {p['name']}\n")
                    f.write(f"  PUNTAJE: {p['score']}\n")
                    f.write(f"  NAVE: {p['ship'] or p['color']}\n")
                    f.write(f"  GENERO: {p['gender']}\n")
                    f.write(f"  EDAD: {p['age']}\n")
                    f.write(f"  PLANETA: {p['level']}\n")
                    f.write(f"  MEDALLAS: {p['medals']}\n")
                    f.write(f"  ESTADO: {p['status']}\n\n")
        except Exception as e:
            import traceback
            traceback.print_exc()
        return players
        return players
class AstronautSelectScreen:
    def __init__(self, game):
        self.game = game
        self.sexo = 'masculino'
        self.nombre = ''
        self.edad_valor = ''
        self.cursor_visible = True
        self.cursor_timer = 0
        self.anim_angle = 0
        self.paso = 1
    def update(self):
        self.anim_angle += 0.1
        self.cursor_timer += 1
        if self.cursor_timer >= 30:
            self.cursor_timer = 0
            self.cursor_visible = not self.cursor_visible
    def draw(self):
        self.game.solar_menu.update()
        self.game.solar_menu.draw()
        center_x = WIDTH // 2
        self.draw_cute_astronauta(center_x, 150)
        panel_w, panel_h = (380, 150)
        panel_x = center_x - panel_w // 2
        panel_y = 270
        pygame.draw.rect(screen, (40, 20, 60), (panel_x - 5, panel_y - 5, panel_w + 10, panel_h + 10), border_radius=20)
        pygame.draw.rect(screen, (70, 40, 100), (panel_x, panel_y, panel_w, panel_h), border_radius=15)
        for i in range(4):
            px = panel_x + 45 + i * 95
            step_y = panel_y + 18
            color = GOLD if i + 1 == self.paso else (50, 50, 70)
            if i + 1 < self.paso:
                color = (50, 200, 80)
            pygame.draw.circle(screen, color, (px, step_y), 14)
            pygame.draw.circle(screen, (20, 20, 30), (px, step_y), 16, 2)
            draw_text(str(i + 1), FONT, WHITE, px, step_y, center=True)
        if self.paso == 1:
            self.draw_paso_nombre(center_x, panel_y)
        else:
            if self.paso == 2:
                self.draw_paso_edad(center_x, panel_y)
            else:
                if self.paso == 3:
                    self.draw_paso_sexo(center_x, panel_y)
                else:
                    if self.paso == 4:
                        self.draw_paso_confirmar(center_x, panel_y)
        help_y = HEIGHT - 25
        if self.paso == 1:
            draw_text('ESCRIBE tu nombre  [ESPACIO] Siguiente', FONT, CYAN, center_x, help_y, center=True)
        else:
            if self.paso == 2:
                draw_text('ESCRIBE tu edad  [ESPACIO] Siguiente', FONT, CYAN, center_x, help_y, center=True)
            else:
                if self.paso == 3:
                    draw_text('← NIÑO   NIÑA →  [ESPACIO] Confirmar', FONT, YELLOW, center_x, help_y, center=True)
                else:
                    if self.paso == 4:
                        draw_text('ESPACIO para CONTINUAR', FONT, GREEN, center_x, help_y, center=True)
    def draw_cute_astronauta(self, cx, cy):
        sway = math.sin(self.anim_angle) * 3
        bounce = math.sin(self.anim_angle * 2) * 2
        color_traje = (60, 120, 220) if self.sexo == 'masculino' else (220, 80, 140)
        pygame.draw.ellipse(screen, (30, 30, 40), (cx - 18 + sway, cy + 60 + bounce, 36, 20))
        pygame.draw.ellipse(screen, color_traje, (cx - 20 + sway, cy + 10 + bounce, 40, 50))
        pygame.draw.ellipse(screen, (max(0, color_traje[0] - 20), max(0, color_traje[1] - 20), max(0, color_traje[2] - 20)), (cx - 20 + sway, cy + 10 + bounce, 40, 15))
        pygame.draw.ellipse(screen, (255, 200, 0), (cx - 22 + sway, cy - 30 + bounce, 44, 40))
        pygame.draw.ellipse(screen, (255, 255, 220), (cx - 18 + sway, cy - 25 + bounce, 36, 30))
        pygame.draw.ellipse(screen, (255, 255, 255), (cx - 12 + sway, cy - 20 + bounce, 12, 18))
        pygame.draw.ellipse(screen, (50, 50, 60), (cx - 18 + sway, cy - 35 + bounce, 8, 8))
        pygame.draw.ellipse(screen, (50, 50, 60), (cx + 10 + sway, cy - 35 + bounce, 8, 8))
        for i in range(3):
            star_x = cx - 15 + i * 12 + sway
            star_y = cy - 40 + bounce + int(math.sin(self.anim_angle + i) * 3)
            pygame.draw.circle(screen, (255, 255, 200), (star_x, star_y), 2)
    def draw_paso_nombre(self, cx, panel_y):
        draw_text('Tu nombre:', FONT, (180, 180, 200), cx, panel_y + 50, center=True)
        box_x, box_y = (cx - 80, panel_y + 65)
        pygame.draw.rect(screen, (40, 20, 60), (box_x, box_y, 160, 28), 1, border_radius=6)
        name_display = self.nombre + ('_' if self.cursor_visible else '')
        draw_text(name_display if name_display else '...', FONT, WHITE, box_x + 8, box_y + 6)
        if len(self.nombre) >= 3:
            draw_text('✓ ok', FONT, GREEN, cx, panel_y + 110, center=True)
            return
        else:
            if len(self.nombre) > 0:
                draw_text('+ letras', FONT, (150, 150, 100), cx, panel_y + 110, center=True)
    def draw_paso_edad(self, cx, panel_y):
        draw_text('Tu edad:', FONT, (180, 180, 200), cx, panel_y + 50, center=True)
        box_x, box_y = (cx - 25, panel_y + 65)
        pygame.draw.rect(screen, (40, 20, 60), (box_x, box_y, 50, 28), 1, border_radius=6)
        age_display = self.edad_valor + ('_' if self.cursor_visible else '')
        draw_text(age_display if age_display else '?', FONT, WHITE, box_x + 20, box_y + 6, center=True)
        if self.edad_valor:
            try:
                e = int(self.edad_valor)
                if 1 <= e <= 15:
                    draw_text(f'{e} años ✓', FONT, GREEN, cx, panel_y + 110, center=True)
            except:
                return
    def draw_paso_sexo(self, cx, panel_y):
        draw_text('Elige tu equipo:', FONT, (180, 180, 200), cx, panel_y + 50, center=True)
        btn_y = panel_y + 75
        w, h = (90, 35)
        if self.sexo == 'masculino':
            pygame.draw.rect(screen, (60, 100, 220), (cx - 100, btn_y, w, h), border_radius=10)
            pygame.draw.rect(screen, (50, 50, 70), (cx + 10, btn_y, w, h), border_radius=10)
        else:
            pygame.draw.rect(screen, (50, 50, 70), (cx - 100, btn_y, w, h), border_radius=10)
            pygame.draw.rect(screen, (200, 80, 150), (cx + 10, btn_y, w, h), border_radius=10)
        pygame.draw.rect(screen, WHITE, (cx - 100, btn_y, w, h), 3, border_radius=10)
        pygame.draw.rect(screen, WHITE, (cx + 10, btn_y, w, h), 3, border_radius=10)
        draw_text('🔵 NIÑO', FONT, WHITE, cx - 55, btn_y + 18, center=True)
        draw_text('🌸 NIÑA', FONT, WHITE, cx + 55, btn_y + 18, center=True)
    def draw_paso_confirmar(self, cx, panel_y):
        draw_text('✓ Listo!', FONT, GREEN, cx, panel_y + 55, center=True)
        draw_text(f'{self.nombre}, {self.edad_valor} años', FONT, WHITE, cx, panel_y + 80, center=True)
        emoji = '🔵' if self.sexo == 'masculino' else '🌸'
        color_rgb = (100, 150, 255) if self.sexo == 'masculino' else (255, 150, 180)
        draw_text(f"{emoji} {('Niño' if self.sexo == 'masculino' else 'Niña')}", FONT, color_rgb, cx, panel_y + 105, center=True)
        pygame.draw.rect(screen, GREEN, (cx - 70, panel_y + 118, 140, 22), border_radius=6)
        draw_text('ENTER', FONT, WHITE, cx, panel_y + 131, center=True)
    def handle_key(self, event):
        if event.key == pygame.K_ESCAPE:
            self.game.state = 'menu'
        else:
            if event.key == pygame.K_SPACE:
                if self.paso == 1 and len(self.nombre) >= 3:
                    self.paso = 2
                else:
                    if self.paso == 2 and self.edad_valor:
                        try:
                            e = int(self.edad_valor)
                            if 1 <= e <= 120:
                                self.paso = 3
                        except:
                            return None
                    else:
                        if self.paso == 3:
                            self.paso = 4
                        else:
                            if self.paso == 4:
                                edad_int = int(self.edad_valor)
                                self.game.astronauta_nombre = self.nombre
                                self.game.astronauta_edad = edad_int
                                self.game.astronauta_sexo = self.sexo
                                self.game.state = 'ship_select'
            else:
                if event.key == pygame.K_BACKSPACE:
                    if self.paso == 1 and len(self.nombre) > 0:
                        self.nombre = self.nombre[:(-1)]
                    else:
                        if self.paso == 2 and len(self.edad_valor) > 0:
                                self.edad_valor = self.edad_valor[:(-1)]
                else:
                    if event.key == pygame.K_LEFT:
                        if self.paso == 3:
                            self.sexo = 'masculino'
                        else:
                            if self.paso > 1:
                                self.paso -= 1
                    else:
                        if event.key == pygame.K_RIGHT:
                            if self.paso == 3:
                                self.sexo = 'femenino'
                            else:
                                if self.paso == 1 and len(self.nombre) >= 3:
                                    self.paso = 2
                                else:
                                    if self.paso == 2 and self.edad_valor:
                                            try:
                                                e = int(self.edad_valor)
                                                if 1 <= e <= 120:
                                                    self.paso = 3
                                            except:
                                                return
                        else:
                            if event.unicode.isalnum():
                                if self.paso == 1 and len(self.nombre) < 10 and event.unicode.isalpha():
                                    self.nombre += event.unicode
                                else:
                                    if self.paso == 2 and len(self.edad_valor) < 2 and event.unicode.isdigit():
                                                self.edad_valor += event.unicode
class Game:
    def __init__(self):
        self.screen = screen
        self.clock = clock
        self.background = Background()
        self.solar_menu = SolarMenu()
        saved = GameData.load()
        self.high_score = saved['high_score']
        self.upgrades = saved['upgrades']
        self.difficulty = saved['difficulty']
        dif_map = {'easy': 0.5, 'normal': 0.8, 'hard': 1.0, 'facil': 0.5, 'dificil': 1.0}
        self.difficulty_mult = dif_map.get(self.difficulty, 1.0)
        if self.difficulty in ['facil', 'dificil']:
            self.difficulty = {'facil': 'easy', 'dificil': 'hard'}.get(self.difficulty)
        self.astronauta_nombre = ''
        self.astronauta_edad = 0
        self.astronauta_sexo = 'masculino'
        self.medallas = 0
        self.screen_shake = 0
        self.shake_intensity = 0
        self.medal_anim = None
        self.reset()
    def reset(self):
        self.state = 'menu'
        sound_manager.start_ambient()
        self.score = 0
        self.current_planet = 0
        self.selected_ship = 'rapido'
        self.player_name = 'Player'
        self.ship_selection = 0
        self.ship_select_timer = 0
        self.ships_list = list(SHIPS.keys())
        self.astronauta_nombre = ''
        self.astronauta_edad = 0
        self.astronauta_sexo = 'masculino'
        self.astronauta_screen = AstronautSelectScreen(self)
        self.ship_size_lvl = self.upgrades.get('size', 0)
        self.ship_speed_lvl = self.upgrades.get('speed', 0)
        self.ship_damage_lvl = self.upgrades.get('damage', 0)
        self.ship_health_lvl = self.upgrades.get('health', 0)
        self.combo = 0
        self.combo_timer = 0
        self.shield_active = False
        self.shield_timer = 0
        self.triple_shot_timer = 0
        self.slow_timer = 0
        self.rapid_fire_timer = 0
        self.base_shoot_delay = 0
        self.paused = False
        self.screen_shake = 0
        self.shake_intensity = 0
        self.menu_button = 0
        self.quiz_active = False
        self.quiz_q = None
        self.quiz_sel = 0
        self.quiz_done = False
        self.quiz_correct = False
        self.medal_anim = None
    def new_game(self):
        self.all_sprites = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        self.bullets = pygame.sprite.Group()
        self.enemy_bullets = pygame.sprite.Group()
        self.explosions = pygame.sprite.Group()
        self.powerups = pygame.sprite.Group()
        self.particles = ParticleSystem()
        dm = self.difficulty_mult
        self.player = Player(self.selected_ship, int(self.ship_size_lvl * dm), int(self.ship_speed_lvl * dm), int(self.ship_damage_lvl * dm), int(self.ship_health_lvl * dm))
        self.all_sprites.add(self.player)
        self.boss = None
        self.boss_spawned = False
        self.enemies_spawned = 0
        self.enemy_timer = pygame.time.get_ticks()
        self.combo = 0
        self.shield_active = False
        self.shield_timer = 0
        self.triple_shot_timer = 0
        self.slow_timer = 0
        self.rapid_fire_timer = 0
        self.base_shoot_delay = 0
        self.took_damage = False
        self.state = 'level_start'
    def spawn_enemy(self):
        p = PLANETS[self.current_planet]
        if self.enemies_spawned < p['enemies']:
            now = pygame.time.get_ticks()
            delay = max(200, 500 - self.current_planet * 50)
            if now - self.enemy_timer > delay:
                self.enemy_timer = now
                enemy = Enemy(self.current_planet)
                self.all_sprites.add(enemy)
                self.enemies.add(enemy)
                self.enemies_spawned += 1
    def spawn_boss(self):
        p = PLANETS[self.current_planet]
        if not self.boss_spawned and self.enemies_spawned >= p['enemies'] and (len(self.enemies) == 0):
                    self.boss = Boss(self.current_planet)
                    self.all_sprites.add(self.boss)
                    self.boss_spawned = True
                    self.boss_powerup_timer = pygame.time.get_ticks()
    def spawn_powerup(self, x, y):
        if random.random() < 0.15:
            p = PowerUp(x, y)
            self.powerups.add(p)
            self.all_sprites.add(p)
    def collect_powerup(self, p):
        self.particles.emit(p.rect.centerx, p.rect.centery, p.color, 15)
        sound_manager.play('powerup')
        if p.power_type == 'shield':
            self.shield_active = True
            self.shield_timer = 480
        else:
            if p.power_type == 'bomb':
                for enemy in self.enemies:
                    self.particles.emit(enemy.rect.centerx, enemy.rect.centery, RED, 12)
                    self.score += enemy.points
                    enemy.kill()
            else:
                if p.power_type == 'rapido':
                    if self.base_shoot_delay == 0:
                        self.base_shoot_delay = self.player.shoot_delay
                    self.player.shoot_delay = max(60, self.player.shoot_delay - 40)
                    self.rapid_fire_timer = 300
                else:
                    if p.power_type == 'triple':
                        self.triple_shot_timer = 300
                    else:
                        if p.power_type == 'slow':
                            self.slow_timer = 240
                        else:
                            if p.power_type == 'score':
                                self.score += 200
                                self.particles.emit(p.rect.centerx, p.rect.centery, (255, 255, 50), 20)
    def save_game(self):
        if self.score > self.high_score:
            self.high_score = self.score
        GameData.save(self.high_score, {'size': self.ship_size_lvl, 'speed': self.ship_speed_lvl, 'damage': self.ship_damage_lvl, 'health': self.ship_health_lvl}, self.difficulty)
    def check_collisions(self):
        if self.paused:
            return
        else:
            for enemy in self.enemies:
                pass
                hits = pygame.sprite.spritecollide(enemy, self.bullets, True)
                if hits:
                    dmg = self.player.damage
                    if enemy.hit():
                        enemy.health -= dmg
                        if enemy.health <= 0:
                            self.score += enemy.points + self.combo * 5
                            self.combo = min(self.combo + 1, 10)
                            self.combo_timer = 60
                            sound_manager.play('explosion')
                            self.particles.emit(enemy.rect.centerx, enemy.rect.centery, enemy.planet_color, 8)
                            exp = Explosion(enemy.rect.centerx, enemy.rect.centery)
                            self.explosions.add(exp)
                            self.all_sprites.add(exp)
                            self.spawn_powerup(enemy.rect.centerx, enemy.rect.centery)
                            enemy.kill()
                        else:
                            enemy.hurt_timer = 5
                            enemy.draw_enemy()
        if self.boss:
            hits = pygame.sprite.spritecollide(self.boss, self.bullets, True)
            for hit in hits:
                self.boss.health -= self.player.damage
                self.boss.hurt_timer = 5
                self.score += 5
                self.particles.emit(hit.rect.centerx, hit.rect.centery, self.boss.planet_color, 5)
                if random.random() < 0.12:
                    self.spawn_powerup(hit.rect.centerx, hit.rect.centery)
                if self.boss.health <= 0:
                    self.score += self.boss.points
                    self.particles.emit(self.boss.rect.centerx, self.boss.rect.centery, self.boss.planet_color, 20)
                    exp = Explosion(self.boss.rect.centerx, self.boss.rect.centery)
                    self.explosions.add(exp)
                    self.all_sprites.add(exp)
                    self.boss.kill()
                    self.boss = None
                    self.state = 'quiz'
                    self.quiz_active = True
                    self.quiz_q = random.choice(QUIZ_QUESTIONS)
                    self.quiz_sel = 0
                    self.quiz_done = False
                    self.quiz_correct = False
                    sound_manager.play('victory')
                    return
        if not self.player.invincible:
            hits = pygame.sprite.spritecollide(self.player, self.enemies, False)
            for hit in hits:
                if self.shield_active:
                    hit.kill()
                    self.particles.emit(hit.rect.centerx, hit.rect.centery, (100, 200, 255), 10)
                else:
                    self.took_damage = True
                    self.player.health -= 35
                    self.player.invincible = True
                    self.player.invincible_timer = 40
                    self.combo = 0
                    sound_manager.play('hit')
                    self.particles.emit(self.player.rect.centerx, self.player.rect.centery, RED, 8)
                    hit.kill()
                    if self.player.health <= 0:
                        self.player.lives -= 1
                        self.player.health = self.player.max_health
                        if self.player.lives <= 0:
                            self.state = 'game_over'
                            sound_manager.play('gameover')
                            self.save_game()
                            nombre = self.astronauta_nombre or self.player_name
                            PlayerDB.save(nombre, 'blue', self.score, self.selected_ship, self.astronauta_sexo, self.astronauta_edad, self.current_planet, self.medallas, 'PIERDE')
        hits = pygame.sprite.spritecollide(self.player, self.enemy_bullets, True)
        for hit in hits:
            if not self.player.invincible:
                if self.shield_active:
                    self.particles.emit(hit.rect.centerx, hit.rect.centery, (100, 200, 255), 5)
                else:
                    self.took_damage = True
                    self.player.health -= 25
                    self.player.invincible = True
                    self.player.invincible_timer = 40
                    self.combo = 0
                    sound_manager.play('hit')
                    if self.player.health <= 0:
                        self.player.lives -= 1
                        self.player.health = self.player.max_health
                        if self.player.lives <= 0:
                            self.state = 'game_over'
                            sound_manager.play('gameover')
                            self.save_game()
                            nombre = self.astronauta_nombre or self.player_name
                            PlayerDB.save(nombre, 'blue', self.score, self.selected_ship, self.astronauta_sexo, self.astronauta_edad, self.current_planet, self.medallas, 'PIERDE')
        hits = pygame.sprite.spritecollide(self.player, self.powerups, True)
        for p in hits:
            self.collect_powerup(p)
    def update(self):
        global game_slow_active
        self.background.update()
        if self.screen_shake > 0:
            self.screen_shake -= 1
        if self.medal_anim:
            self.medal_anim.update()
            if not self.medal_anim.is_alive():
                if self.state == 'medal_display':
                    self.state = 'level_complete'
                    sound_manager.play('menu_select')
                self.medal_anim = None
        if self.state == 'ship_select':
            self.ship_select_timer += 1
        if self.state == 'paused':
            return
        else:
            if self.state in ['level_start', 'playing']:
                self.all_sprites.update()
                self.particles.update()
                if self.combo_timer > 0:
                    self.combo_timer -= 1
                    if self.combo_timer == 0:
                        self.combo = 0
                bullets = self.player.shoot(triple=self.triple_shot_timer > 0)
                for b in bullets:
                    self.bullets.add(b)
                    self.all_sprites.add(b)
                if self.boss:
                    now_boss = pygame.time.get_ticks()
                    if now_boss - self.boss_powerup_timer > 4000:
                        self.boss_powerup_timer = now_boss
                        p = PowerUp(random.randint(50, WIDTH - 50), 20)
                        self.powerups.add(p)
                        self.all_sprites.add(p)
                    old_phase = self.boss.phase
                    self.boss.phase = self.boss.get_phase()
                    if self.boss.phase > old_phase:
                        self.screen_shake = 15
                        self.shake_intensity = 8
                        sound_manager.play('explosion')
                        for _ in range(20):
                            self.particles.emit(self.boss.rect.centerx + random.randint((-40), 40), self.boss.rect.centery + random.randint((-40), 40), (255, 100, 0), 5)
                        p = PowerUp(self.boss.rect.centerx, self.boss.rect.centery)
                        self.powerups.add(p)
                        self.all_sprites.add(p)
                    bullets = self.boss.shoot()
                    if bullets:
                        for b in bullets:
                            self.enemy_bullets.add(b)
                            self.all_sprites.add(b)
                if self.triple_shot_timer > 0:
                    self.triple_shot_timer -= 1
                if self.slow_timer > 0:
                    self.slow_timer -= 1
                    game_slow_active = True
                else:
                    game_slow_active = False
                if self.shield_timer > 0:
                    self.shield_timer -= 1
                    if self.shield_timer <= 0:
                        self.shield_active = False
                if self.rapid_fire_timer > 0:
                    self.rapid_fire_timer -= 1
                    if self.rapid_fire_timer <= 0 and self.base_shoot_delay > 0:
                            self.player.shoot_delay = self.base_shoot_delay
                            self.base_shoot_delay = 0
                for enemy in self.enemies:
                    b = enemy.shoot()
                    if b:
                        self.enemy_bullets.add(b)
                        self.all_sprites.add(b)
                self.spawn_enemy()
                self.spawn_boss()
                self.check_collisions()
    def draw_hud(self):
        draw_text(f'PUNTOS: {self.score}', FONT, WHITE, 15, 12)
        if self.combo > 1:
            draw_text(f'x{self.combo}', FONT, YELLOW, 120, 12)
        planet_name = PLANETS[self.current_planet]['name']
        draw_text(f'VIDAS: {self.player.lives}', FONT, PINK, 15, 32)
        pygame.draw.rect(screen, DARK_GRAY, (15, 55, 120, 8))
        fill = int(self.player.health / self.player.max_health * 120)
        color = GREEN if self.player.health > 50 else YELLOW if self.player.health > 25 else RED
        pygame.draw.rect(screen, color, (15, 55, fill, 8))
        if self.shield_active:
            pygame.draw.circle(screen, (100, 200, 255), (20, 75), 8)
            draw_text('ESCUDO', FONT, (100, 200, 255), 35, 72)
        menu_btn = Button(WIDTH - 100, 5, 90, 25, 'MENU', (80, 30, 30), RED)
        menu_btn.draw(screen)
        if not self.boss:
            draw_text(f'NIVEL {self.current_planet + 1}: {planet_name}', FONT, (100, 200, 255), WIDTH // 2, 12, center=True)
        if self.boss:
            bx, by, bw, bh = (WIDTH // 2 - 100, 6, 200, 10)
            draw_text(self.boss.boss_name, FONT, self.boss.planet_color, WIDTH // 2, by - 10, center=True)
            pygame.draw.rect(screen, DARK_GRAY, (bx, by, bw, bh))
            fill = int(self.boss.health / self.boss.max_health * bw)
            bar_color = RED if self.boss.get_phase() == 0 else ORANGE if self.boss.get_phase() == 1 else (255, 50, 50)
            pygame.draw.rect(screen, bar_color, (bx, by, fill, bh))
            pygame.draw.rect(screen, WHITE, (bx, by, bw, bh), 1)
            phase_text = ['', 'FASE 2', 'FASE 3'][self.boss.get_phase()]
            if phase_text:
                phase_color = YELLOW if self.boss.get_phase() == 1 else RED
                draw_text(phase_text, SMALL_FONT, phase_color, bx + bw + 30, by + 1)
    def draw(self):
        if self.state == 'astronauta_select':
            self.astronauta_screen.update()
            self.astronauta_screen.draw()
        else:
            if self.state == 'menu':
                self.solar_menu.update()
                self.solar_menu.draw()
                time = pygame.time.get_ticks()
                title_y = 30
                scroll_text = 'DESARROLLO DE SOFTWARE EL NACIONAL 2do AÑO'
                scroll_w = FONT.render(scroll_text, True, WHITE).get_width()
                scroll_speed = 0.1
                total_dist = WIDTH + scroll_w
                scroll_x_pos = -scroll_w + int(time * scroll_speed % total_dist)
                scroll_y = 8
                scroll_bg = pygame.Surface((scroll_w + 10, 22))
                scroll_bg.set_alpha(140)
                scroll_bg.fill((5, 15, 40))
                screen.blit(scroll_bg, (scroll_x_pos - 5, scroll_y - 2))
                draw_text(scroll_text, FONT, CYAN, scroll_x_pos, scroll_y)
                bar_width = WIDTH - 200
                bar_x = 100
                pygame.draw.rect(screen, (5, 15, 35), (bar_x, title_y, bar_width, 45), border_radius=6)
                pygame.draw.rect(screen, (50, 150, 200), (bar_x, title_y, bar_width, 45), 2, border_radius=6)
                for i in range(12):
                    wave_x = bar_x + 15 + i * ((bar_width - 30) // 11)
                    wave_height = 4 + int(math.sin(time * 0.005 + i * 0.5) * 3)
                    wave_y = title_y + 35
                    for h in range(wave_height):
                        alpha = 255 - h * 30
                        color = (50, 150, 200, max(0, alpha))
                        s = pygame.Surface((5, 1), pygame.SRCALPHA)
                        s.fill(color)
                        screen.blit(s, (wave_x, wave_y - h))
                star_colors = [(100, 200, 255), (150, 220, 255), CYAN]
                for i in range(15):
                    sx = bar_x + 15 + i * 47 % (bar_width - 30)
                    sy = title_y + 8 + i * 17 % 20
                    flicker = int(math.sin(time * 0.008 + i) * 1 + 2)
                    color_idx = i % 3
                    pygame.draw.rect(screen, star_colors[color_idx], (sx, sy, flicker, flicker))
                title_text = 'SOLAR DEFENDER'
                draw_text(title_text, TITLE_FONT, (30, 30, 60), WIDTH // 2, title_y + 18, center=True)
                draw_text(title_text, TITLE_FONT, CYAN, WIDTH // 2, title_y + 28, center=True)
                shine_offset = int(math.sin(time * 0.003) * 5)
                for i, char in enumerate(title_text):
                    char_x = WIDTH // 2 - len(title_text) * 12 + i * 24 + 12
                    char_y = title_y + 28
                    pygame.draw.rect(screen, (100, 200, 255, 100), (char_x + 2, char_y + shine_offset, 18, 4))
                center_panel_x = WIDTH // 2 - 130
                button_data = [(200, 50, 'JUGAR', (20, 100, 180)), (260, 45, 'ELEGIR NAVE', (60, 50, 100)), (315, 45, 'ESTADISTICAS', (50, 70, 50)), (370, 45, 'RANKING', (40, 100, 40)), (425, 45, 'SALIR', (120, 30, 30))]
                for i, (y, h, text, color) in enumerate(button_data):
                    btn = Button(center_panel_x, y, 260, h, text, color, CYAN)
                    if i == self.menu_button:
                        pulse = int(math.sin(time * 0.006) * 5)
                        pygame.draw.rect(screen, (80, 180, 255), (center_panel_x - 4, y - 4, 268, h + 8), 2, border_radius=8)
                        pygame.draw.rect(screen, (100, 200, 255, 50), (center_panel_x - 2, y - 2, 264, h + 4), border_radius=8)
                    btn.draw(screen)
                if self.high_score > 0:
                    draw_text(f'MEJOR PUNTAJE: {self.high_score}', FONT, (150, 150, 180), WIDTH // 2, 500, center=True)
                    top_players = PlayerDB.load()
                    if top_players:
                        top = top_players[0]
                        top_info = [f"{top['name']}"]
                        if top.get('ship') and top['ship'] in SHIPS:
                                top_info.append(f"Nave: {SHIPS[top['ship']]['name']}")
                        if top.get('gender'):
                            top_info.append('Niño' if top['gender'] == 'masculino' else 'Niña')
                        draw_text('  |  '.join(top_info), FONT, (180, 200, 220), WIDTH // 2, 520, center=True)
                footer_y = HEIGHT - 40
                panel_diff = pygame.Surface((300, 50), pygame.SRCALPHA)
                panel_diff.fill((5, 15, 35, 180))
                screen.blit(panel_diff, (WIDTH // 2 - 150, footer_y - 25))
                draw_text('DIFICULTAD:', FONT, GRAY, WIDTH // 2 - 80, footer_y - 5, center=True)
                for i, diff in enumerate(['FACIL', 'NORMAL', 'DIFICIL']):
                    x = WIDTH // 2 + 20 + i * 60
                    val = ['easy', 'normal', 'hard'][i]
                    is_sel = val == self.difficulty
                    color = GREEN if diff == 'FACIL' else YELLOW if diff == 'NORMAL' else RED
                    if is_sel:
                        pygame.draw.rect(screen, color, (x - 25, footer_y - 18, 50, 20), border_radius=4)
                        draw_text(diff, FONT, BLACK, x, footer_y - 5, center=True)
                    else:
                        draw_text(diff, FONT, color, x, footer_y - 5, center=True)
                draw_text('[ENTER] Seleccionar  [↑↓] Moverse  [1-3] Dificultad', FONT, (100, 100, 120), WIDTH // 2, HEIGHT - 25, center=True)
                flag_x, flag_y = (30, HEIGHT - 160)
                flag_w, flag_h = (130, 72)
                stripe_h = flag_h // 3
                celeste = (114, 180, 230)
                blanco = (255, 255, 255)
                oro = (255, 215, 0)
                glow_surf = pygame.Surface((flag_w + 60, flag_h + 60), pygame.SRCALPHA)
                for r in range(25, 0, (-1)):
                    a = max(0, 60 - r * 2)
                    pygame.draw.ellipse(glow_surf, (150, 220, 255, a), (glow_surf.get_width() // 2 - r * 3, glow_surf.get_height() // 2 - r * 2, r * 6, r * 4))
                screen.blit(glow_surf, (flag_x - 30, flag_y - 30))
                pygame.draw.rect(screen, celeste, (flag_x, flag_y, flag_w, stripe_h))
                pygame.draw.rect(screen, blanco, (flag_x, flag_y + stripe_h, flag_w, stripe_h))
                pygame.draw.rect(screen, celeste, (flag_x, flag_y + 2 * stripe_h, flag_w, stripe_h))
                sun_cx = flag_x + flag_w // 2
                sun_cy = flag_y + flag_h // 2
                sun_r = stripe_h - 5
                pygame.draw.circle(screen, (200, 170, 0), (sun_cx, sun_cy), sun_r + 2)
                pygame.draw.circle(screen, oro, (sun_cx, sun_cy), sun_r)
                pygame.draw.circle(screen, (255, 240, 130), (sun_cx, sun_cy), sun_r - 3)
                for i in range(16):
                    ang = i * 0.3927
                    rx = sun_cx + int(math.cos(ang) * (sun_r + 4))
                    ry = sun_cy + int(math.sin(ang) * (sun_r + 4))
                    pygame.draw.circle(screen, oro, (rx, ry), 2)
                pygame.draw.circle(screen, (80, 55, 0), (sun_cx - 4, sun_cy - 2), 1)
                pygame.draw.circle(screen, (80, 55, 0), (sun_cx + 4, sun_cy - 2), 1)
                pygame.draw.arc(screen, (80, 55, 0), (sun_cx - 5, sun_cy, 10, 5), 0.2, math.pi - 0.2, 1)
                txt_x = flag_x
                txt_y = flag_y + flag_h + 8
                txt_surf = CREDIT_FONT.render('MADE IN CORDOBA LA CARLOTA', True, oro)
                screen.blit(txt_surf, (txt_x, txt_y))
                credit_x = WIDTH - 20
                credit_y = HEIGHT - 58
                alpha_pulse = abs(math.sin(time * 0.002)) * 0.5 + 0.5
                line1 = SMALL_FONT.render('Desarrollado por', True, (150, 180, 200))
                line2 = CREDIT_FONT.render('NAHUEL PEDRAZA', True, (100, 200, 255))
                glow_w = max(line1.get_width(), line2.get_width()) + 40
                glow = pygame.Surface((glow_w, 40), pygame.SRCALPHA)
                for r in range(15, 0, (-1)):
                    a = int(alpha_pulse * 12 * (15 - r))
                    pygame.draw.ellipse(glow, (100, 200, 255, a), (glow_w // 2 - r * 3, 20 - r, r * 6, r * 2))
                screen.blit(glow, (credit_x - glow_w, credit_y - 10))
                screen.blit(line1, (credit_x - line1.get_width(), credit_y))
                screen.blit(line2, (credit_x - line2.get_width(), credit_y + 16))
            else:
                if self.state == 'ship_select':
                    self.solar_menu.update()
                    self.solar_menu.draw()
                    cx = WIDTH // 2
                    panel = pygame.Surface((WIDTH - 80, HEIGHT - 60), pygame.SRCALPHA)
                    panel.fill((0, 20, 40, 230))
                    screen.blit(panel, (40, 30))
                    pygame.draw.rect(screen, CYAN, (40, 30, WIDTH - 80, HEIGHT - 60), 3)
                    draw_text('ELEGIR TU NAVE', TITLE_FONT, (0, 100, 150), cx + 3, 53, center=True)
                    draw_text('ELEGIR TU NAVE', TITLE_FONT, GOLD, cx, 50, center=True)
                    pygame.draw.line(screen, GOLD, (cx - 200, 72), (cx + 200, 72), 2)
                    astro_color = BLUE if self.astronauta_sexo == 'masculino' else PINK
                    pygame.draw.circle(screen, astro_color, (cx - 110, 92), 10)
                    pygame.draw.circle(screen, WHITE, (cx - 110, 92), 10, 1)
                    inicial = self.astronauta_nombre[0].upper() if self.astronauta_nombre else '?'
                    draw_text(inicial, FONT, WHITE, cx - 110, 92, center=True)
                    draw_text(f'{self.astronauta_nombre}  |  {self.astronauta_edad} años', FONT, WHITE, cx + 15, 92, center=True)
                    pulse = math.sin(self.ship_select_timer * 0.06) * 0.5 + 0.5
                    bob = math.sin(self.ship_select_timer * 0.04) * 5
                    ship_spacing = 290
                    start_x = cx - ship_spacing
                    for i, ship_key in enumerate(self.ships_list):
                        ship = SHIPS[ship_key]
                        x = start_x + i * ship_spacing
                        y = 195
                        sel = i == self.ship_selection
                        card_w, card_h = (200, 220)
                        card_x = x - card_w // 2
                        card_y = y - 15
                        card_rect = pygame.Rect(card_x, card_y, card_w, card_h)
                        shadow_surf = pygame.Surface((card_w, card_h), pygame.SRCALPHA)
                        shadow_surf.fill((0, 0, 0, 50))
                        screen.blit(shadow_surf, (card_x + 4, card_y + 4))
                        if sel:
                            glow = int(pulse * 50) + 15
                            glow_color = tuple((min(255, c + glow) for c in ship['color']))
                            glow_rect = pygame.Rect(card_x - 3, card_y - 3, card_w + 6, card_h + 6)
                            pygame.draw.rect(screen, glow_color, glow_rect, border_radius=12)
                            pygame.draw.rect(screen, glow_color, glow_rect, 2, border_radius=12)
                        bg_color = (18, 28, 50) if not sel else (22, 35, 68)
                        pygame.draw.rect(screen, bg_color, card_rect, border_radius=10)
                        border_color = WHITE if sel else ship['color']
                        border_width = 2 if sel else 1
                        pygame.draw.rect(screen, border_color, card_rect, border_width, border_radius=10)
                        ship_y = y + 15 + (bob if sel else 0)
                        draw_ship_icon(x, ship_y, ship['color'], ship_key, scale=1.4)
                        name_color = WHITE if sel else (210, 210, 210)
                        draw_text(ship['name'].upper(), FONT, name_color, x, y + 58, center=True)
                        draw_text(ship['desc'], SMALL_FONT, ship['color'], x, y + 74, center=True)
                        pygame.draw.line(screen, (50, 60, 85), (x - 50, y + 85), (x + 50, y + 85))
                        cadencia = round((300 - ship['delay']) / 30, 1)
                        stats_data = [('VEL', ship['speed'], 6, (0, 230, 200)), ('DAN', ship['damage'], 3, (255, 120, 60)), ('CAD', cadencia, 5, (200, 180, 80))]
                        for j, (label, val, max_val, bar_color) in enumerate(stats_data):
                            sy = y + 92 + j * 17
                            bar_w = 110
                            bar_h = 7
                            bar_x = x - bar_w // 2
                            fill_w = int(val / max_val * bar_w)
                            pygame.draw.rect(screen, (30, 35, 55), (bar_x, sy, bar_w, bar_h), border_radius=3)
                            if fill_w > 0:
                                pygame.draw.rect(screen, bar_color, (bar_x, sy, fill_w, bar_h), border_radius=3)
                            draw_text(label, SMALL_FONT, (140, 145, 165), bar_x - 20, sy - 1, center=True)
                        if sel:
                            btn_y = y + 148
                            btn_w, btn_h = (160, 30)
                            btn_x = x - btn_w // 2
                            btn_rect = pygame.Rect(btn_x, btn_y, btn_w, btn_h)
                            btn_glow = int(pulse * 50)
                            btn_border = (0, 180 + btn_glow, 230 + btn_glow)
                            btn_border = tuple((min(255, c) for c in btn_border))
                            pygame.draw.rect(screen, (0, 25, 48), btn_rect, border_radius=8)
                            pygame.draw.rect(screen, btn_border, btn_rect, 2, border_radius=8)
                            tri_size = 6
                            tri_x = x - 24
                            tri_y = btn_y + btn_h // 2
                            pygame.draw.polygon(screen, CYAN, [(tri_x, tri_y - tri_size), (tri_x, tri_y + tri_size), (tri_x + tri_size + 2, tri_y)])
                            draw_text('JUGAR', FONT, WHITE, x + 6, btn_y + btn_h // 2, center=True)
                    draw_text('[ESC] Volver  [ENTER] Jugar  [← →] Elegir nave', FONT, YELLOW, cx, HEIGHT - 40, center=True)
                else:
                    if self.state == 'stats':
                        self.background.draw()
                        panel = pygame.Surface((WIDTH - 100, HEIGHT - 100), pygame.SRCALPHA)
                        panel.fill((0, 20, 40, 240))
                        screen.blit(panel, (50, 50))
                        pygame.draw.rect(screen, CYAN, (50, 50, WIDTH - 100, HEIGHT - 100), 3)
                        draw_text('ESTADISTICAS', TITLE_FONT, CYAN, WIDTH // 2, 80, center=True)
                        stats = [('Mejor Puntaje:', f'{self.high_score}', YELLOW), ('Dificultad:', {'easy': 'FACIL', 'normal': 'NORMAL', 'hard': 'DIFICIL'}.get(self.difficulty, self.difficulty.upper()), GREEN if self.difficulty == 'easy' else YELLOW if self.difficulty == 'normal' else RED)]
                        for i, (label, value, color) in enumerate(stats):
                            draw_text(label, FONT, GRAY, 120, 140 + i * 40)
                            draw_text(str(value), FONT, color, 450, 140 + i * 40)
                        draw_text('ESC - VOLVER', FONT, YELLOW, WIDTH // 2, HEIGHT - 40, center=True)
                    else:
                        if self.state == 'ranking':
                            self.solar_menu.update()
                            self.solar_menu.draw()
                            panel = pygame.Surface((WIDTH - 100, HEIGHT - 90), pygame.SRCALPHA)
                            panel.fill((0, 20, 50, 230))
                            screen.blit(panel, (50, 45))
                            pygame.draw.rect(screen, GREEN, (50, 45, WIDTH - 100, HEIGHT - 90), 3, border_radius=10)
                            draw_text('- MEJORES PILOTOS -', TITLE_FONT, GREEN, WIDTH // 2, 65, center=True)
                            players = PlayerDB.load()
                            planetas = ['Mercurio', 'Venus', 'Marte', 'Jupiter', 'Saturno']
                            if len(players) == 0:
                                draw_text('¡Sé el primero en jugar!', FONT, GRAY, WIDTH // 2, 150, center=True)
                            else:
                                col_name = 130
                                col_age = 290
                                col_ship = 410
                                col_level = 510
                                col_status = 610
                                col_score = 740
                                draw_text('PILOTO', FONT, CYAN, col_name, 100, center=True)
                                draw_text('EDAD', FONT, CYAN, col_age, 100, center=True)
                                draw_text('NAVE', FONT, CYAN, col_ship, 100, center=True)
                                draw_text('NIVEL', FONT, CYAN, col_level, 100, center=True)
                                draw_text('ESTADO', FONT, CYAN, col_status, 100, center=True)
                                draw_text('PUNTOS', FONT, CYAN, col_score, 100, center=True)
                                pygame.draw.line(screen, CYAN, (100, 115), (WIDTH - 100, 115), 1)
                                for i, p in enumerate(players):
                                    y = 130 + i * 42
                                    color = YELLOW if i == 0 else WHITE
                                    rank_badge = ['🥇', '🥈', '🥉'][i] if i < 3 else f'{i + 1}.'
                                    draw_text(f"{rank_badge} {p['name']}", FONT, color, col_name - 60, y)
                                    draw_text(f"{p['age']} años", FONT, color, col_age, y, center=True)
                                    ship_name = SHIPS[p['ship']]['name'] if p.get('ship') and p['ship'] in SHIPS else '-'
                                    draw_text(ship_name, FONT, WHITE, col_ship, y, center=True)
                                    lvl = p.get('level', 0)
                                    lvl_text = f'{planetas[lvl]}' if lvl < len(planetas) else 'Victoria'
                                    draw_text(lvl_text, FONT, (100, 200, 255), col_level, y, center=True)
                                    status = p.get('status', '')
                                    status_colors = {'GANA': (100, 255, 100), 'PIERDE': (255, 100, 100), 'SALE': (255, 255, 100)}
                                    status_color = status_colors.get(status, GRAY)
                                    status_text = {'GANA': 'GANO', 'PIERDE': 'PERDIO', 'SALE': 'SALIO'}.get(status, status)
                                    draw_text(status_text, FONT, status_color, col_status, y, center=True)
                                    draw_text(f"{p['score']}", FONT, YELLOW, col_score, y, center=True)
                            draw_text('ESC - VOLVER', FONT, YELLOW, WIDTH // 2, HEIGHT - 30, center=True)
                        else:
                            if self.state in ['level_start', 'playing', 'level_complete', 'quiz', 'medal_display']:
                                self.background.draw()
                                earth_x, earth_y = (WIDTH // 2, HEIGHT - 90)
                                base_size = 130
                                if VOID_EARTH_GAME:
                                    screen.blit(VOID_EARTH_GAME, (earth_x - base_size - 20, earth_y - base_size - 20))
                                else:
                                    if PLANET_SPRITES.get(2):
                                        earth_scaled = pygame.transform.scale(PLANET_SPRITES[2], (base_size * 2 + 40, base_size * 2 + 40))
                                        screen.blit(earth_scaled, (earth_x - base_size - 20, earth_y - base_size - 20))
                                    else:
                                        pygame.draw.circle(screen, (20, 40, 80), (earth_x, earth_y), base_size + 20)
                                        pygame.draw.circle(screen, (0, 100, 200), (earth_x, earth_y), base_size)
                                        pygame.draw.circle(screen, (50, 150, 255), (earth_x, earth_y), base_size - 5)
                                        continents = [((earth_x - 40, earth_y - 30), 25), ((earth_x + 30, earth_y - 50), 20), ((earth_x + 50, earth_y + 10), 18), ((earth_x - 60, earth_y + 20), 22), ((earth_x + 10, earth_y + 40), 15)]
                                        for (cx, cy), size in continents:
                                            pygame.draw.ellipse(screen, (80, 160, 80), (cx - size, cy - size // 2, size * 2, size))
                                        pygame.draw.circle(screen, (200, 230, 255), (earth_x - 30, earth_y - 30), 20)
                                self.all_sprites.draw(self.screen)
                                self.explosions.draw(self.screen)
                                self.particles.draw(screen)
                                if self.state == 'level_start':
                                    pname = PLANETS[self.current_planet]['name']
                                    draw_text(f'¡{pname.upper()} NOS ATACA!', TITLE_FONT, (100, 200, 255), WIDTH // 2, 60, center=True)
                                    draw_text(f'NIVEL {self.current_planet + 1}', FONT, GREEN, WIDTH // 2, 100, center=True)
                                    draw_text('[ESPACIO] Comenzar  [P] Pausa  [ESC] Menu', FONT, YELLOW, WIDTH // 2, HEIGHT - 60, center=True)
                                else:
                                    if self.shield_active:
                                        pulse = math.sin(pygame.time.get_ticks() * 0.01) * 5
                                        pygame.draw.circle(screen, (100, 200, 255, 60), (self.player.rect.centerx, self.player.rect.centery), max(self.player.rect.width, self.player.rect.height) + 10 + int(pulse), 2)
                                    if self.player.invincible and pygame.time.get_ticks() // 50 % 2 == 0:
                                            flash = self.player.image.copy()
                                            flash.fill((120, 120, 255, 0), special_flags=pygame.BLEND_RGBA_ADD)
                                            screen.blit(flash, self.player.rect)
                                    self.draw_hud()
                                    if self.state in ['level_complete', 'quiz', 'medal_display']:
                                        nxt = self.current_planet + 1
                                        if nxt < len(PLANETS):
                                            draw_text(f"¡{PLANETS[self.current_planet]['name']} VENCIDO!", FONT, GREEN, WIDTH // 2, HEIGHT // 2, center=True)
                                            draw_text(f"SIGUIENTE: {PLANETS[nxt]['name']}", FONT, YELLOW, WIDTH // 2, HEIGHT // 2 + 30, center=True)
                                        if self.state == 'quiz':
                                            s = pygame.Surface((WIDTH, HEIGHT))
                                            s.set_alpha(180)
                                            s.fill((0, 0, 0))
                                            screen.blit(s, (0, 0))
                                            qw, qh = (500, 280)
                                            qx, qy = (WIDTH // 2 - qw // 2, HEIGHT // 2 - qh // 2)
                                            pygame.draw.rect(screen, (20, 30, 80), (qx, qy, qw, qh), border_radius=15)
                                            pygame.draw.rect(screen, GOLD, (qx, qy, qw, qh), 3, border_radius=15)
                                            draw_text('🌟 PREGUNTA 🌟', TITLE_FONT, GOLD, WIDTH // 2, qy + 25, center=True)
                                            draw_text(self.quiz_q['q'], FONT, WHITE, WIDTH // 2, qy + 70, center=True)
                                            for i, opt in enumerate(self.quiz_q['opts']):
                                                oy = qy + 105 + i * 42
                                                sel = i == self.quiz_sel
                                                color = GOLD if sel else (50, 50, 80)
                                                txt_color = BLACK if sel else WHITE
                                                pygame.draw.rect(screen, color, (qx + 40, oy, qw - 80, 34), border_radius=8)
                                                if self.quiz_done:
                                                    if i == self.quiz_q['ans']:
                                                        pygame.draw.rect(screen, GREEN, (qx + 40, oy, qw - 80, 34), border_radius=8)
                                                        txt_color = BLACK
                                                    else:
                                                        if sel and (not self.quiz_correct):
                                                                pygame.draw.rect(screen, RED, (qx + 40, oy, qw - 80, 34), border_radius=8)
                                                                txt_color = WHITE
                                                draw_text(opt, FONT, txt_color, WIDTH // 2, oy + 17, center=True)
                                            if not self.quiz_done:
                                                draw_text('[↑↓] Elegir  [ENTER] Responder', FONT, (150, 150, 180), WIDTH // 2, qy + qh - 25, center=True)
                                            else:
                                                if self.quiz_correct:
                                                    draw_text('✅ ¡CORRECTO! +1 MEDALLA + MEJORA', FONT, GREEN, WIDTH // 2, qy + qh - 25, center=True)
                                                else:
                                                    draw_text(f"❌ INCORRECTO. Era: {self.quiz_q['opts'][self.quiz_q['ans']]}", FONT, (255, 150, 150), WIDTH // 2, qy + qh - 25, center=True)
                                                draw_text('[ESPACIO] Continuar', FONT, YELLOW, WIDTH // 2, qy + qh + 25, center=True)
                                        if self.state == 'medal_display':
                                            s = pygame.Surface((WIDTH, HEIGHT))
                                            s.set_alpha(160)
                                            s.fill((0, 0, 0))
                                            screen.blit(s, (0, 0))
                                            draw_text('PRESIONA [ESPACIO] PARA CONTINUAR', FONT, YELLOW, WIDTH // 2, HEIGHT - 50, center=True)
                            else:
                                if self.state == 'game_over':
                                    self.background.draw()
                                    s = pygame.Surface((WIDTH, HEIGHT))
                                    s.set_alpha(180)
                                    s.fill((0, 0, 0))
                                    screen.blit(s, (0, 0))
                                    draw_text('¡FIN DEL JUEGO!', TITLE_FONT, RED, WIDTH // 2, 180, center=True)
                                    draw_text(f'PUNTOS: {self.score}', FONT, WHITE, WIDTH // 2, 250, center=True)
                                    if self.score >= self.high_score and self.score > 0:
                                            draw_text('¡NUEVO RECORD!', FONT, YELLOW, WIDTH // 2, 290, center=True)
                                    draw_text('[ENTER] Menu  [ESPACIO] Reiniciar', FONT, YELLOW, WIDTH // 2, 350, center=True)
                                    draw_text('[←→↑↓] Moverse  [ESPACIO] Disparar', FONT, (150, 150, 150), WIDTH // 2, 380, center=True)
                                else:
                                    if self.state == 'victory':
                                        self.background.draw()
                                        s = pygame.Surface((WIDTH, HEIGHT))
                                        s.set_alpha(200)
                                        s.fill((0, 50, 100))
                                        screen.blit(s, (0, 0))
                                        draw_text('¡VICTORIA!', TITLE_FONT, YELLOW, WIDTH // 2, 150, center=True)
                                        draw_text('¡JUEGO GUARDADO!', FONT, WHITE, WIDTH // 2, 200, center=True)
                                        draw_text(f'PUNTOS: {self.score}', FONT, CYAN, WIDTH // 2, 280, center=True)
                                        draw_text('[ENTER] Volver al Menu', FONT, YELLOW, WIDTH // 2, 380, center=True)
                                    else:
                                        if self.state == 'paused':
                                            self.background.draw()
                                            self.all_sprites.draw(self.screen)
                                            self.draw_hud()
                                            s = pygame.Surface((WIDTH, HEIGHT))
                                            s.set_alpha(160)
                                            s.fill((0, 0, 0))
                                            screen.blit(s, (0, 0))
                                            panel = pygame.Surface((300, 200), pygame.SRCALPHA)
                                            panel.fill((20, 30, 60, 230))
                                            screen.blit(panel, (WIDTH // 2 - 150, HEIGHT // 2 - 100))
                                            pygame.draw.rect(screen, CYAN, (WIDTH // 2 - 150, HEIGHT // 2 - 100, 300, 200), 3, border_radius=10)
                                            draw_text('PAUSA', TITLE_FONT, CYAN, WIDTH // 2, HEIGHT // 2 - 80, center=True)
                                            draw_text('[P] o [ENTER] Continuar  [ESC] Menu', FONT, WHITE, WIDTH // 2, HEIGHT // 2 - 20, center=True)
        if self.medal_anim:
            self.medal_anim.draw(screen)
        if self.screen_shake > 0:
            shake_x = random.randint(-self.shake_intensity, self.shake_intensity)
            shake_y = random.randint(-self.shake_intensity, self.shake_intensity)
            current_screen = screen.copy()
            screen.fill(BLACK)
            screen.blit(current_screen, (shake_x, shake_y))
        pygame.display.flip()
    def next_level(self):
        if self.current_planet < len(PLANETS) - 1:
            self.current_planet += 1
            self.new_game()
            self.state = 'level_start'
            return
        else:
            self.state = 'victory'
            sound_manager.play('victory')
            if self.score > self.high_score:
                self.high_score = self.score
            self.save_game()
    def run(self):
        running = True
        while running:
            self.clock.tick(FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    nombre = self.astronauta_nombre or self.player_name
                    if nombre and self.state not in ['menu']:
                            PlayerDB.save(nombre, 'blue', self.score, self.selected_ship, self.astronauta_sexo, self.astronauta_edad, self.current_planet, self.medallas, 'SALE')
                    running = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    cx = WIDTH // 2
                    if self.state == 'menu':
                        center_panel_x = WIDTH // 2 - 130
                        button_rects = [(center_panel_x, 200, 260, 50), (center_panel_x, 260, 260, 45), (center_panel_x, 315, 260, 45), (center_panel_x, 370, 260, 45), (center_panel_x, 425, 260, 45)]
                        for i, (bx, by, bw, bh) in enumerate(button_rects):
                            if pygame.Rect(bx, by, bw, bh).collidepoint(event.pos):
                                self.menu_button = i
                                if i == 0 or i == 1:
                                    self.astronauta_screen = AstronautSelectScreen(self)
                                    self.state = 'astronauta_select'
                                else:
                                    if i == 2:
                                        self.state = 'stats'
                                    else:
                                        if i == 3:
                                            self.state = 'ranking'
                                        else:
                                            if i == 4:
                                                self.save_game()
                                                running = False
                                break
                        footer_y = HEIGHT - 40
                        for i, diff in enumerate(['easy', 'normal', 'hard']):
                            x = WIDTH // 2 + 20 + i * 60
                            if pygame.Rect(x - 25, footer_y - 18, 50, 20).collidepoint(event.pos):
                                self.difficulty = diff
                                self.difficulty_mult = {'easy': 0.5, 'normal': 0.8, 'hard': 1.0}.get(self.difficulty, 1.0)
                                self.save_game()
                                break
                    else:
                        if self.state == 'ship_select':
                            ship_cx = WIDTH // 2
                            ship_spacing = 290
                            start_x = ship_cx - ship_spacing
                            for i in range(len(self.ships_list)):
                                x = start_x + i * ship_spacing
                                if pygame.Rect(x - 100, 180, 200, 220).collidepoint(event.pos):
                                    self.ship_selection = i
                                    break
                        else:
                            if self.state in ('playing', 'level_start', 'level_complete') and pygame.Rect(WIDTH - 100, 5, 90, 25).collidepoint(event.pos):
                                    self.save_game()
                                    nombre = self.astronauta_nombre or self.player_name
                                    if nombre:
                                        PlayerDB.save(nombre, 'blue', self.score, self.selected_ship, self.astronauta_sexo, self.astronauta_edad, self.current_planet, self.medallas, 'SALE')
                                    self.reset()
                                    self.state = 'menu'
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        if self.state in ['astronauta_select', 'ship_select', 'game_over', 'victory', 'stats', 'ranking']:
                            self.state = 'menu'
                        else:
                            if self.state in ['playing', 'level_complete', 'quiz']:
                                self.save_game()
                                nombre = self.astronauta_nombre or self.player_name
                                if nombre:
                                    PlayerDB.save(nombre, 'blue', self.score, self.selected_ship, self.astronauta_sexo, self.astronauta_edad, self.current_planet, self.medallas, 'SALE')
                                self.reset()
                                self.state = 'menu'
                            else:
                                if self.state == 'paused':
                                    self.paused = False
                                    self.state = 'playing'
                                else:
                                    if self.state == 'menu':
                                        self.save_game()
                                        running = False
                    else:
                        if event.key == pygame.K_p:
                            if self.state == 'playing':
                                self.paused = True
                                self.state = 'paused'
                            else:
                                if self.state == 'paused':
                                    self.paused = False
                                    self.state = 'playing'
                        else:
                            if event.key == pygame.K_RETURN:
                                if self.state == 'menu':
                                    sound_manager.play('menu_select')
                                    if self.menu_button == 0 or self.menu_button == 1:
                                        self.astronauta_screen = AstronautSelectScreen(self)
                                        self.state = 'astronauta_select'
                                    else:
                                        if self.menu_button == 2:
                                            self.state = 'stats'
                                        else:
                                            if self.menu_button == 3:
                                                self.state = 'ranking'
                                            else:
                                                if self.menu_button == 4:
                                                    self.save_game()
                                                    running = False
                                else:
                                    if self.state == 'astronauta_select':
                                        if self.astronauta_screen.nombre and self.astronauta_screen.edad_valor:
                                            try:
                                                edad_int = int(self.astronauta_screen.edad_valor)
                                                if 1 <= edad_int <= 120:
                                                        self.astronauta_nombre = self.astronauta_screen.nombre
                                                        self.astronauta_edad = edad_int
                                                        self.astronauta_sexo = self.astronauta_screen.sexo
                                                        self.state = 'ship_select'
                                            except:
                                                pass
                                    else:
                                        if self.state == 'ship_select':
                                            self.selected_ship = self.ships_list[self.ship_selection]
                                            self.new_game()
                            else:
                                if event.key == pygame.K_UP:
                                    if self.state == 'menu':
                                        self.menu_button = (self.menu_button - 1) % 5
                                else:
                                    if event.key == pygame.K_1:
                                        if self.state == 'menu':
                                            self.difficulty = 'easy'
                                            self.difficulty_mult = 0.5
                                            self.save_game()
                                    else:
                                        if event.key == pygame.K_2:
                                            if self.state == 'menu':
                                                self.difficulty = 'normal'
                                                self.difficulty_mult = 0.8
                                                self.save_game()
                                        else:
                                            if event.key == pygame.K_3:
                                                if self.state == 'menu':
                                                    self.difficulty = 'hard'
                                                    self.difficulty_mult = 1.0
                                                    self.save_game()
                                            else:
                                                if event.key == pygame.K_DOWN:
                                                    if self.state == 'menu':
                                                        self.menu_button = (self.menu_button + 1) % 5
                                                    else:
                                                        if self.state == 'game_over':
                                                            if self.score > self.high_score:
                                                                self.high_score = self.score
                                                            self.current_planet = 0
                                                            self.score = 0
                                                            self.new_game()
                                                        else:
                                                            if self.state == 'victory':
                                                                self.save_game()
                                                                nombre = self.astronauta_nombre or self.player_name
                                                                PlayerDB.save(nombre, 'blue', self.score, self.selected_ship, self.astronauta_sexo, self.astronauta_edad, self.current_planet, self.medallas, 'GANA')
                                                                self.reset()
                                                            else:
                                                                if self.state == 'paused':
                                                                    self.paused = False
                                                                    self.state = 'playing'
                                                else:
                                                    if event.key == pygame.K_SPACE:
                                                        if self.state == 'level_start':
                                                            self.state = 'playing'
                                                        else:
                                                            if self.state == 'level_complete':
                                                                self.next_level()
                                                            else:
                                                                if self.state == 'quiz' and self.quiz_done:
                                                                    self.quiz_active = False
                                                                    if self.quiz_correct:
                                                                        self.state = 'medal_display'
                                                                    else:
                                                                        self.state = 'level_complete'
                                                                        sound_manager.play('menu_select')
                                                                else:
                                                                    if self.state == 'medal_display':
                                                                        self.state = 'level_complete'
                                                                        sound_manager.play('menu_select')
                                                                        self.medal_anim = None
                    if self.state == 'quiz' and self.quiz_active and (not self.quiz_done):
                                if event.key == pygame.K_UP:
                                    self.quiz_sel = (self.quiz_sel - 1) % len(self.quiz_q['opts'])
                                else:
                                    if event.key == pygame.K_DOWN:
                                        self.quiz_sel = (self.quiz_sel + 1) % len(self.quiz_q['opts'])
                                    else:
                                        if event.key == pygame.K_RETURN:
                                            self.quiz_done = True
                                            self.quiz_correct = self.quiz_sel == self.quiz_q['ans']
                                            if self.quiz_correct:
                                                self.medallas += 1
                                                self.medal_anim = MedalAnimation(self.current_planet)
                                                self.player.lives = min(self.player.lives + 1, 10)
                                                sound_manager.play('powerup')
                    if self.state == 'astronauta_select':
                        self.astronauta_screen.handle_key(event)
                    if self.state == 'ship_select':
                        if event.key == pygame.K_LEFT:
                            self.ship_selection = (self.ship_selection - 1) % len(self.ships_list)
                        else:
                            if event.key == pygame.K_RIGHT:
                                self.ship_selection = (self.ship_selection + 1) % len(self.ships_list)
                            else:
                                if event.key == pygame.K_BACKSPACE:
                                    self.player_name = self.player_name[:(-1)]
                                else:
                                    if len(self.player_name) < 10 and event.unicode.isalnum():
                                            self.player_name += event.unicode
            self.update()
            self.draw()
        sound_manager.stop_ambient()
        pygame.quit()
if __name__ == '__main__':
    Game().run()