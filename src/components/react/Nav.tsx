import { useState } from "react";
import { routeGroups, routes } from "../../data/routes";

interface Props {
  active?: string;
}

export default function Nav({ active = "/" }: Props) {
  const [open, setOpen] = useState(false);
  const [openGroup, setOpenGroup] = useState<string | null>(null);

  const groupIsActive = (id: string) => routes.some((r) => r.group === id && r.href === active);

  return (
    <nav className="sticky top-0 z-[500] border-b border-line1 bg-bg/85 backdrop-blur-2xl">
      <div className="mx-auto flex h-[60px] max-w-[1120px] items-center justify-between gap-4 px-5 md:px-10">
        <a href="/" className="flex shrink-0 items-center gap-2.5">
          <span className="h-2 w-2 animate-pulse rounded-full bg-a1 shadow-[0_0_10px_var(--color-a1)]" />
          <span className="whitespace-nowrap text-[13px] font-semibold">Astrónomos por un día</span>
        </a>

        {/* Desktop */}
        <div className="hidden items-center gap-0.5 min-[880px]:flex" onMouseLeave={() => setOpenGroup(null)}>
          <a
            href="/"
            className={[
              "rounded-lg px-3 py-2 text-xs transition-colors",
              active === "/" ? "bg-line1 text-t1" : "text-t2 hover:bg-line1 hover:text-t1",
            ].join(" ")}
          >
            Inicio
          </a>

          {routeGroups.map((g) => (
            <div key={g.id} className="relative" onMouseEnter={() => setOpenGroup(g.id)}>
              <button
                type="button"
                onClick={() => setOpenGroup(openGroup === g.id ? null : g.id)}
                className={[
                  "flex items-center gap-1 rounded-lg px-3 py-2 text-xs transition-colors",
                  groupIsActive(g.id) || openGroup === g.id
                    ? "bg-line1 text-t1"
                    : "text-t2 hover:bg-line1 hover:text-t1",
                ].join(" ")}
              >
                <span>{g.icon}</span>
                {g.label}
                <svg
                  width="10"
                  height="10"
                  viewBox="0 0 24 24"
                  fill="none"
                  stroke="currentColor"
                  strokeWidth="2.4"
                  className={["transition-transform", openGroup === g.id ? "rotate-180" : ""].join(" ")}
                >
                  <path d="M6 9l6 6 6-6" />
                </svg>
              </button>

              {openGroup === g.id && (
                <div className="absolute left-0 top-full z-[600] pt-2">
                  <div className="w-64 rounded-xl border border-line1 bg-bg2 p-2 shadow-[0_20px_60px_rgba(0,0,0,.6)]">
                    {g.routes.map((r) => (
                      <a
                        key={r.href}
                        href={r.href}
                        onClick={() => setOpenGroup(null)}
                        className={[
                          "flex items-start gap-3 rounded-lg p-2.5 transition-colors",
                          active === r.href ? "bg-bg3" : "hover:bg-bg3",
                        ].join(" ")}
                      >
                        <span className="mt-0.5 text-base">{r.icon}</span>
                        <span>
                          <span className="block text-[13px] font-medium text-t1">{r.label}</span>
                          <span className="block text-[11px] leading-snug text-t3">{r.blurb}</span>
                        </span>
                      </a>
                    ))}
                  </div>
                </div>
              )}
            </div>
          ))}
        </div>

        <div className="flex shrink-0 items-center gap-2">
          <a
            href="/inscripcion"
            className="hidden rounded-full bg-a1 px-4.5 py-2 text-[11px] font-semibold uppercase tracking-[0.06em] text-white transition hover:-translate-y-px hover:opacity-85 min-[880px]:inline-block"
          >
            Inscribite →
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
            href="/"
            onClick={() => setOpen(false)}
            className="mb-2 block rounded-lg px-3 py-2 text-[13px] font-medium text-t1 hover:bg-bg3"
          >
            🏠 Inicio
          </a>
          {routeGroups.map((g) => (
            <div key={g.id} className="mb-3">
              <div className="mb-1 flex items-center gap-2 px-3 font-mono text-[10px] uppercase tracking-[0.16em] text-a1/75">
                <span>{g.icon}</span>
                {g.label}
              </div>
              <div className="grid grid-cols-1 gap-0.5 sm:grid-cols-2">
                {g.routes.map((r) => (
                  <a
                    key={r.href}
                    href={r.href}
                    onClick={() => setOpen(false)}
                    className={[
                      "flex items-center gap-3 rounded-lg px-3 py-2 text-[13px]",
                      active === r.href ? "bg-bg3 text-t1" : "text-t2 hover:bg-bg3 hover:text-t1",
                    ].join(" ")}
                  >
                    <span>{r.icon}</span>
                    {r.label}
                  </a>
                ))}
              </div>
            </div>
          ))}
        </div>
      )}
    </nav>
  );
}
