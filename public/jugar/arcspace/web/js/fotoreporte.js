import { ANCHO, ALTO } from './constants.js';
import { escalarRellenar } from './render.js';

export class FotoReporte {
  constructor(clave, texto, rectMin, rectDest, pixelImg, realImg, nombreMostrar) {
    this.clave = clave;
    this.nombreMostrar = nombreMostrar || clave;
    this.textoAstro = texto;
    this.rectMin = rectMin;
    this.rectDest = rectDest;
    this.pixelImg = pixelImg;
    this.realImg = realImg;
    this.estado = 'oculta_en_libro';
    this.angulo = 0;
    this.hover = false;
    this.pagina = 0;
    this._sonidoGiroEmitido = false;
    this._sonidoPegadoEmitido = false;

    const pw = pixelImg ? pixelImg.width : 100;
    const ph = pixelImg ? pixelImg.height : 100;
    const escala = Math.min(rectDest.w / pw, rectDest.h / ph);
    this.tamanioNormal = { w: Math.floor(pw * escala), h: Math.floor(ph * escala) };
    this.tamanioAnim = { w: Math.floor(pw * escala * 3), h: Math.floor(ph * escala * 3) };
    this.tamanioRelleno = { w: rectDest.w, h: rectDest.h };

    this.x = rectMin.x + rectMin.w / 2;
    this.y = rectMin.y + rectMin.h / 2;
    this.w = this.tamanioNormal.w;
    this.h = this.tamanioNormal.h;
  }

  get rect() {
    return { x: this.x - this.w / 2, y: this.y - this.h / 2, w: this.w, h: this.h };
  }

  update(audio, ticks) {
    if (this.estado === 'girando') this._animarGiro(audio, ticks);
    else if (this.estado === 'pegando') this._animarPegado(audio, ticks);
  }

  _animarGiro(audio, ticks) {
    if (!this._sonidoGiroEmitido) {
      if (audio) audio.play('giro');
      this._sonidoGiroEmitido = true;
    }
    const prevAng = this.velocidadAngular || 0.02;
    this.velocidadAngular = Math.min(prevAng + 0.003, 0.3);
    if (!this._giroStartAng) this._giroStartAng = this.angulo;
    this.angulo += this.velocidadAngular;
    const seno = Math.sin(this.angulo);
    const factorAncho = Math.abs(seno);
    let nuevoAncho = Math.max(Math.floor(this.tamanioAnim.w * factorAncho), 1);

    const img = seno >= 0 ? this.pixelImg : (this._flippedPixelImg || (() => {
      const c = document.createElement('canvas');
      c.width = this.pixelImg.width;
      c.height = this.pixelImg.height;
      const ctx = c.getContext('2d');
      ctx.scale(-1, 1);
      ctx.drawImage(this.pixelImg, -c.width, 0);
      this._flippedPixelImg = c;
      return c;
    })());

    this.w = nuevoAncho;
    this.h = this.tamanioAnim.h;
    this.x = ANCHO / 2;
    this.y = ALTO / 2;

    if (this.angulo >= 10 * Math.PI && Math.abs(seno) > 0.95) {
      if (audio) { audio.stop('giro'); audio.play('revelada'); }
      this._flashInicio = ticks;
      this.w = this.tamanioAnim.w;
      this.h = this.tamanioAnim.h;
      this.x = ANCHO / 2;
      this.y = ALTO / 2;
      this.estado = 'revelada';
      this._sonidoGiroEmitido = false;
      this._giroStartAng = undefined;
    }
  }

  pegar(audio, instantaneo = false, ticks) {
    if (instantaneo) {
      this.w = this.tamanioRelleno.w;
      this.h = this.tamanioRelleno.h;
      this.x = this.rectDest.x + this.rectDest.w / 2;
      this.y = this.rectDest.y + this.rectDest.h / 2;
      this.estado = 'pegada';
      return;
    }
    this._pegandoInicio = ticks;
    this._pegandoDuracion = 500;
    this._pegandoStartCenter = { x: ANCHO / 2, y: ALTO / 2 };
    this._pegandoEndCenter = { x: this.rectDest.x + this.rectDest.w / 2, y: this.rectDest.y + this.rectDest.h / 2 };
    this._pegandoStartSize = { w: this.tamanioAnim.w, h: this.tamanioAnim.h };
    this._pegandoEndSize = { w: this.tamanioRelleno.w, h: this.tamanioRelleno.h };
    this.estado = 'pegando';
    this._sonidoPegadoEmitido = false;
  }

  _animarPegado(audio, ticks) {
    const elapsed = ticks - this._pegandoInicio;
    let t = Math.min(elapsed / this._pegandoDuracion, 1.0);
    let ease = 1 - Math.pow(1 - t, 3);
    if (t > 0.8) {
      const bt = (t - 0.8) / 0.2;
      ease += 0.08 * Math.sin(bt * Math.PI * 3) * (1 - bt);
    }
    ease = Math.min(ease, 1.0);

    this.x = this._pegandoStartCenter.x + (this._pegandoEndCenter.x - this._pegandoStartCenter.x) * ease;
    this.y = this._pegandoStartCenter.y + (this._pegandoEndCenter.y - this._pegandoStartCenter.y) * ease;
    this.w = Math.max(Math.floor(this._pegandoStartSize.w + (this._pegandoEndSize.w - this._pegandoStartSize.w) * ease), 1);
    this.h = Math.max(Math.floor(this._pegandoStartSize.h + (this._pegandoEndSize.h - this._pegandoStartSize.h) * ease), 1);

    if (t >= 1.0) {
      if (!this._sonidoPegadoEmitido) {
        if (audio) audio.play('pegado');
        this._sonidoPegadoEmitido = true;
      }
      this.w = this.tamanioRelleno.w;
      this.h = this.tamanioRelleno.h;
      this.x = this._pegandoEndCenter.x;
      this.y = this._pegandoEndCenter.y;
      this.estado = 'pegada';
    }
  }

  revelarAmpliado() {
    this.w = this.tamanioAnim.w;
    this.h = this.tamanioAnim.h;
    this.x = ANCHO / 2;
    this.y = ALTO / 2;
    this.estado = 'revelada';
  }

  render(ctx, ticks) {
    if (this.estado === 'oculta_en_libro' || !this.realImg) return;
    const img = (this.estado === 'revelada' || this.estado === 'pegando' || this.estado === 'pegada') ? this.realImg : this.pixelImg;
    if (!img) return;

    ctx.save();
    if (this.estado === 'girando') {
      const imgSrc = Math.sin(this.angulo) >= 0 ? this.pixelImg : this._flippedPixelImg;
      if (imgSrc) {
        ctx.drawImage(imgSrc, this.x - this.w / 2, this.y - this.h / 2, this.w, this.h);
      }
    } else {
      if (this.estado === 'pegada') {
        const r = escalarRellenar(img.width, img.height, this.w, this.h);
        ctx.drawImage(img, r.sx, r.sy, r.sw, r.sh, this.x - this.w / 2, this.y - this.h / 2, this.w, this.h);
      } else if (this.estado === 'revelada') {
        const r = escalarRellenar(img.width, img.height, this.w, this.h);
        ctx.drawImage(img, r.sx, r.sy, r.sw, r.sh, this.x - this.w / 2, this.y - this.h / 2, this.w, this.h);
        if (this._flashInicio && ticks - this._flashInicio < 600) {
          const fa = Math.floor(255 * (1 - (ticks - this._flashInicio) / 600));
          ctx.fillStyle = `rgba(255,255,255,${fa/255})`;
          ctx.fillRect(this.x - this.w / 2, this.y - this.h / 2, this.w, this.h);
        }
      } else {
        ctx.drawImage(img, this.x - this.w / 2, this.y - this.h / 2, this.w, this.h);
      }
    }
    ctx.restore();
  }
}
