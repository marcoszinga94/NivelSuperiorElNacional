import { POSICIONES_FIJAS_PARES } from './constants.js';

// Igual que ASTROS_REDUCIDOS en main.py: estos astros se dibujan al 70% de su
// tamaño nativo.
const ASTROS_REDUCIDOS = new Set([
  'CometaHalley', 'AgujeroNegro', 'Nebulosa', 'Galaxia', 'Agujero De Gusano',
]);

// Tamaños objetivo (target_w, target_h) exactamente igual que en main.py:1835‑1848.
export const ASTRO_TARGET_SIZES = {
  'Luna':              { w: 140, h: 140 },
  'Venus':             { w: 140, h: 140 },
  'Mercurio':          { w: 140, h: 140 },
  'Marte':             { w: 140, h: 140 },
  'Estacion':          { w: 120, h:  75 },
  'Jupiter':           { w: 140, h: 140 },
  'Saturno':           { w: 140, h:  76 },
  'Urano':             { w: 140, h: 140 },
  'Neptuno':           { w: 140, h: 140 },
  'Estrella':          { w:  45, h:  42 },
  'CometaHalley':      { w: 140, h: 140 },
  'AgujeroNegro':      { w: 140, h:  76 },
  'Nebulosa':          { w: 140, h: 140 },
  'Galaxia':           { w: 140, h: 140 },
  'Agujero De Gusano': { w: 140, h: 140 },
  'Exoplaneta':        { w: 140, h: 140 },
};

export class Astro {
  constructor(data, posicion, img) {
    this.nombre = data.nombre;
    this.puntos = data.puntos;
    this.img = img;
    this.x = posicion.x;
    this.y = posicion.y;
    this.seleccionado = false;
    this.radioDeteccion = 150;
    this.alpha = 0;
    this.alive = true;

    // La imagen ya viene pre-escalada al target size (desde assets.js),
    // igual que en Python donde cargar_imagen ya recibe (w, h).
    this.w = img?.width || 140;
    this.h = img?.height || 140;
    if (ASTROS_REDUCIDOS.has(this.nombre)) {
      this.w = Math.floor(this.w * 0.7);
      this.h = Math.floor(this.h * 0.7);
    }
    this.centerX = this.x;
    this.centerY = this.y;
  }

  // Rect real usado para colisión AABB (equivalente a self.rect en pygame).
  get rect() {
    return { x: this.x - this.w / 2, y: this.y - this.h / 2, w: this.w, h: this.h };
  }

  updateVisual(visorX, visorY) {
    const dx = this.x - visorX;
    const dy = this.y - visorY;
    const distancia = Math.hypot(dx, dy);
    if (distancia < this.radioDeteccion) {
      const proporcion = 1 - distancia / this.radioDeteccion;
      this.alpha = Math.floor(proporcion * 255);
      this.seleccionado = proporcion > 0.8;
    } else {
      this.alpha = 0;
      this.seleccionado = false;
    }
  }

  render(ctx) {
    if (!this.alive || !this.img || this.alpha <= 0) return;
    ctx.save();
    ctx.globalAlpha = this.alpha / 255;
    ctx.drawImage(this.img, this.x - this.w / 2, this.y - this.h / 2, this.w, this.h);
    ctx.restore();
  }

  kill() {
    this.alive = false;
  }
}

/**
 * Crea los astros del nivel indicado y los agrega a astrosGrupo (in-place),
 * igual que crear_astros() en main.py.
 *
 * IMPORTANTE: a diferencia de la versión anterior, las posiciones ocupadas
 * se calculan SIEMPRE a partir de los astros vivos que ya están en
 * astrosGrupo (igual que `ocupadas = {a.rect.center for a in astros_grupo}`
 * en Python), en vez de depender de un Set vacío pasado desde afuera. Esto
 * evita que un astro nuevo se genere exactamente encima de un astro viejo
 * que sobrevivió de una ronda anterior. De paso, se limpian del array los
 * astros ya muertos (pygame.sprite.Group los remueve automáticamente al
 * llamar kill(); aquí hay que hacerlo a mano).
 */
export function crearAstros(astrosData, astrosGrupo, nivel, assetsAstros) {
  // Compactar: quitar del array los astros ya fotografiados/matados.
  for (let i = astrosGrupo.length - 1; i >= 0; i--) {
    if (!astrosGrupo[i].alive) astrosGrupo.splice(i, 1);
  }

  const ocupadas = new Set(astrosGrupo.map(a => `${a.x},${a.y}`));

  const astrosNivel = astrosData.filter(a => a.nivel === nivel);
  const total = astrosNivel.reduce((sum, a) => sum + (a.cantidad || 1), 0);
  const disponibles = getDisponibles(ocupadas);

  let seleccionadas;
  if (total > disponibles.length) {
    console.warn(`AVISO: nivel ${nivel} requiere ${total} posiciones pero solo ` +
      `hay ${disponibles.length} disponibles; se omitirán ${total - disponibles.length} astro(s).`);
    seleccionadas = shuffle(disponibles);
  } else {
    seleccionadas = shuffle(disponibles).slice(0, total);
  }

  let idx = 0;
  for (const dato of astrosNivel) {
    for (let c = 0; c < (dato.cantidad || 1); c++) {
      if (idx >= seleccionadas.length) break;
      const p = seleccionadas[idx++];
      const img = assetsAstros[dato.nombre];
      if (!img) continue;
      const astro = new Astro(dato, p, img);
      astrosGrupo.push(astro);
    }
  }
}

function shuffle(arr) {
  const out = [...arr];
  for (let i = out.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [out[i], out[j]] = [out[j], out[i]];
  }
  return out;
}

export function getDisponibles(posicionesOcupadas) {
  return POSICIONES_FIJAS_PARES.filter(p => !posicionesOcupadas.has(`${p.x},${p.y}`));
}
