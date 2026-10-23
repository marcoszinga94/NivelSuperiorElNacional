# AGENTS.md — `web/`

Astro 7 + Tailwind v4 + React 19 port of `/astronomos.html` (see the repo-root `AGENTS.md`).

## Commands

- `npm run dev` — dev server at http://localhost:4321. For background use the Astro CLI:
  `astro dev --background`, then `astro dev logs` / `astro dev status` / `astro dev stop`.
- `npm run build` — static output to `dist/`. This is the only verification step (no tests/linters).

## Layout — dos páginas largas + páginas cortas

La home es la página de la escuela (institución + las dos carreras + inscripción) y "Astrónomos por un día" junta todo su proyecto en una sola página. El resto de las secciones sigue en rutas cortas. `src/pages/*.astro` son finas: cada una importa `Base` y una o más secciones.

- `src/pages/index.astro` — home **de la escuela**: `Institution` (hace de hero: nombre, dos tecnicaturas y CTAs) + `Career` (Desarrollo de Software) + `Administration` (Administración) + `Enroll` + banda CTA. Las anclas son `#institucion`, `#carrera`, `#administracion`, `#inscripcion`; las viejas rutas `/institucion`, `/carrera` e `/inscripcion` redirigen a su ancla (ver `astro.config.mjs`). No hay `Hero.astro`: el video del proyecto vive en `/proyecto`.
- `src/pages/proyecto.astro` — "Astrónomos por un día" completo: `Project` + `Process` + `Chronology` + `Impact` + `Testimonials` + `Skills`, con anclas `#proceso`, `#cronologia`, `#impacto`, `#testimonios`, `#competencias`. Las viejas rutas de esas secciones redirigen acá.
- `src/pages/jugar/[slug].astro` — one page per playable game (`/jugar/arcspace`), generated from the games that have `web` set in `games.ts`. Embeds the game with `GamePlayer.astro`, which iframes `public/jugar/<slug>/juego/`.
- `public/jugar/player.js` — runs the recovered games in the browser (Pyodide + pygame-ce). Tres juegos usan en cambio un build propio de una sola página en HTML + JS (`html` en `games.ts`: `boom_cosmico.html`, `el_cielo_cordobes.html`, `viaje_galactico.html`), que se embebe con el mismo `GamePlayer` (`src`). See `tools/README.md` for how the games are recovered and rebuilt.
- `src/pages/juegos.astro` — una sola página para los juegos: `Games` (portada con contadores + grilla, cada tarjeta con el juego y su estudiante) y `Technologies` (`#tecnologias`, bloque 02). Las viejas rutas `/equipo` y `/tecnologias` redirigen acá.
- `src/pages/<slug>.astro` — one page per section (e.g. `aplicaciones.astro` renders `sections/Apps.astro`). Add a new section by creating the section component, the page, and an entry in `routes.ts`.
- `src/data/routes.ts` — **source of truth** for the route order, the nav `groups` (Proyecto, Juegos, Aplicaciones — la home es Escuela y no va en `routes`; Juegos y Aplicaciones son links directos, sólo Proyecto despliega), the dropdown `blurb`s, the `projects` list (the two entries of the "Proyecto" dropdown) and prev/next (`neighbours()`). Update `groups` + `routes` when adding/renaming a page — `routeGroups` is derived from them.
- `src/components/react/Nav.tsx` — navigation: school logo (`/logo_el_nacional.png`, on a white chip because the artwork is dark) + Escuela (link a `/`) + Proyecto (desplegable con los dos proyectos) + Juegos y Aplicaciones como links directos + the "Inscribite" CTA; mobile hamburger shows the same sections expanded. It highlights the active route via the `active` prop (`Astro.url.pathname`, con la barra final normalizada). No icons in the header.
- `src/pages/aplicaciones.astro` + `src/pages/administrativas.astro` — the second project: catalog of administrative apps (`src/data/apps.ts`, empty until the first one ships) and the project page. `Apps.astro` además incluye la sección `#proyecto-aplicaciones` con la propuesta de trabajo (empresas de tres integrantes, los tres proyectos asignados, etapas y documentación); esos textos viven en arrays del frontmatter del componente.
- `src/layouts/Base.astro` — head, Google Fonts, `<ClientRouter />` (navegación sin recarga), `<Particles>`/`<Nav>` islands, `<Footer>`, and the scroll-reveal `IntersectionObserver` script. Pasa `Astro.url.pathname` a `Nav` para el estado activo. Con el router, los `<script>` inline se vuelven a ejecutar en cada navegación: si agregás uno, que sea idempotente o escuchá `astro:page-load`.
- `src/components/sections/*.astro` — one section each; `Section.astro`, `SectionHeader.astro` are shared wrappers (`Divider.astro` is only for use *within* a page).
- `src/components/react/*.tsx` — client islands. Everything else is static.
- `src/data/games.ts` — single source of truth for the 8 games **and** the "Estudiantes" cards (author, initials, accent gradient, quote). Edit copy there, not in the section files. `web` is the slug of the browser build under `public/jugar/<web>/` (`null` = not playable online yet); `exe` is the Windows file in `public/Ejecutadores/`; `logo` is the icon pulled out of that `.exe` (`public/juegos/icono/<slug>.png`, see `tools/README.md`), `null` = the executable has no usable icon and the card falls back to the emoji.
- `src/data/site.ts` — event name/description, hero stats, impact metrics.

Las rutas cortas usan rutas reales (`/juegos`, `/equipo`, ...). La escuela y "Astrónomos por un día" son páginas largas con anclas (`/#carrera`, `/proyecto#impacto`): al linkear dentro de ellas usá el ancla, y mantené la redirección en `astro.config.mjs` si movés una sección.

## Conventions

- Languages: Spanish (es-AR) only.
- Design tokens (`--color-a1`, `--color-bg`, fonts) are defined in `src/styles/global.css` under `@theme`; style markup with Tailwind utilities. The `.reveal` animation classes and `.text-gradient` live there too.
- `@theme` color names map to utilities: `--color-a1` → `bg-a1/text-a1`, `--color-bg2` → `bg-bg2`, `--color-line1` → `border-line1`, `--color-t2` → `text-t2`.
- There are no game demo videos for the rest of the games; don't reintroduce the demo modal or `data-demo` buttons. Two games have a gameplay video (`video` in `games.ts`, `public/jugar/<slug>/`): their page shows the video instead of the embedded game and their card button says "Ver juego".
- `public/juegos/icono/` guarda los logos extraídos de los `.exe` (ver `tools/README.md`); dos juegos usan otro archivo porque su ejecutable no trae ícono propio (`arcspace-logo.png`, `solar-defender-logo.png`). Si falta un logo, la tarjeta cae al emoji sobre el degradado; no lo tapes con una captura inventada.
