export const ANCHO = 1280;
export const ALTO = 720;

export const ESTADO_MENU              = "menu";
export const ESTADO_INTERMISION1      = "intermision1";
export const ESTADO_INTERMISION2      = "intermision2";
export const ESTADO_INTERMISION3      = "intermision3";
export const ESTADO_INTERMISION4      = "intermision4";
export const ESTADO_INTERMISION_MEJORA = "intermision_mejora";
export const ESTADO_INTERMISION_PAUSA  = "intermision_pausa";
export const ESTADO_JUGANDO           = "jugando";
export const ESTADO_REPORTE           = "reporte";
export const ESTADO_PUNTAJES          = "puntajes";
export const ESTADO_ALBUM_PUNTAJES    = "album_puntajes";
export const ESTADO_FELICITACION      = "felicitacion";

export const ESTADOS_INTERMISION = [
  ESTADO_INTERMISION1, ESTADO_INTERMISION2,
  ESTADO_INTERMISION3, ESTADO_INTERMISION4,
  ESTADO_INTERMISION_MEJORA, ESTADO_INTERMISION_PAUSA,
];

export const OBJETIVOS_POR_NIVEL = {1: 500, 2: 1000, 3: 2000, 4: 3500, 5: 5000};
export const TIEMPO_INICIAL = 60;
export const FOTOS_INICIALES = 5;

export const POSICIONES_FIJAS = [
  100, 165, 307, 165, 514, 165, 721, 165, 928, 165, 1135, 165,
  100, 305, 307, 305, 514, 305, 721, 305, 928, 305, 1135, 305,
  100, 445, 307, 445, 514, 445, 721, 445, 928, 445, 1135, 445,
  100, 585, 307, 585, 514, 585, 721, 585, 928, 585, 1135, 585,
];
export const POSICIONES_FIJAS_PARES = [];
for (let i = 0; i < POSICIONES_FIJAS.length; i += 2) {
  POSICIONES_FIJAS_PARES.push({x: POSICIONES_FIJAS[i], y: POSICIONES_FIJAS[i+1]});
}

export const REC_W = 130, REC_H = 130, GAP = 30, SEP = 150;
export const GROUP_W = 2 * REC_W + GAP;
export const START_Y = 275;
export const LIBRO_BOTTOM = 670;
export const MARGEN_BOOK = 12;
export const TAM_FLECHA = 50;
export const FLECHA_IZQ_X = ANCHO / 2 - 415 + MARGEN_BOOK + 30;
export const FLECHA_DER_X = ANCHO / 2 + 415 - MARGEN_BOOK - TAM_FLECHA - 30;
export const FLECHA_Y = LIBRO_BOTTOM - MARGEN_BOOK - TAM_FLECHA - 40;

export const PAG_SLIDE_DURACION = 200;
export const MAX_NOMBRE = 10;
