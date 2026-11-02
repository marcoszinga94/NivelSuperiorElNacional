import { ANCHO, ALTO, ESTADO_REPORTE, FOTOS_INICIALES } from '../constants.js';

export class PauseState {
  constructor(game) { this.game = game; }
  enter() {}
  exit() {}

  update(dt) {
    const g = this.game;
    const input = g.input;

    if (input.justPressed('Escape')) {
      g.salirJuego();
      return;
    }

    const t = (g.ticks - (g.tiempoInicio.intermisionPausa || 0)) / 1000;
    if (t >= 4.0) {
      g.audio.stop('gameover');
      g.audio.stop('objetivocompleto');
      g.fotosRepInstancias = [];
      g.paginaActual = 0;
      g.fotos = FOTOS_INICIALES;
      g.pagSlideActiva = false;
      g.pagSlideSolicitada = 0;
      g.pagSlideCaptura = null;
      g.estadoActual = ESTADO_REPORTE;
    }
  }

  render(ctx) {
    const g = this.game;
    ctx.drawImage(g.assets.getImg('fondo'), 0, 0, ANCHO, ALTO);

    const objetivo = g.nivel === 5 ? g.objetivoNivel5Inicial : g.objetivoActual();
    let linea1, linea2, color;
    if (g.tipoPausa === 'objetivo') {
      color = '#ffd700';
      linea1 = 'OBJETIVO COMPLETADO';
      linea2 = `${g.puntuacion} / ${objetivo} puntos`;
    } else if (g.tipoPausa === 'fotos') {
      color = '#f66';
      linea1 = 'FOTOS AGOTADAS';
      linea2 = 'Has usado todas las fotos';
    } else {
      color = '#f66';
      linea1 = 'TIEMPO AGOTADO';
      linea2 = 'Se acabo el tiempo';
    }
    ctx.save();
    ctx.font = '80px Silkscreen';
    ctx.textAlign = 'center';
    ctx.textBaseline = 'middle';
    ctx.fillStyle = color;
    ctx.fillText(linea1, ANCHO / 2, ALTO / 2 - 30);
    ctx.font = '30px Silkscreen';
    ctx.fillStyle = '#fff';
    ctx.fillText(linea2, ANCHO / 2, ALTO / 2 + 30);
    ctx.restore();
  }
}
