import { ANCHO, ALTO, REC_W, REC_H, GAP, SEP, GROUP_W, START_Y, TAM_FLECHA, FLECHA_IZQ_X, FLECHA_DER_X, FLECHA_Y } from './constants.js';

export function escalarProporcional(w, h, targetW, targetH) {
  const escala = Math.min(targetW / w, targetH / h);
  return { w: Math.floor(w * escala), h: Math.floor(h * escala) };
}

export function escalarRellenar(w, h, targetW, targetH) {
  targetW = Math.max(Math.floor(targetW), 1);
  targetH = Math.max(Math.floor(targetH), 1);
  const escala = Math.max(targetW / w, targetH / h);
  const sw = Math.ceil(targetW / escala);
  const sh = Math.ceil(targetH / escala);
  const sx = Math.floor((w - sw) / 2);
  const sy = Math.floor((h - sh) / 2);
  return { sx, sy, sw, sh, escala };
}

let _gradienteCache = {};

export function renderGradienteTexto(ctx, texto, x, y, color1, color2, fuente) {
  const clave = `${texto}_${color1}_${color2}`;
  if (_gradienteCache[clave]) {
    ctx.drawImage(_gradienteCache[clave], x, y);
    return;
  }
  ctx.save();
  ctx.fillStyle = color1;
  ctx.font = fuente;
  const metrics = ctx.measureText(texto);
  const w = metrics.width;
  const h = parseInt(fuente) || 40;
  const offscreen = document.createElement('canvas');
  offscreen.width = w;
  offscreen.height = h * 1.5;
  const octx = offscreen.getContext('2d');
  for (let xi = 0; xi < w; xi++) {
    const t = xi / Math.max(w - 1, 1);
    const r = Math.floor(color1[0] * (1 - t) + color2[0] * t);
    const g = Math.floor(color1[1] * (1 - t) + color2[1] * t);
    const b = Math.floor(color1[2] * (1 - t) + color2[2] * t);
    octx.fillStyle = `rgb(${r},${g},${b})`;
    octx.fillRect(xi, 0, 1, h * 1.5);
  }
  octx.font = fuente;
  octx.textBaseline = 'top';
  octx.globalCompositeOperation = 'destination-in';
  octx.fillStyle = '#fff';
  octx.fillText(texto, 0, 0);
  octx.globalCompositeOperation = 'source-over';
  _gradienteCache[clave] = offscreen;
  ctx.drawImage(offscreen, x, y);
  ctx.restore();
}

let _pulseTime = 0;
export function colorPulsante(ticks) {
  const t = (ticks % 3000) / 3000;
  if (t < 1/3) {
    const lt = t * 3;
    return `rgb(${Math.floor(255 - lt * 127)},${Math.floor(165 - lt * 165)},${Math.floor(lt * 128)})`;
  } else if (t < 2/3) {
    const lt = (t - 1/3) * 3;
    return `rgb(${Math.floor(128 - lt * 128)},0,${Math.floor(128 + lt * 127)})`;
  } else {
    const lt = (t - 2/3) * 3;
    return `rgb(${Math.floor(lt * 255)},${Math.floor(lt * 165)},${Math.floor(255 - lt * 255)})`;
  }
}

let _glowCache = {};

export function dibujarBoton(ctx, texto, yCenter, xCenter, colorFondo = '#6400b4', colorTexto = '#fff', escala = 1) {
  ctx.save();
  ctx.font = '30px Silkscreen';
  const metrics = ctx.measureText(texto);
  const tw = metrics.width;
  const th = 30;
  const bw = tw + 24, bh = th + 12;
  const x = xCenter - bw / 2;
  const y = yCenter - bh / 2;
  ctx.fillStyle = colorFondo;
  roundRect(ctx, x, y, bw, bh, 8);
  ctx.fill();
  ctx.fillStyle = colorTexto;
  ctx.font = '30px Silkscreen';
  ctx.textAlign = 'center';
  ctx.textBaseline = 'middle';
  ctx.fillText(texto, xCenter, yCenter);
  ctx.restore();
  return { x, y, w: bw, h: bh };
}

export function dibujarBotonConHover(ctx, texto, yCenter, xCenter, mousePos, ticks, colorFondo = '#6400b4', colorTexto = '#fff') {
  ctx.save();
  ctx.font = '30px Silkscreen';
  const metrics = ctx.measureText(texto);
  const tw = metrics.width;
  const th = 30;
  const bw = tw + 24, bh = th + 12;
  const x = xCenter - bw / 2;
  const y = yCenter - bh / 2;
  const hover = mousePos && x <= mousePos.x && mousePos.x <= x + bw && y <= mousePos.y && mousePos.y <= y + bh;
  if (hover) {
    const pulse = 0.5 + 0.5 * Math.sin(ticks / 200);
    const alpha = Math.floor(60 + 40 * pulse);
    ctx.save();
    ctx.fillStyle = `rgba(180, 80, 255, ${alpha / 255})`;
    roundRect(ctx, x - 18, y - 9, bw + 36, bh + 18, 12);
    ctx.fill();
    ctx.restore();
  }
  ctx.fillStyle = colorFondo;
  roundRect(ctx, x, y, bw, bh, 8);
  ctx.fill();
  ctx.fillStyle = colorTexto;
  ctx.textAlign = 'center';
  ctx.textBaseline = 'middle';
  ctx.fillText(texto, xCenter, yCenter);
  ctx.restore();
  return { x, y, w: bw, h: bh, hover };
}

export function dibujarBotonHover(ctx, texto, yCenter, rightEdge, mousePos, ticks, colorFondo = '#6400b4', colorTexto = '#fff') {
  return dibujarBotonConHover(ctx, texto, yCenter, rightEdge, mousePos, ticks, colorFondo, colorTexto);
}

export function roundRect(ctx, x, y, w, h, r) {
  ctx.beginPath();
  ctx.moveTo(x + r, y);
  ctx.lineTo(x + w - r, y);
  ctx.arcTo(x + w, y, x + w, y + r, r);
  ctx.lineTo(x + w, y + h - r);
  ctx.arcTo(x + w, y + h, x + w - r, y + h, r);
  ctx.lineTo(x + r, y + h);
  ctx.arcTo(x, y + h, x, y + h - r, r);
  ctx.lineTo(x, y + r);
  ctx.arcTo(x, y, x + r, y, r);
  ctx.closePath();
}

export function wrapText(texto, fuenteWidth, anchoMax) {
  const palabras = texto.split(' ');
  const lineas = [];
  let actual = '';
  for (const p of palabras) {
    const prueba = (actual + ' ' + p).trim();
    if (fuenteWidth(prueba) <= anchoMax) {
      actual = prueba;
    } else {
      if (actual) lineas.push(actual);
      actual = p;
    }
  }
  if (actual) lineas.push(actual);
  return lineas;
}

export function calcularSlotsAlbum() {
  const totalW = 2 * GROUP_W + SEP;
  const startX = (ANCHO - totalW) / 2;
  const slots = [];
  for (let i = 0; i < 8; i++) {
    const group = Math.floor(i / 4);
    const idx = i % 4;
    const r = Math.floor(idx / 2);
    const c = idx % 2;
    const rx = startX + group * (GROUP_W + SEP) + c * (REC_W + GAP);
    const ry = START_Y + r * (REC_H + GAP);
    slots.push({ x: rx, y: ry, w: REC_W, h: REC_H });
  }
  return slots;
}

export function calcularPosicionesPagina(astrosData) {
  const slotsBase = calcularSlotsAlbum();
  const posiciones = astrosData.filter(a => a.posicion !== undefined).map(a => a.posicion);
  const maxPos = posiciones.length > 0 ? Math.max(...posiciones) : 0;
  const totalPags = Math.floor(maxPos / 8) + 1;
  const paginas = {};
  for (let p = 0; p < totalPags; p++) {
    paginas[p] = slotsBase.map(s => ({ ...s }));
  }
  return paginas;
}

export function obtenerPaginaSlot(pos) {
  return [Math.floor(pos / 8), pos % 8];
}

export function dibujarRectPunteado(ctx, x, y, w, h, color = '#000', dash = 8) {
  ctx.save();
  ctx.strokeStyle = color;
  ctx.lineWidth = 1;
  ctx.setLineDash([dash, dash]);
  ctx.strokeRect(x, y, w, h);
  ctx.restore();
}

export function dibujarFlechasAlbum(ctx, paginaActual, totalPaginas, imgArrowL, imgArrowR) {
  if (paginaActual > 0 && imgArrowL) {
    ctx.drawImage(imgArrowL, FLECHA_IZQ_X, FLECHA_Y, TAM_FLECHA, TAM_FLECHA);
  }
  if (paginaActual < totalPaginas - 1 && imgArrowR) {
    ctx.drawImage(imgArrowR, FLECHA_DER_X, FLECHA_Y, TAM_FLECHA, TAM_FLECHA);
  }
}

export function dibujarSlotsAlbum(ctx, slots, offsetPagina = 0) {
  ctx.save();
  ctx.font = '30px Silkscreen';
  ctx.textAlign = 'center';
  ctx.textBaseline = 'middle';
  for (let i = 0; i < slots.length; i++) {
    const s = slots[i];
    dibujarRectPunteado(ctx, s.x, s.y, s.w, s.h, '#000', 8);
    ctx.fillStyle = '#b4b4b4';
    ctx.fillText(String(i + offsetPagina * 8 + 1), s.x + s.w / 2, s.y + s.h / 2);
  }
  ctx.restore();
}

export function dibujarOverlaySlide(ctx, activa, captura, inicio, ticks) {
  if (!activa || !captura) return [false, null];
  const elapsed = ticks - inicio;
  const t = Math.min(elapsed / 200, 1);
  if (t >= 1) return [false, null];
  ctx.save();
  ctx.globalAlpha = 1 - t * t;
  ctx.drawImage(captura, 0, 0);
  ctx.restore();
  return [true, captura];
}
