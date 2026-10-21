export interface AppScreenshot {
  /** ruta en /public (ej. "/Aplicaciones/EduGestionAR_02.png") */
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
    status: "en uso",
    authors: ["Marcos Zingaretti", "Celia Cassagne", "Agustín Godoy"],
    screenshots: [
      {
        src: "/Aplicaciones/EduGestionAR_02.png",
        alt: "Panel de inicio de EduGestionAR con los indicadores de alumnos, carreras, promedio y asistencia",
        caption: "Panel de inicio",
      },
      {
        src: "/Aplicaciones/EduGestionAR_01.png",
        alt: "Pantalla de inicio de sesión de EduGestionAR",
        caption: "Inicio de sesión",
      },
      {
        src: "/Aplicaciones/EduGestionAR_03.png",
        alt: "Listado de alumnos con su carrera, año, estado y promedio",
        caption: "Alumnos",
      },
      {
        src: "/Aplicaciones/EduGestionAR_04.png",
        alt: "Gestión de materias por carrera y año, con clases y correlatividades",
        caption: "Materias",
      },
    ],
  },
];
