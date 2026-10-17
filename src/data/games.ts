export interface Game {
  id: string;
  title: string;
  icon: string;
  category: string;
  weeks: string;
  featuredBadge?: string;
  /** CSS gradient used for the preview background */
  gradient: string;
  /** Demo video file (relative to /public). Empty string = no demo yet. */
  demo: string;
  /** Short line shown on the card, written in our own voice */
  objective: string;
  /** Longer description shown on the card */
  description: string;
  tech: string[];
  /** Student / author */
  author: string;
  initials: string;
  role: string;
  /** Avatar + card accent gradient */
  accent: string;
  /** The student explaining their game, first person */
  studentDescription: string;
  quote: string;
  studentTech: string[];
}

export const games: Game[] = [
  {
    id: "boom-cosmico",
    title: "Boom Cósmico",
    icon: "🚀",
    category: "Acción",
    weeks: "~3 sem.",
    gradient: "linear-gradient(135deg,#0d1230 0%,#1a0840 50%,#060820 100%)",
    demo: "benja.mp4",
    objective: "Queríamos que el nene coordinara la mano y, de paso, reconociera constelaciones sin darse cuenta.",
    description:
      "Manejás un cohete que junta estrellas para armar constelaciones mientras esquivás meteoritos. Hay poderes especiales, varios niveles y el puntaje sube a medida que jugás.",
    tech: ["Python", "Pygame"],
    author: "Benjamín Basiluk",
    initials: "BB",
    role: "Desarrollador · Acción",
    accent: "linear-gradient(135deg,#4f7fff,#7c4dff)",
    studentDescription:
      "Hice un juego de acción: manejás un cohete, juntás estrellas para armar constelaciones y esquivás meteoritos. Lo que más me costó fue calibrar la dificultad.",
    quote:
      "El desafío más grande fue hacer que el juego se sintiera justo para un nene de seis años: si era muy difícil se frustraba, si era muy fácil se aburría.",
    studentTech: ["Python", "Pygame", "Sprites", "Físicas 2D"],
  },
  {
    id: "arcspace",
    title: "ArcSpace",
    icon: "🔭",
    category: "Exploración",
    weeks: "~3 sem.",
    gradient: "linear-gradient(135deg,#0a1a30 0%,#0d2040 50%,#061018 100%)",
    demo: "ulises.mp4",
    objective: "Queríamos que los chicos reconocieran planetas y astros mirando, sin depender de leer.",
    description:
      "Te ponés el traje de astrónomo, agarrás un telescopio digital y fotografiás planetas, estrellas y lo que se cruce. Cada foto suma a tu álbum cósmico personal.",
    tech: ["Python", "Pygame"],
    author: "Ulises Sosa",
    initials: "US",
    role: "Desarrollador · Exploración",
    accent: "linear-gradient(135deg,#00c8ff,#4f7fff)",
    studentDescription:
      "Hice un juego donde el nene es un astrónomo con un telescopio digital que fotografía astros para armar su álbum.",
    quote:
      "Quería que el nene sintiera que estaba descubriendo algo real, que cada astro que fotografiaba era un logro genuino de su exploración.",
    studentTech: ["Python", "Pygame", "Animaciones", "Sistema de colección"],
  },
  {
    id: "solar-defender",
    title: "SolarDefender",
    icon: "🛡️",
    category: "Arcade",
    weeks: "~4 sem.",
    gradient: "linear-gradient(135deg,#1a0a0a 0%,#300d20 50%,#0f0810 100%)",
    demo: "nahuel.mp4",
    objective: "Queríamos que aprendieran los planetas sin darse cuenta, jugando.",
    description:
      "Un arcade donde viajás de planeta en planeta (Mercurio, Venus, Marte, Júpiter y Saturno) liquidando oleadas de naves. Cada planeta termina con un jefe de tres fases.",
    tech: ["Python", "Pygame"],
    author: "Nahuel Pedraza",
    initials: "NP",
    role: "Desarrollador · Arcade",
    accent: "linear-gradient(135deg,#ff6b6b,#ff9f43)",
    studentDescription:
      "Hice un arcade en el que viajás por los planetas eliminando oleadas de enemigos, con datos de cada uno.",
    quote:
      "Lo más desafiante fue que el juego enseñara los planetas sin que el nene se diera cuenta de que estaba aprendiendo. Que fuera primero divertido.",
    studentTech: ["Python", "Pygame", "IA enemigos", "Niveles"],
  },
  {
    id: "cielo-cordobes",
    title: "El Cielo Cordobés",
    icon: "⭐",
    category: "Educativo",
    weeks: "~3 sem.",
    featuredBadge: "Local",
    gradient: "linear-gradient(135deg,#0a1020 0%,#101828 50%,#080c18 100%)",
    demo: "aleida.mp4",
    objective: "Queríamos enseñar las constelaciones que se ven desde Córdoba, sin marear a nadie.",
    description:
      "Lumina, una estrella exploradora, te guía para conectar estrellas en el orden correcto y armar las 12 constelaciones del cielo cordobés. Con datos curiosos cada vez que acertás.",
    tech: ["Python", "Pygame"],
    author: "Aleida Appendino",
    initials: "AA",
    role: "Desarrolladora · Educativo",
    accent: "linear-gradient(135deg,#4fbb7c,#00c8ff)",
    studentDescription:
      "Hice un juego sobre las constelaciones que se ven desde Córdoba, con Lumina, una estrella que te guía.",
    quote:
      "Elegí hacer el cielo de Córdoba porque quería que los chicos supieran que la astronomía también la pueden vivir desde su patio, mirando arriba.",
    studentTech: ["Python", "Pygame", "Personaje guía", "Datos astronómicos"],
  },
  {
    id: "sistema-solar",
    title: "Sistema Solar Interactivo",
    icon: "🪐",
    category: "Simulación",
    weeks: "~5 sem.",
    gradient: "linear-gradient(135deg,#080c20 0%,#0d1428 50%,#060a14 100%)",
    demo: "",
    objective: "Queríamos mostrar el Sistema Solar con datos reales, pero que se entienda.",
    description:
      "Una simulación en tiempo real del Sistema Solar con datos orbitales reales. Podés mirar cada planeta, sus lunas y las velocidades de traslación, y hacer clic para leer los datos.",
    tech: ["Python", "Pygame"],
    author: "Marcos Zingaretti",
    initials: "MZ",
    role: "Desarrollador · Simulación",
    accent: "linear-gradient(135deg,#7c4dff,#4f7fff)",
    studentDescription:
      "Hice una simulación del Sistema Solar en tiempo real, con los movimientos y los datos de cada planeta.",
    quote:
      "El Sistema Solar tiene proporciones imposibles de representar a escala real. Aprendí que en visualización científica hay que elegir entre precisión y comprensión.",
    studentTech: ["Python", "Pygame", "Simulación orbital", "Datos NASA"],
  },
  {
    id: "cartas-espaciales",
    title: "Cartas Espaciales",
    icon: "🃏",
    category: "Memoria",
    weeks: "~2 sem.",
    gradient: "linear-gradient(135deg,#0a0820 0%,#14102a 50%,#060814 100%)",
    demo: "ezequiel.mp4",
    objective: "Queríamos que entrenaran la memoria y reconocieran astros.",
    description:
      "El clásico juego de memoria, pero en el espacio. Encontrá todos los pares de planetas y astros antes de quedarte sin intentos. Y ojo, porque aparecen peligros sorpresa.",
    tech: ["Python", "Pygame"],
    author: "Ezequiel Strombe",
    initials: "ES",
    role: "Desarrollador · Memoria",
    accent: "linear-gradient(135deg,#ff9f43,#ff6b6b)",
    studentDescription:
      "Hice el clásico juego de memoria en el espacio. Pensar cuántas cartas poner costó más de lo que parecía.",
    quote:
      "El juego de memoria parece simple pero requirió pensar mucho la dificultad: demasiadas cartas abruman a un chico de seis años, muy pocas lo aburren.",
    studentTech: ["Python", "Pygame", "Lógica de pares", "Eventos aleatorios"],
  },
  {
    id: "preguntados-kids",
    title: "Preguntados Kids 🚀",
    icon: "💡",
    category: "Trivia",
    weeks: "~3 sem.",
    featuredBadge: "Con audio",
    gradient: "linear-gradient(135deg,#0c1a08 0%,#142410 50%,#080c06 100%)",
    demo: "santiago.mp4",
    objective: "Queríamos llevar la astronomía a nenes que todavía no leen bien.",
    description:
      "Una trivia de astronomía pensada para primer grado. Colores fuertes, una voz que te guía, tres opciones para elegir y recompensas que no castigan el error.",
    tech: ["Python", "Pygame", "Audio"],
    author: "Santiago Martino",
    initials: "SM",
    role: "Desarrollador · UX + Audio",
    accent: "linear-gradient(135deg,#4fbb7c,#4f7fff)",
    studentDescription:
      "Hice una trivia de astronomía para nenes de 6 años, con guía de audio y opciones con dibujos.",
    quote:
      "Aprendí que diseñar para niños que todavía no leen bien es un desafío de UX enorme. Todo tiene que comunicarse visualmente y con sonido, sin depender del texto.",
    studentTech: ["Python", "Pygame", "Audio engine", "UX inclusivo"],
  },
  {
    id: "viaje-galactico",
    title: "¡Viaje Galáctico!",
    icon: "🌌",
    category: "Aventura",
    weeks: "~4 sem.",
    gradient: "linear-gradient(135deg,#0a1420 0%,#0d1c30 50%,#060e18 100%)",
    demo: "agus godoy.mp4",
    objective: "Queríamos que fuera un viaje, no una lista de planetas.",
    description:
      "Una aventura por distintos sectores del universo. Vas descubriendo planetas, nebulosas y fenómenos raros, con un mapa estelar que se abre a medida que avanzás.",
    tech: ["Python", "Pygame"],
    author: "Agustín Godoy",
    initials: "AG",
    role: "Desarrollador · Aventura",
    accent: "linear-gradient(135deg,#00c8ff,#7c4dff)",
    studentDescription:
      "Hice una aventura en la que viajás por el universo descubriendo planetas, nebulosas y fenómenos.",
    quote:
      "Quería que el juego sintiera como un viaje de verdad. Que cada sector del universo fuera visualmente diferente y que el jugador tuviera razones para seguir explorando.",
    studentTech: ["Python", "Pygame", "Exploración", "Mapa estelar"],
  },
];
