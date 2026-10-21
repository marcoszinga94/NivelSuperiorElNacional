export interface Game {
  id: string;
  title: string;
  icon: string;
  category: string;
  weeks?: string;
  featuredBadge?: string;
  /** CSS gradient used for the preview background */
  gradient: string;
  /**
   * Slug of the browser build living in `public/jugar/<web>/juego/`.
   * `null` = the game cannot be played online yet (see /jugar/<web>).
   */
  web: string | null;
  /** Windows executable in `public/Ejecutadores/`. `null` = nobody handed it in. */
  exe: string | null;
  /**
   * Logo de la tarjeta. Por defecto sale de ese mismo `.exe`
   * (`public/juegos/icono/<slug>.png`), tal como lo muestra Windows; si el arte
   * original que entregó el estudiante está mejor, apunta a ese archivo.
   * `null` = no hay logo usable y la tarjeta cae al emoji.
   */
  logo: string | null;
  /** Keyboard controls shown next to the player. */
  controls: string;
  /**
   * The original is a desktop app (Tkinter), so the browser version is a port
   * to Pygame that keeps its rules and assets. Shown as a note on the page.
   */
  ported?: boolean;
  /** Short line shown on the card, written in our own voice */
  objective: string;
  /** Longer description shown on the card */
  description: string;
  tech: string[];
  /** Student / author */
  author: string;
  initials: string;
  /** Segundo autor, si el juego lo hicieron entre dos. */
  coInitials?: string;
  role: string;
  /** Avatar + card accent gradient */
  accent: string;
  /** Color del avatar del segundo autor */
  coAccent?: string;
  /** The student explaining their game, first person. Missing when we have no words from them. */
  studentDescription?: string;
  quote?: string;
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
    web: "boom-cosmico",
    exe: "Boom Cosmico.exe",
    // El arte que entregó el estudiante está en mejor resolución que el ícono
    // que quedó dentro del .exe, así que la tarjeta usa ese archivo.
    logo: "/juegos/boom-cosmico.png",
    controls:
      "Escribí tu nombre y apretá ENTER para empezar. Manejás el cohete con las flechas y disparás con ESPACIO.",
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
    web: "arcspace",
    exe: "ARCSPACE.exe",
    // El .exe solo trae el ícono genérico de PyInstaller, así que la tarjeta
    // arma el logo con lo que sí es del juego: el fondo del menú y la tipografía
    // Silkscreen que viajan adentro del ejecutable, con el título tal cual.
    logo: "/juegos/arcspace-logo.png",
    controls:
      "Escribí tu nombre con el teclado y apretá ESPACIO para empezar. ESC vuelve al menú y con PUNTAJES ves la tabla de mejores puntajes.",
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
    web: "solar-defender",
    exe: "Solar Defender.exe",
    // Este .exe tiene el recurso de icono vacío (0 bytes), así que el logo sale
    // del arte que el juego trae adentro (`assets/splash.png`), recortado en
    // círculo y sin el fondo blanco.
    logo: "/juegos/solar-defender-logo.png",
    controls:
      "Te movés con las flechas y la nave dispara sola. ENTER confirma en los menús, P pausa, ESC vuelve atrás y con 1, 2 o 3 elegís la dificultad.",
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
    web: "cielo-cordobes",
    exe: "el cielo cordobez.exe",
    logo: "/juegos/icono/cielo-cordobes.png",
    controls:
      "Escribí tu nombre y elegí con el mouse o las flechas entre JUGAR, RANKING y SALIR. Después conectás las estrellas en orden para armar cada constelación.",
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
    id: "cartas-espaciales",
    title: "Cartas Espaciales",
    icon: "🃏",
    category: "Memoria",
    weeks: "~2 sem.",
    gradient: "linear-gradient(135deg,#0a0820 0%,#14102a 50%,#060814 100%)",
    web: "cartas-espaciales",
    exe: "cartas espaciales.exe",
    logo: "/juegos/icono/cartas-espaciales.png",
    controls:
      "Escribí tu nombre y apretá ENTER. Después hacés clic en las cartas para encontrar los 7 pares. Si aparecen los 3 aliens perdés, y el comodín los vuelve a tapar. M = instrucciones, R = records.",
    ported: true,
    objective: "Queríamos que entrenaran la memoria y reconocieran astros.",
    description:
      "El clásico juego de memoria, pero en el espacio. Encontrá todos los pares de planetas y astros antes de quedarte sin intentos. Y ojo, porque aparecen peligros sorpresa.",
    tech: ["Python", "Pygame"],
    author: "Ezequiel Stromberg y Celia Cassagne",
    initials: "ES",
    coInitials: "CC",
    role: "Desarrollador · Memoria",
    accent: "linear-gradient(135deg,#ff9f43,#ff6b6b)",
    coAccent: "linear-gradient(135deg,#00c8ff,#4fbb7c)",
    studentDescription:
      "Hicimos el clásico juego de memoria en el espacio. Pensar cuántas cartas poner costó más de lo que parecía.",
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
    web: "preguntados-kids",
    exe: "Astro-Kids.exe",
    logo: "/juegos/icono/preguntados-kids.png",
    controls:
      "Elegís la respuesta con el mouse. Un acierto suma y un error no te saca del juego: la idea es que se animen a probar.",
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
    web: "viaje-galactico",
    exe: "íViaje Galactico!.exe",
    logo: "/juegos/icono/viaje-galactico.png",
    controls:
      "Tocá cada cuerpo celeste para leer su historia y escucharla en voz alta. C abre el cuestionario, V vuelve a escuchar y ESC cierra la ficha.",
    ported: true,
    objective: "Queríamos que fuera un viaje, no una lista de planetas.",
    description:
      "Una aventura por distintos sectores del universo. Vas descubriendo planetas, nebulosas y fenómenos raros, con un mapa estelar que se abre a medida que avanzás.",
    tech: ["Python", "Pygame"],
    author: "Marcos Zingaretti",
    initials: "MZ",
    role: "Desarrollador · Aventura",
    accent: "linear-gradient(135deg,#00c8ff,#7c4dff)",
    studentDescription:
      "Hice una aventura en la que viajás por el universo descubriendo planetas, nebulosas y fenómenos.",
    quote:
      "Quería que el juego sintiera como un viaje de verdad. Que cada sector del universo fuera visualmente diferente y que el jugador tuviera razones para seguir explorando.",
    studentTech: ["Python", "Pygame", "Exploración", "Mapa estelar"],
  },
  {
    id: "stellar-scrap",
    title: "Stellar Scrap",
    icon: "🛰️",
    category: "Arcade",
    gradient: "linear-gradient(135deg,#04121f 0%,#0a2038 50%,#040c18 100%)",
    web: "stellar-scrap",
    exe: "Stellar Scrap.exe",
    logo: "/juegos/icono/stellar-scrap.png",
    controls:
      "Escribí tu nombre y elegí JUGAR. Manejás la nave con el mouse o las flechas, juntás chatarra espacial y esquivás asteroides. Con INSTRUCCIONES ves el detalle y RESET RANKING borra la tabla.",
    objective: "Quería un juego donde limpiar el espacio fuera la excusa para sumar puntos.",
    description:
      "Manejás una nave que limpia el espacio: juntás baterías, cápsulas, paneles solares y satélites mientras esquivás asteroides. Hay varios niveles de dificultad, escudo, vidas y un robot de monitoreo que te sigue el puntaje. Al final queda el ranking de los mejores.",
    tech: ["Python", "Pygame"],
    author: "Agustín Godoy",
    initials: "AG",
    role: "Desarrollador · Arcade",
    accent: "linear-gradient(135deg,#00c8ff,#4fbb7c)",
    studentTech: ["Python", "Pygame", "Ranking", "Niveles de dificultad"],
  },
];

/** Games with a browser build under `public/jugar/<web>/` (see /jugar/[slug].astro). */
export const playableGames = games.filter((g) => g.web);
