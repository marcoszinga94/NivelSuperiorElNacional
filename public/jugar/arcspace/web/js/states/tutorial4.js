import { ANCHO, ALTO, ESTADO_JUGANDO, FOTOS_INICIALES } from '../constants.js';
import { ASTROS_DATA } from '../data.js';
import { crearAstros } from '../astro.js';

export class Tutorial4State {
  constructor(game) { this.game = game; }
  enter() {}
  exit() {}

  update(dt) {
    const g = this.game;
    if (g.input.justPressed('Space')) {
      g.fotos = FOTOS_INICIALES;
      if (g.camara) { g.camara.x = ANCHO / 2 - 100; g.camara.y = ALTO / 2 - 70; g.camara._updateCenter(); }
      g.ticksInicioJuego = g.ticks;
      crearAstros(ASTROS_DATA, g.astrosGrupo, g.nivel, g.assetsAstros);
      g.estadoActual = ESTADO_JUGANDO;
    }
  }

  render(ctx) {
    const g = this.game;
    ctx.drawImage(g.assets.getImg('fondo'), 0, 0, ANCHO, ALTO);

    const t = (g.ticks - (g.tiempoInicio.intermision4 || 0)) / 1000;
    const textos = [
      { t: 0, msg: 'PREPARATE', color: '#fff' },
      { t: 1, msg: '3', color: '#fff' },
      { t: 2, msg: '2', color: '#fff' },
      { t: 3, msg: '1', color: '#fff' },
      { t: 4, msg: 'A JUGAR', color: '#0f0' },
    ];
    let idxT = -1;
    for (let i = textos.length - 1; i >= 0; i--) {
      if (t >= textos[i].t) { idxT = i; break; }
    }
    if (idxT < 0 || t >= 5) {
      g.fotos = FOTOS_INICIALES;
      if (g.camara) { g.camara.x = ANCHO / 2 - 100; g.camara.y = ALTO / 2 - 70; g.camara._updateCenter(); }
      g.ticksInicioJuego = g.ticks;
      crearAstros(ASTROS_DATA, g.astrosGrupo, g.nivel, g.assetsAstros);
      g.estadoActual = ESTADO_JUGANDO;
    } else {
      const info = textos[Math.min(idxT, 4)];
      ctx.save();
      ctx.font = '80px Silkscreen';
      ctx.textAlign = 'center';
      ctx.textBaseline = 'middle';
      ctx.fillStyle = info.color;
      ctx.fillText(info.msg, ANCHO / 2, ALTO / 2);
      ctx.restore();
    }
  }
}
