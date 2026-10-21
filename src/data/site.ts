export const site = {
  /** Event framing — the page is an institutional showcase, not a career fair. */
  event: "Muestra Institucional 2026",
  eventShort: "Muestra 2026",
  institution: "Escuela Superior El Nacional",
  location: "La Carlota · Córdoba",
  title: "Astrónomos por un día · Muestra Institucional 2026 · Escuela Superior El Nacional",
  description:
    "Ocho videojuegos de astronomía que hicimos nosotros, los estudiantes de la Tecnicatura en Programación Full Stack de la Escuela Superior El Nacional, para que los nenes de primer grado aprendan jugando. La Carlota, Córdoba.",
  youtube:
    "https://www.youtube.com/embed/aYXByxcr6zE?autoplay=1&mute=1&controls=0&loop=1&playlist=aYXByxcr6zE&rel=0&modestbranding=1&playsinline=1&iv_load_policy=3",
};

/**
 * Dónde se anota la gente. `instagram` es el destino del botón de inscripción;
 * `phone` es el número para "Más información" (formato internacional para
 * `tel:`) y `phoneLabel` es cómo se muestra en pantalla.
 */
export const enrollment = {
  instagram: "https://www.instagram.com/nivelsuperiorelnacional?mdxt=OGRzNmJjOGxsbXgy",
  phone: "+543584423142" as string | null,
  phoneLabel: "358 442-3142",
};

export const metrics = [
  { icon: "🎮", target: 8, suffix: "", label: "Juegos\nterminados", delay: "reveal-d1" },
  { icon: "🎓", target: 8, suffix: "", label: "Estudiantes\nmetidos", delay: "reveal-d2" },
  { icon: "⏱️", target: 150, suffix: "+", label: "Horas\nde código", delay: "reveal-d3" },
  { icon: "👶", target: 100, suffix: "+", label: "Nenes que\njugaron", delay: "reveal-d4" },
  { icon: "📚", target: 3, suffix: "", label: "Materias\nmezcladas", delay: "reveal-d5" },
];
