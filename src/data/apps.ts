export interface AppInfo {
  /** slug corto para identificarla */
  slug: string;
  name: string;
  description: string;
  /** emoji o ruta a un logo en /public */
  icon: string;
  /** "en uso" = ya funciona en la escuela; "en desarrollo" = todavía en obra */
  status: "en uso" | "en desarrollo";
  /** link a la app, si está publicada */
  href?: string;
}

/**
 * Catálogo de aplicaciones administrativas.
 * Vacío por ahora: la página /aplicaciones muestra el estado vacío hasta que
 * carguemos la primera. Para publicar una, agregarla acá.
 */
export const apps: AppInfo[] = [];
