import { useEffect, useState } from "react";
import { home, projects, routeGroups, routes } from "../../data/routes";
import { workshop } from "../../data/site";

interface Props {
  active?: string;
}

type Theme = "light" | "dark";

declare global {
  interface Window {
    __applyTheme?: (theme: Theme, animate?: boolean) => void;
    __currentTheme?: () => Theme;
  }
}

function ThemeIcon({ theme }: { theme: Theme }) {
  const common = {
    width: 16,
    height: 16,
    viewBox: "0 0 24 24",
    fill: "none",
    stroke: "currentColor",
    strokeWidth: 1.9,
    strokeLinecap: "round" as const,
    strokeLinejoin: "round" as const,
    "aria-hidden": true,
  };

  if (theme === "light") {
    return (
      <svg {...common}>
        <circle cx="12" cy="12" r="4" />
        <path d="M12 2v2M12 20v2M4.9 4.9l1.4 1.4M17.7 17.7l1.4 1.4M2 12h2M20 12h2M4.9 19.1l1.4-1.4M17.7 6.3l1.4-1.4" />
      </svg>
    );
  }

  return (
    <svg {...common}>
      <path d="M21 12.8A9 9 0 1 1 11.2 3a7 7 0 0 0 9.8 9.8z" />
    </svg>
  );
}

interface NavLink {
  href: string;
  label: string;
  blurb: string;
}

interface NavEntry {
  id: string;
  label: string;
  /** link directo (sin desplegable) */
  href?: string;
  /** contenido del desplegable */
  links?: NavLink[];
}

export default function Nav({ active = "/" }: Props) {
  const [open, setOpen] = useState(false);
  const [openGroup, setOpenGroup] = useState<string | null>(null);
  const [theme, setTheme] = useState<Theme>("dark");

  useEffect(() => {
    const sync = () => setTheme(window.__currentTheme?.() ?? "dark");
    sync();
    window.addEventListener("themechange", sync);
    return () => window.removeEventListener("themechange", sync);
  }, []);

  const toggleTheme = () => {
    const next: Theme = theme === "light" ? "dark" : "light";
    try {
      localStorage.setItem("theme", next);
    } catch {}
    window.__applyTheme?.(next, true);
  };

  // Astro entrega "/juegos/" y las rutas están sin barra final: normalizamos.
  const path = active.replace(/\/+$/, "") || "/";

  const groupLinks = (id: string): NavLink[] =>
    (routeGroups.find((g) => g.id === id)?.routes ?? []).map((r) => ({
      href: r.href,
      label: r.label,
      blurb: r.blurb,
    }));

  const entries: NavEntry[] = [
    { id: "escuela", label: home.label, href: home.href },
    {
      id: "proyecto",
      label: "Proyectos",
      links: projects.map((p) => ({ href: p.href, label: p.label, blurb: p.blurb })),
    },
    { id: "juegos", label: "Juegos", href: "/juegos" },
    {
      id: "aplicaciones",
      label: "Aplicaciones",
      href: routes.find((r) => r.group === "aplicaciones")?.href ?? "/aplicaciones",
    },
  ];

  const isActive = (entry: NavEntry) =>
    entry.href ? path === entry.href : (entry.links ?? []).some((l) => l.href === path);

  return (
    <nav className="sticky top-0 z-[500] border-b border-line1 bg-bg/85 backdrop-blur-2xl">
      <div className="mx-auto flex h-[60px] max-w-[1120px] items-center justify-between gap-4 px-5 md:px-10">
        <a href="/" aria-label="Nivel Superior El Nacional — Inicio" className="flex shrink-0 items-center">
          <img
            src="/logo_superior.png"
            alt="Nivel Superior El Nacional"
            width="1100"
            height="304"
            className="logo-on-light h-[32px] w-auto"
          />
          <img
            src="/logo_superior_dark.png"
            alt="Nivel Superior El Nacional"
            width="1100"
            height="304"
            className="logo-on-dark h-[32px] w-auto"
          />
        </a>

        {/* Desktop */}
        <div className="hidden items-center gap-0.5 min-[880px]:flex" onMouseLeave={() => setOpenGroup(null)}>
          {entries.map((entry) =>
            entry.href ? (
              <a
                key={entry.id}
                href={entry.href}
                className={[
                  "rounded-lg px-3 py-2 text-xs transition-colors",
                  isActive(entry) ? "bg-line1 text-t1" : "text-t2 hover:bg-line1 hover:text-t1",
                ].join(" ")}
              >
                {entry.label}
              </a>
            ) : (
              <div key={entry.id} className="relative" onMouseEnter={() => setOpenGroup(entry.id)}>
                <button
                  type="button"
                  onClick={() => setOpenGroup(openGroup === entry.id ? null : entry.id)}
                  className={[
                    "flex items-center gap-1 rounded-lg px-3 py-2 text-xs transition-colors",
                    isActive(entry) || openGroup === entry.id
                      ? "bg-line1 text-t1"
                      : "text-t2 hover:bg-line1 hover:text-t1",
                  ].join(" ")}
                >
                  <span>{entry.label}</span>
                  <svg
                    width="10"
                    height="10"
                    viewBox="0 0 24 24"
                    fill="none"
                    stroke="currentColor"
                    strokeWidth="2.4"
                    className={["transition-transform", openGroup === entry.id ? "rotate-180" : ""].join(" ")}
                  >
                    <path d="M6 9l6 6 6-6" />
                  </svg>
                </button>

                {openGroup === entry.id && (
                  <div className="absolute left-0 top-full z-[600] pt-2">
                    <div
                      className={[
                        "rounded-xl border border-line1 bg-bg2 p-2 ",
                        entry.id === "proyecto" ? "w-[330px]" : "w-64",
                      ].join(" ")}
                    >
                      {(entry.links ?? []).map((l) => (
                        <a
                          key={l.href}
                          href={l.href}
                          onClick={() => setOpenGroup(null)}
                          className={[
                            "block rounded-lg p-2.5 transition-colors",
                            path === l.href ? "bg-bg3" : "hover:bg-bg3",
                          ].join(" ")}
                        >
                          <span className="block text-[13px] font-medium text-t1">{l.label}</span>
                          <span className="block text-[11px] leading-snug text-t3">{l.blurb}</span>
                        </a>
                      ))}
                    </div>
                  </div>
                )}
              </div>
            )
          )}
        </div>

        <div className="flex shrink-0 items-center gap-2">
          <button
            type="button"
            onClick={toggleTheme}
            aria-label={`Cambiar a tema ${theme === "light" ? "oscuro" : "claro"}`}
            title={`Tema ${theme === "light" ? "claro" : "oscuro"}`}
            className="flex h-9 w-9 items-center justify-center rounded-lg border border-line1 text-t2 transition-colors hover:bg-bg3 hover:text-t1 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-a1"
          >
            <ThemeIcon theme={theme} />
          </button>
          <a
            href="/#inscripcion"
            className="hidden rounded-full bg-a1 px-4.5 py-2 text-[11px] font-semibold uppercase tracking-[0.06em] text-white transition  hover:opacity-85 min-[880px]:inline-block"
          >
            Contactate →
          </a>
          <a
            href={workshop.form}
            target="_blank"
            rel="noopener noreferrer"
            className="hidden items-center gap-1.5 whitespace-nowrap rounded-full bg-[linear-gradient(135deg,var(--color-a2),var(--color-a3))] px-4.5 py-2 text-[12px] font-semibold text-white shadow-[0_6px_20px_-6px_rgba(124,77,255,0.6)] transition hover:brightness-110 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-a3 min-[880px]:inline-flex"
          >
            <svg width="13" height="13" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true">
              <path d="M12 2.5l1.9 5.6 5.6 1.9-5.6 1.9L12 17.5l-1.9-5.6-5.6-1.9 5.6-1.9L12 2.5z" />
            </svg>
            Mi Primera App
            <span className="sr-only"> (se abre en una pestaña nueva)</span>
          </a>
          <button
            type="button"
            aria-label="Menú"
            className="flex p-2 text-t2 min-[880px]:hidden"
            onClick={() => setOpen((v) => !v)}
          >
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.8">
              {open ? <path d="M6 6l12 12M18 6L6 18" /> : <path d="M3 12h18M3 6h18M3 18h18" />}
            </svg>
          </button>
        </div>
      </div>

      {/* Mobile */}
      {open && (
        <div className="absolute inset-x-0 top-[60px] max-h-[calc(100vh-60px)] overflow-y-auto border-b border-line1 bg-bg2 px-5 py-4 min-[880px]:hidden">
          <a
            href={workshop.form}
            target="_blank"
            rel="noopener noreferrer"
            onClick={() => setOpen(false)}
            className="mb-4 flex items-center justify-center gap-2 rounded-xl bg-[linear-gradient(135deg,var(--color-a2),var(--color-a3))] px-4 py-3 text-[13px] font-semibold text-white shadow-[0_6px_20px_-6px_rgba(124,77,255,0.6)] transition hover:brightness-110 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-a3"
          >
            <svg width="14" height="14" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true">
              <path d="M12 2.5l1.9 5.6 5.6 1.9-5.6 1.9L12 17.5l-1.9-5.6-5.6-1.9 5.6-1.9L12 2.5z" />
            </svg>
            Mi Primera App
            <span className="sr-only"> (se abre en una pestaña nueva)</span>
          </a>

          {entries.map((entry) =>
            entry.href ? (
              <a
                key={entry.id}
                href={entry.href}
                onClick={() => setOpen(false)}
                className={[
                  "mb-2 block rounded-lg px-3 py-2 text-[13px] font-medium",
                  isActive(entry) ? "bg-bg3 text-t1" : "text-t1 hover:bg-bg3",
                ].join(" ")}
              >
                {entry.label}
              </a>
            ) : (
              <div key={entry.id} className="mb-3">
                <div className="mb-1 px-3 font-mono text-[10px] uppercase tracking-[0.16em] text-a1/75">
                  {entry.label}
                </div>
                <div className="grid grid-cols-1 gap-0.5 sm:grid-cols-2">
                  {(entry.links ?? []).map((l) => (
                    <a
                      key={l.href}
                      href={l.href}
                      onClick={() => setOpen(false)}
                      className={[
                        "block rounded-lg px-3 py-2 text-[13px]",
                        path === l.href ? "bg-bg3 text-t1" : "text-t2 hover:bg-bg3 hover:text-t1",
                      ].join(" ")}
                    >
                      {l.label}
                    </a>
                  ))}
                </div>
              </div>
            )
          )}
        </div>
      )}
    </nav>
  );
}
