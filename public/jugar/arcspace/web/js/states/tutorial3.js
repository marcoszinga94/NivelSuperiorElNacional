import { ANCHO, ALTO, ESTADO_INTERMISION3, ESTADO_INTERMISION4, FOTOS_INICIALES } from '../constants.js';
import { ASTROS_DATA } from '../data.js';
import { Astro } from '../astro.js';

export class Tutorial3State {
  constructor(game) {
    this.game = game;
    this._t3Init = false;
    this._t3Indice = 0;
    this._t3Pts = 0;
    this._t3DemoAstros = [];
    this._t3FotoTomada = false;
  }

  enter() {
    this._t3Init = false;
    this._t3Indice = 0;
    this._t3Pts = 0;
    this._t3DemoAstros = [];
  }
  exit() {
    for (const a of this._t3DemoAstros) a.kill();
    this._t3DemoAstros = [];
  }

  update(dt) {
    const g = this.game;
    const cam = g.camara;
    if (!cam) return;

    if (!this._t3Init) {
      this._t3Init = true;
      this._t3Indice = 0;
      this._t3Pts = 0;
      const nombres = ['Luna', 'Marte', 'Venus'];
      const posiciones = [
        { x: ANCHO / 2 + 200, y: ALTO / 2 },
        { x: ANCHO / 2 - 150, y: ALTO / 2 - 80 },
        { x: ANCHO / 2 + 100, y: ALTO / 2 - 120 },
      ];
      for (let i = 0; i < nombres.length; i++) {
        const data = ASTROS_DATA.find(d => d.nombre === nombres[i]);
        if (!data) continue;
        const img = g.assetsAstros[nombres[i]];
        if (!img) continue;
        const a = new Astro(data, posiciones[i], img);
        this._t3DemoAstros.push(a);
      }
    }

    if (g.input.justPressed('Space')) {
      for (const a of g.astrosGrupo) a.kill();
      for (const a of this._t3DemoAstros) a.kill();
      this.exit();
      if (cam) { cam.x = ANCHO / 2 - 100; cam.y = ALTO / 2 - 70; cam._updateCenter(); }
      g.fotos = FOTOS_INICIALES;
      g.tiempoInicio.intermision4 = g.ticks;
      g.estadoActual = ESTADO_INTERMISION4;
      return;
    }

    if (this._t3Indice < this._t3DemoAstros.length) {
      const astro = this._t3DemoAstros[this._t3Indice];
      const dx = astro.x - cam.centerX;
      const dy = astro.y - cam.centerY;
      const dist = Math.hypot(dx, dy);
      astro.alpha = dist < astro.radioDeteccion
        ? Math.floor((1 - dist / astro.radioDeteccion) * 255) : 0;

      const llego = cam.moverHacia(astro.x, astro.y);
      if (llego && !this._t3FotoTomada) {
        this._t3FotoTomada = true;
        g.flashActivo = true;
        g.flashTiempo = g.ticks;
        g.audio.play('camara');
        this._t3Pts += 100;
        this._t3Indice++;
        if (astro) astro.kill();
        this._t3FotoTomada = false;
      }
    }

    if (g.ticks - (g.tiempoInicio.intermision3 || 0) >= 7000) {
      for (const a of g.astrosGrupo) a.kill();
      for (const a of this._t3DemoAstros) a.kill();
      this.exit();
      g.fotos = FOTOS_INICIALES;
      g.tiempoInicio.intermision4 = g.ticks;
      g.estadoActual = ESTADO_INTERMISION4;
    }
  }

  render(ctx) {
    const g = this.game;
    const cam = g.camara;
    ctx.drawImage(g.assets.getImg('fondo'), 0, 0, ANCHO, ALTO);

    for (const a of this._t3DemoAstros) {
      if (a.alive) a.render(ctx);
    }

    if (cam) cam.render(ctx, g.ticks, false);

    this._mostrarPuntos(ctx, this._t3Pts);

    const ancla = { x: ANCHO / 2, y: Math.floor(ALTO / 1.3) };
    ctx.save();
    ctx.font = '30px Silkscreen';
    ctx.textAlign = 'center';
    ctx.textBaseline = 'middle';
    ctx.fillStyle = '#fff';
    const lineas = ['CADA FOTO TE DA PUNTOS', 'COMPLETA EL OBJETIVO PARA PASAR DE NIVEL'];
    for (let i = 0; i < lineas.length; i++) {
      ctx.fillText(lineas[i], ancla.x, ancla.y - 80 + i * 40);
    }
    ctx.restore();
    g.mostrarFlash(ctx);
  }

  _mostrarPuntos(ctx, pts) {
    const barW = 20, barH = Math.floor(ALTO * 0.6);
    const x = ANCHO - 75, y = Math.floor((ALTO - barH) / 2);
    ctx.save();
    ctx.font = '30px Silkscreen';
    ctx.textAlign = 'center';
    ctx.textBaseline = 'bottom';
    ctx.fillStyle = '#fff';
    ctx.fillText('PUNTOS', x + barW / 2, y - 5);
    ctx.strokeStyle = '#404040';
    ctx.lineWidth = 2;
    ctx.strokeRect(x, y, barW, barH);
    if (pts > 0) {
      const fillH = Math.floor(barH * Math.min(pts / 500, 1));
      ctx.fillStyle = '#ffd700';
      ctx.fillRect(x, y + barH - fillH, barW, fillH);
    }
    ctx.restore();
  }
}
