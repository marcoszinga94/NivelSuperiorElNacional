import { useCallback, useEffect, useRef, useState } from "react";

interface Demo {
  src: string;
  title: string;
  dev: string;
}

export default function VideoModal() {
  const [demo, setDemo] = useState<Demo | null>(null);
  const [open, setOpen] = useState(false);
  const videoRef = useRef<HTMLVideoElement>(null);

  const close = useCallback(() => {
    setOpen(false);
    const video = videoRef.current;
    if (video) {
      video.pause();
      video.removeAttribute("src");
      video.load();
    }
    document.body.style.overflow = "";
  }, []);

  const openDemo = useCallback((d: Demo) => {
    if (!d.src) {
      window.alert("Demo de video próximamente disponible.");
      return;
    }
    setDemo(d);
    setOpen(true);
    document.body.style.overflow = "hidden";
  }, []);

  useEffect(() => {
    const onClick = (e: MouseEvent) => {
      const el = (e.target as HTMLElement)?.closest<HTMLElement>("[data-demo]");
      if (!el) return;
      openDemo({
        src: el.dataset.demo ?? "",
        title: el.dataset.title ?? "Demo",
        dev: el.dataset.dev ?? "",
      });
    };
    document.addEventListener("click", onClick);
    return () => document.removeEventListener("click", onClick);
  }, [openDemo]);

  useEffect(() => {
    const onKey = (e: KeyboardEvent) => {
      if (e.key === "Escape") close();
    };
    document.addEventListener("keydown", onKey);
    return () => document.removeEventListener("keydown", onKey);
  }, [close]);

  return (
    <div
      role="dialog"
      aria-modal="true"
      aria-hidden={!open}
      className={[
        "fixed inset-0 z-[1000] flex items-center justify-center p-5 transition-opacity duration-300",
        open ? "pointer-events-auto opacity-100" : "pointer-events-none opacity-0",
      ].join(" ")}
    >
      <div className="absolute inset-0 cursor-pointer bg-bg/92 backdrop-blur-2xl" onClick={close} />
      <div
        className={[
          "relative w-full max-w-[880px] overflow-hidden rounded-[20px] border border-ba bg-bg2 shadow-[0_40px_120px_rgba(0,0,0,.8),0_0_60px_rgba(79,127,255,.1)] transition-transform duration-[350ms]",
          open ? "scale-100 translate-y-0" : "scale-[.94] translate-y-4",
        ].join(" ")}
      >
        <div className="flex items-center justify-between border-b border-line1 px-6 py-4.5">
          <div>
            <div className="text-base font-semibold text-t1">{demo?.title ?? "Demo"}</div>
            <div className="text-xs text-t3">por {demo?.dev ?? ""}</div>
          </div>
          <button
            type="button"
            aria-label="Cerrar"
            onClick={close}
            className="flex h-8 w-8 items-center justify-center rounded-lg border border-line1 text-base text-t2 transition hover:bg-bg3 hover:text-t1"
          >
            ✕
          </button>
        </div>
        <video
          ref={videoRef}
          className="block max-h-[70vh] w-full bg-black"
          controls
          preload="auto"
          src={open ? demo?.src : undefined}
        />
      </div>
    </div>
  );
}
