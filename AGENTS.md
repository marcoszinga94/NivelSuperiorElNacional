# AGENTS.md — `web/`

Astro 7 + Tailwind v4 + React 19 port of `/astronomos.html` (see the repo-root `AGENTS.md`).

## Commands

- `npm run dev` — dev server at http://localhost:4321. For background use the Astro CLI:
  `astro dev --background`, then `astro dev logs` / `astro dev status` / `astro dev stop`.
- `npm run build` — static output to `dist/`. This is the only verification step (no tests/linters).

## Layout — multi-page (one route per section)

The site used to be one long scroll page; it is now split into routes so each section is short. `src/pages/*.astro` are thin: each imports `Base`, one section component, and `PageNav`.

- `src/pages/index.astro` — home: `Hero` + `ExploreGrid` (cards linking to every route) + a closing CTA band.
- `src/pages/jugar/[slug].astro` — one page per playable game (`/jugar/arcspace`), generated from the games that have `web` set in `games.ts`. Embeds the game with `GamePlayer.astro`, which iframes `public/jugar/<slug>/juego/`.
- `public/jugar/player.js` — runs the recovered games in the browser (Pyodide + pygame-ce). See `tools/README.md` for how the games are recovered and rebuilt.
- `src/pages/<slug>.astro` — one page per section (e.g. `juegos.astro` renders `sections/Games.astro`). Add a new section by creating the section component, the page, and an entry in `routes.ts`.
- `src/data/routes.ts` — **source of truth** for the route order, the `groups` (section headings used by the nav dropdowns, home grid and footer), the dropdown `blurb`s, and prev/next (`neighbours()`). Update `groups` + `routes` when adding/renaming a page — `routeGroups` is derived from them.
- `src/components/react/Nav.tsx` — grouped navigation: desktop dropdown per group + "Inicio" + the "Inscribite" CTA; mobile hamburger shows the same groups expanded. It highlights the active route via the `active` prop (`Astro.url.pathname`).
- `src/layouts/Base.astro` — head, Google Fonts, `<Particles>`/`<Nav>` islands, `<Footer>`, and the scroll-reveal `IntersectionObserver` script. Passes `Astro.url.pathname` to `Nav` for the active state.
- `src/components/ExploreGrid.astro` / `PageNav.astro` — home grid and prev/next footer nav (both driven by `routes.ts`).
- `src/components/sections/*.astro` — one section each; `Section.astro`, `SectionHeader.astro` are shared wrappers (`Divider.astro` is only for use *within* a page).
- `src/components/react/*.tsx` — client islands. Everything else is static.
- `src/data/games.ts` — single source of truth for the 8 games **and** the "Estudiantes" cards (author, initials, accent gradient, quote). Edit copy there, not in the section files. `web` is the slug of the browser build under `public/jugar/<web>/` (`null` = not playable online yet); `exe` is the Windows file in `public/Ejecutadores/`; `logo` is the icon pulled out of that `.exe` (`public/juegos/icono/<slug>.png`, see `tools/README.md`), `null` = the executable has no usable icon and the card falls back to the emoji.
- `src/data/site.ts` — event name/description, hero stats, impact metrics.

All internal navigation uses real route paths (`/juegos`, `/equipo`, ...), not `#anchors`. Don't reintroduce in-page anchor links.

## Conventions

- Languages: Spanish (es-AR) only.
- Design tokens (`--color-a1`, `--color-bg`, fonts) are defined in `src/styles/global.css` under `@theme`; style markup with Tailwind utilities. The `.reveal` animation classes and `.text-gradient` live there too.
- `@theme` color names map to utilities: `--color-a1` → `bg-a1/text-a1`, `--color-bg2` → `bg-bg2`, `--color-line1` → `border-line1`, `--color-t2` → `text-t2`.
- There are no game demo videos; don't reintroduce the demo modal or `data-demo` buttons.
- `public/juegos/icono/` guarda los logos extraídos de los `.exe` (ver `tools/README.md`); dos juegos usan otro archivo porque su ejecutable no trae ícono propio (`arcspace-logo.png`, `solar-defender-logo.png`). Si falta un logo, la tarjeta cae al emoji sobre el degradado; no lo tapes con una captura inventada.
