import { ANCHO, ALTO, ESTADO_INTERMISION4 } from '../constants.js';

export class MejoraState {
  constructor(game) { this.game = game; }
  enter() {}
  exit() {}

  update(dt) {
    const g = this.game;
    if (g.input.justPressed('Space')) {
      g.tiempoInicio.intermision4 = g.ticks;
      g.estadoActual = ESTADO_INTERMISION4;
      return;
    }
    const t = (g.ticks - (g.tiempoInicio.intermisionMejora || 0)) / 1000;
    if (t >= 3) {
      g.tiempoInicio.intermision4 = g.ticks;
      g.estadoActual = ESTADO_INTERMISION4;
    }
  }

  render(ctx) {
    const g = this.game;
    ctx.drawImage(g.assets.getImg('fondo'), 0, 0, ANCHO, ALTO);

    const t = (g.ticks - (g.tiempoInicio.intermisionMejora || 0)) / 1000;
    ctx.save();
    ctx.textAlign = 'center';
    ctx.textBaseline = 'middle';
    if (t < 3) {
      if (g.objetivoCompletado) {
        ctx.font = '50px Silkscreen';
        ctx.fillStyle = '#ffd700';
        ctx.fillText('Camara mejorada', ANCHO / 2, ALTO / 2 - 20);
        ctx.font = '30px Silkscreen';
        ctx.fillStyle = '#fff';
        ctx.fillText('Ahora puedes ver mas lejos', ANCHO / 2, ALTO / 2 + 30);
      } else {
        ctx.font = '50px Silkscreen';
        ctx.fillStyle = '#f66';
        ctx.fillText('INTENTA DE NUEVO', ANCHO / 2, ALTO / 2 - 20);
        ctx.font = '30px Silkscreen';
        ctx.fillStyle = '#fff';
        ctx.fillText('Vuelve a intentar el nivel', ANCHO / 2, ALTO / 2 + 30);
      }
    } else {
      g.tiempoInicio.intermision4 = g.ticks;
      g.estadoActual = ESTADO_INTERMISION4;
    }
    ctx.restore();
  }
}
