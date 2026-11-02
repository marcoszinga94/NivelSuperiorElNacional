import { ASTRO_TARGET_SIZES } from './astro.js';

const _BASE = import.meta.url;

function imgPath(name) {
  return new URL(`../assets/Graphics/${name}`, _BASE).href;
}

function astroPath(name) {
  return imgPath(`Astros/${name}`);
}

function realPath(name) {
  return imgPath(`Reales/${name}`);
}

function fontPath(name) {
  return new URL(`../assets/Fonts/${name}`, _BASE).href;
}

function soundPath(name) {
  return new URL(`../assets/Sonido/${name}`, _BASE).href;
}

function loadImage(url) {
  return new Promise((resolve, reject) => {
    const img = new Image();
    img.onload = () => resolve(img);
    img.onerror = () => reject(new Error(`No se pudo cargar: ${url}`));
    img.src = url;
  });
}

export class AssetManager {
  constructor() {
    this.images = {};
    this.fonts = {};
    this._loaded = false;
    this._totalAssets = 0;
    this._loadedAssets = 0;
  }

  get progress() {
    return this._totalAssets > 0 ? this._loadedAssets / this._totalAssets : 0;
  }

  async loadAll(audioManager) {
    this._loadedAssets = 0;
    const assets = [];

    assets.push(loadImage(imgPath('fondo.png')).then(img => { this.images['fondo'] = img; this._loadedAssets++; }));
    assets.push(loadImage(imgPath('Fondo-Menu.png')).then(img => { this.images['fondo_menu'] = img; this._loadedAssets++; }));
    assets.push(loadImage(imgPath('Camara.png')).then(img => { this.images['camara'] = img; this._loadedAssets++; }));
    assets.push(loadImage(imgPath('UIBook.png')).then(img => { this.images['uibook'] = img; this._loadedAssets++; }));
    assets.push(loadImage(imgPath('Nacional.png')).then(img => { this.images['nacional'] = img; this._loadedAssets++; }));
    assets.push(loadImage(imgPath('Logo.webp')).then(img => { this.images['logo'] = img; this._loadedAssets++; }));

    assets.push(loadImage(imgPath('Keyboard & Mouse/Default/keyboard_arrow_up.png')).then(img => { this.images['arrow_up'] = img; this._loadedAssets++; }));
    assets.push(loadImage(imgPath('Keyboard & Mouse/Default/keyboard_arrow_down.png')).then(img => { this.images['arrow_down'] = img; this._loadedAssets++; }));
    assets.push(loadImage(imgPath('Keyboard & Mouse/Default/keyboard_arrow_left.png')).then(img => { this.images['arrow_left'] = img; this._loadedAssets++; }));
    assets.push(loadImage(imgPath('Keyboard & Mouse/Default/keyboard_arrow_right.png')).then(img => { this.images['arrow_right'] = img; this._loadedAssets++; }));
    assets.push(loadImage(imgPath('Keyboard & Mouse/Default/keyboard_m.png')).then(img => { this.images['key_m'] = img; this._loadedAssets++; }));
    assets.push(loadImage(imgPath('Keyboard & Mouse/Default/mouse_left.png')).then(img => { this.images['mouse_left'] = img; this._loadedAssets++; }));
    assets.push(loadImage(imgPath('Keyboard & Mouse/espacio-key.png')).then(img => { this.images['space_key'] = img; this._loadedAssets++; }));

    const astros = [
      'Luna', 'Venus', 'Mercurio', 'Marte', 'Estacion', 'Jupiter', 'Saturno',
      'Urano', 'Neptuno', 'Estrella', 'Cometa', 'Agujero', 'Nebulosa', 'Galaxia',
      'Gusano', 'Exoplaneta'
    ];
    const astroNames = [
      'Luna', 'Venus', 'Mercurio', 'Marte', 'Estacion', 'Jupiter', 'Saturno',
      'Urano', 'Neptuno', 'Estrella', 'CometaHalley', 'AgujeroNegro', 'Nebulosa', 'Galaxia',
      'Agujero De Gusano', 'Exoplaneta'
    ];
    for (let i = 0; i < astros.length; i++) {
      const name = astroNames[i];
      const file = astros[i];
      const target = ASTRO_TARGET_SIZES[name] || { w: 140, h: 140 };
      assets.push(loadImage(astroPath(`${file}.png`)).then(img => {
        const c = document.createElement('canvas');
        c.width = target.w;
        c.height = target.h;
        c.getContext('2d').drawImage(img, 0, 0, target.w, target.h);
        this.images[`astro_${name}`] = c;
        this._loadedAssets++;
      }));
    }

    function escalarReal(img) {
      const maxLado = 800;
      if (img.width <= maxLado && img.height <= maxLado) return img;
      const sc = maxLado / Math.max(img.width, img.height);
      const w = Math.floor(img.width * sc);
      const h = Math.floor(img.height * sc);
      const c = document.createElement('canvas');
      c.width = w; c.height = h;
      c.getContext('2d').drawImage(img, 0, 0, w, h);
      return c;
    }
    const reales = [
      'Luna-Real', 'Venus-Real', 'Mercurio-Real', 'Marte-Real', 'Estacion-Real',
      'Jupiter-Real', 'Saturno-Real', 'Urano-Real', 'Neptuno-Real', 'Estrella-Real',
      'Cometa-Real', 'Agujero-Real', 'Nebulosa-Real', 'Galaxia-Real', 'Gusano-Real',
      'Exoplaneta-Real'
    ];
    for (const r of reales) {
      assets.push(loadImage(realPath(`${r}.webp`)).then(img => { this.images[`real_${r}`] = escalarReal(img); this._loadedAssets++; }));
    }

    const sounds = [
      ['camara', 'camara.mp3', 0.6],
      ['objetivocompleto', 'objetivocompleto.ogg', 0.7],
      ['gameover', 'gameover.mp3', 0.7],
      ['felicitaciones', 'felicitaciones.mp3', 0.6],
      ['giro', 'whoshfinal.mp3', 0.5],
      ['revelada', 'revelada.wav', 0.7],
      ['pegado', 'pegado.mp3', 0.6],
      ['cambio_pagina', 'Cambio-Pagina.wav', 0.5],
    ];
    if (audioManager) {
      for (const [key, file, vol] of sounds) {
        assets.push(audioManager.loadBuffer(key, soundPath(file), vol));
      }
    }

    this._totalAssets = assets.length;
    return Promise.allSettled(assets);
  }

  getImg(key) { return this.images[key] || null; }

  getAstroImg(name) { return this.images[`astro_${name}`] || null; }

  getRealImg(name, realName) {
    const target = realName || `${name}-Real`;
    const realKey = `real_${target}`;
    if (this.images[realKey]) return this.images[realKey];
    const altKey = `real_${name}`;
    return this.images[altKey] || null;
  }
}
