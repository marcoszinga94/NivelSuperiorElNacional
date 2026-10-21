export interface RouteInfo {
  href: string;
  label: string;
  icon: string;
  blurb: string;
  /** id of the group this route belongs to (see `groups`) */
  group: string;
}

export interface RouteGroup {
  id: string;
  label: string;
  icon: string;
}

/** Un proyecto de la muestra — es lo que se despliega en "Proyecto" del nav. */
export interface ProjectInfo {
  href: string;
  label: string;
  blurb: string;
}

/**
 * La home es la página de la escuela: institución, carrera e inscripción viven
 * todas en `/` con anclas (`#institucion`, `#carrera`, `#inscripcion`).
 */
export const home = { href: "/", label: "Escuela" };

/** Navigation sections — every page belongs to one of these. */
export const groups: RouteGroup[] = [
  { id: "proyecto", label: "Proyecto", icon: "🔭" },
  { id: "juegos", label: "Juegos", icon: "🎮" },
  { id: "aplicaciones", label: "Aplicaciones", icon: "📱" },
];

/** Los dos proyectos que se muestran en el desplegable "Proyecto". */
export const projects: ProjectInfo[] = [
  {
    href: "/proyecto",
    label: "Astrónomos por un día",
    blurb: "La muestra de astronomía, sus estaciones y los ocho juegos.",
  },
  {
    href: "/administrativas",
    label: "Desarrollo de aplicaciones administrativas",
    blurb: "Sistemas de gestión hechos por los estudiantes de la tecnicatura.",
  },
];

/** Ordered list of the site's routes (one per former section). */
export const routes: RouteInfo[] = [
  { href: "/proyecto", label: "Astrónomos por un día", icon: "🔭", blurb: "La muestra, el proceso, el impacto y los testimonios.", group: "proyecto" },
  { href: "/administrativas", label: "Aplicaciones administrativas", icon: "🗂️", blurb: "El proyecto de sistemas de gestión.", group: "proyecto" },

  { href: "/juegos", label: "Los juegos", icon: "🎮", blurb: "Los ocho juegos, sus autores y las herramientas.", group: "juegos" },

  { href: "/aplicaciones", label: "Aplicaciones", icon: "📱", blurb: "Las apps que ya están en uso.", group: "aplicaciones" },
];

/** Routes grouped by section, ready to render in nav / grids / footer. */
export const routeGroups = groups.map((g) => ({
  ...g,
  routes: routes.filter((r) => r.group === g.id),
}));
