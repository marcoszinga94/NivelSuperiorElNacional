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

/** Navigation sections — every page belongs to one of these. */
export const groups: RouteGroup[] = [
  { id: "escuela", label: "La escuela", icon: "🏫" },
  { id: "proyecto", label: "El proyecto", icon: "🔭" },
  { id: "produccion", label: "Los juegos", icon: "🎮" },
  { id: "muestra", label: "La muestra", icon: "🎪" },
];

/** Ordered list of the site's routes (one per former section). */
export const routes: RouteInfo[] = [
  { href: "/institucion", label: "Escuela Superior El Nacional", icon: "🏫", blurb: "La escuela y la tecnicatura.", group: "escuela" },
  { href: "/carrera", label: "La carrera", icon: "🎓", blurb: "Plan, materias y duración.", group: "escuela" },
  { href: "/inscripcion", label: "Inscribite", icon: "✍️", blurb: "Cómo anotarte en la carrera.", group: "escuela" },

  { href: "/proyecto", label: "El proyecto", icon: "🔭", blurb: "Un día como astrónomos, en 5 estaciones.", group: "proyecto" },
  { href: "/proceso", label: "Cómo lo hicimos", icon: "🛠️", blurb: "Del boceto al juego, en 4 pasos.", group: "proyecto" },
  { href: "/cronologia", label: "Cronología", icon: "🗓️", blurb: "La línea de tiempo del cuatrimestre.", group: "proyecto" },

  { href: "/juegos", label: "Los juegos", icon: "🎮", blurb: "Los ocho videojuegos que hicimos.", group: "produccion" },
  { href: "/equipo", label: "Estudiantes", icon: "🧑‍💻", blurb: "Quién hizo cada juego.", group: "produccion" },
  { href: "/tecnologias", label: "Herramientas", icon: "🐍", blurb: "Python, Pygame y todo lo demás.", group: "produccion" },

  { href: "/impacto", label: "Impacto", icon: "📊", blurb: "Los números del proyecto.", group: "muestra" },
  { href: "/testimonios", label: "Testimonios", icon: "💬", blurb: "Lo que dijeron los protagonistas.", group: "muestra" },
  { href: "/competencias", label: "Competencias", icon: "💪", blurb: "Lo que nos llevamos para el trabajo.", group: "muestra" },
];

/** Routes grouped by section, ready to render in nav / grids / footer. */
export const routeGroups = groups.map((g) => ({
  ...g,
  routes: routes.filter((r) => r.group === g.id),
}));

/** Neighbours (for the prev/next links at the bottom of each page). */
export function neighbours(href: string) {
  const index = routes.findIndex((r) => r.href === href);
  return {
    prev: index > 0 ? routes[index - 1] : null,
    next: index >= 0 && index < routes.length - 1 ? routes[index + 1] : null,
  };
}
