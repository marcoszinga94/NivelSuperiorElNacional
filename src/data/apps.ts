export interface AppScreenshot {
  /** ruta en /public (ej. "/Aplicaciones/EduGestionAR_02.webp") */
  src: string;
  alt: string;
  /** epígrafe corto que se muestra debajo de la captura */
  caption: string;
}

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
  /** quiénes la desarrollaron */
  authors?: string[];
  /** tecnologías con las que está hecha */
  tech?: string[];
  /** capturas: la primera se usa como portada y las demás van a la galería */
  screenshots?: AppScreenshot[];
}

/**
 * Catálogo de aplicaciones administrativas.
 * Para publicar una, agregarla acá: la página /aplicaciones arma la ficha
 * (portada + datos + galería de capturas) a partir de estos datos.
 */
export const apps: AppInfo[] = [
  {
    slug: "edugestionar",
    name: "EduGestionAR",
    // Descripción provisoria: reemplazar por el texto final del equipo.
    description:
      "El sistema de gestión escolar de la escuela. Reúne en un solo lugar la matrícula de los alumnos, las carreras y sus materias, las notas, la regularidad y la asistencia, con usuarios y roles para el personal administrativo.",
    icon: "🎓",
    status: "en desarrollo",
    authors: ["Marcos Zingaretti", "Celia Cassagne", "Agustín Godoy"],
    screenshots: [
      {
        src: "/Aplicaciones/EduGestionAR_02.webp",
        alt: "Panel de inicio de EduGestionAR con los indicadores de alumnos, carreras, promedio y asistencia",
        caption: "Panel de inicio",
      },
      {
        src: "/Aplicaciones/EduGestionAR_01.webp",
        alt: "Pantalla de inicio de sesión de EduGestionAR",
        caption: "Inicio de sesión",
      },
      {
        src: "/Aplicaciones/EduGestionAR_03.webp",
        alt: "Listado de alumnos con su carrera, año, estado y promedio",
        caption: "Alumnos",
      },
      {
        src: "/Aplicaciones/EduGestionAR_04.webp",
        alt: "Gestión de materias por carrera y año, con clases y correlatividades",
        caption: "Materias",
      },
    ],
  },
  {
    slug: "surtech-financiero",
    name: "SurTech Financiero",
    description:
      "Una herramienta para que los alumnos de la carrera de Administración de la escuela practiquen sistemas de contabilidad en entornos realistas, junto a la profesora. Ventas, compras, stock y cierre de ejercicio con IVA, todo en un mismo sistema.",
    icon: "💹",
    status: "en desarrollo",
    authors: ["Ezequiel Stromberg", "Santiago Martino", "Aleida Appendino"],
    screenshots: [
      {
        src: "/Aplicaciones/Surtech_02.webp",
        alt: "Panel de inicio de SurTech Financiero con ventas, compras, productos y vencimientos del mes",
        caption: "Panel de inicio",
      },
      {
        src: "/Aplicaciones/Surtech_01.webp",
        alt: "Pantalla de inicio de sesión de SurTech Financiero",
        caption: "Inicio de sesión",
      },
      {
        src: "/Aplicaciones/Surtech_03.webp",
        alt: "Módulo de ventas con datos del cliente, IVA, ítems, descuentos y total",
        caption: "Ventas",
      },
      {
        src: "/Aplicaciones/Surtech_04.webp",
        alt: "Módulo de compras con datos del proveedor, artículos y resumen de IVA",
        caption: "Compras",
      },
      {
        src: "/Aplicaciones/Surtech_05.webp",
        alt: "Control de stock con código, descripción, precio y stock actual de cada artículo",
        caption: "Stock",
      },
      {
        src: "/Aplicaciones/Surtech_06.webp",
        alt: "Panel de vencimientos y recordatorios con cuotas de venta y próximas fechas",
        caption: "Recordatorios",
      },
      {
        src: "/Aplicaciones/Surtech_07.webp",
        alt: "Cierre de ejercicio con balance consolidado y saldo técnico de IVA",
        caption: "Cierre de ejercicio",
      },
    ],
  },
];
