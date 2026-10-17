/**
 * Browser player for the recovered pygame games.
 *
 * The games ship as the original Python bytecode (`*.pyc`) taken from the
 * student `.exe` builds, plus their assets. We run them with Pyodide
 * (CPython compiled to WebAssembly) and the pygame-ce wheel for the matching
 * Python version, so nothing has to be installed and no source is required.
 *
 * The one thing a browser cannot do is let a synchronous game loop run
 * forever: it would freeze the tab. So `pygame.display.update` / `flip` and
 * the clock are wrapped to hand control back to the browser once per frame
 * (`run_sync` + asyncify), which keeps rendering and input alive.
 *
 * Each game folder only needs an `index.html` with:
 *   window.GAME_CONFIG = { title, pyodide, entry, archive }
 */
(() => {
  const cfg = window.GAME_CONFIG || {};
  const status = (msg) => {
    const el = document.getElementById("player-status");
    if (el) el.textContent = msg;
  };
  const fail = (err) => {
    const detail = String((err && err.stack) || (err && err.message) || err);
    window.__lastError = detail;
    const el = document.getElementById("player-status");
    if (el) {
      el.textContent = "No se pudo iniciar el juego. " + detail;
      el.classList.add("is-error");
    } else {
      const box = document.createElement("pre");
      box.style.cssText =
        "position:fixed;inset:0;z-index:99;margin:0;padding:24px;overflow:auto;" +
        "background:#12060a;color:#ff9d9d;font:12px/1.5 monospace;white-space:pre-wrap";
      box.textContent = "No se pudo iniciar el juego.\n\n" + detail;
      document.body.appendChild(box);
    }
    console.error("[player]", detail);
  };

  window.jsGameStarted = () => {
    document.getElementById("player-overlay")?.classList.add("is-hidden");
    setTimeout(() => document.getElementById("player-overlay")?.remove(), 600);
  };

  /** Scale the framebuffer canvas to the viewport, keeping the aspect ratio. */
  const fitCanvas = () => {
    const c = document.getElementById("canvas");
    if (!c || !c.width || !c.height) return;
    const pad = 8;
    const s = Math.min(
      (window.innerWidth - pad) / c.width,
      (window.innerHeight - pad) / c.height
    );
    c.style.width = `${Math.floor(c.width * s)}px`;
    c.style.height = `${Math.floor(c.height * s)}px`;
  };
  window.addEventListener("resize", fitCanvas);

  const PYTHON = String.raw`
import asyncio, builtins, marshal, os, sys, time, zipfile
from pyodide.ffi import run_sync
import pygame


# --- cooperative frame yield ------------------------------------------------
def _yield():
    run_sync(js_sleep())


def _sleep(seconds):
    if seconds and seconds > 0:
        run_sync(js_sleep(float(seconds) * 1000.0))


def _wrap_yield(owner, name):
    original = getattr(owner, name)

    def wrapper(*args, **kwargs):
        result = original(*args, **kwargs)
        _yield()
        return result

    setattr(owner, name, wrapper)


_wrap_yield(pygame.display, "update")
_wrap_yield(pygame.display, "flip")

# time.sleep would busy-wait and freeze the tab.
time.sleep = _sleep
pygame.time.wait = lambda ms=0: _sleep((ms or 0) / 1000.0)
pygame.time.delay = pygame.time.wait

if hasattr(pygame.event, "wait"):
    def _event_wait(timeout=0):
        events = pygame.event.get()
        if events:
            return events[0]
        _sleep(0.001)
        return pygame.event.Event(pygame.NOEVENT)
    pygame.event.wait = _event_wait


# --- display ----------------------------------------------------------------
_CANNOT_FULLSCREEN = (
    getattr(pygame, "FULLSCREEN", 0)
    | getattr(pygame, "SCALED", 0)
    | getattr(pygame, "RESIZABLE", 0)
    | getattr(pygame, "NOFRAME", 0)
)
_set_mode = pygame.display.set_mode


def set_mode(size=(0, 0), flags=0, *args, **kwargs):
    result = _set_mode(size, flags & ~_CANNOT_FULLSCREEN, *args, **kwargs)
    return result


pygame.display.set_mode = set_mode

# Several games size their "virtual" surface from the reported screen size and
# then letterbox it. SDL in the browser reports a tiny default, which breaks
# that maths, so games can pin the resolution they were designed for.
if GAME_SCREEN:

    class _ScreenInfo:
        def __init__(self, width, height):
            self.current_w = width
            self.current_h = height
            self.hw = False
            self.wm = False
            self.video_mem = 0
            self.bitsize = 32
            self.bytesize = 4
            self.video_driver = "emscripten"

    def screen_info():
        return _ScreenInfo(*GAME_SCREEN)

    pygame.display.Info = screen_info


# pygame's Clock.tick waits with SDL_Delay, which cannot yield in the browser,
# and the C type cannot be patched in place, so we swap in a Python clock.
class _Clock:
    def __init__(self):
        self._start = time.monotonic()
        self._elapsed = 0.0
        self._fps = 0.0

    def tick(self, framerate=0):
        now = time.monotonic()
        elapsed = now - self._start
        if framerate:
            target = 1.0 / framerate
            if target > elapsed:
                _sleep(target - elapsed)
                now = time.monotonic()
                elapsed = now - self._start
        self._start = now
        self._elapsed = elapsed
        self._fps = (1.0 / elapsed) if elapsed > 0 else 0.0
        return int(elapsed * 1000)

    def tick_busy_loop(self, framerate=0):
        return self.tick(framerate)

    def get_time(self):
        return int(self._elapsed * 1000)

    def get_rawtime(self):
        return int(self._elapsed * 1000)

    def get_fps(self):
        return self._fps


pygame.time.Clock = _Clock


# --- boot the game ----------------------------------------------------------
async def _boot():
    os.chdir("/game")
    pygame.display.set_caption(GAME_TITLE)
    entry = os.path.join("/game", GAME_ENTRY)
    if GAME_ENTRY.endswith(".py"):
        # Recovered source (for games whose bytecode cannot run: Python 3.10/3.11).
        with open(entry, "r", encoding="utf-8") as handle:
            code = compile(handle.read(), entry, "exec")
    else:
        with open(entry, "rb") as handle:
            code = marshal.loads(handle.read()[16:])
    globals_ = {"__name__": "__main__", "__file__": entry, "__builtins__": builtins}
    sys.argv = [entry]
    sys.path.insert(0, "/game")
    js_game_started()
    exec(code, globals_)
`;

  async function boot() {
    try {
      status("Descargando el motor de Python…");
      const { loadPyodide } = await import(
        `https://cdn.jsdelivr.net/pyodide/v${cfg.pyodide}/full/pyodide.mjs`
      );
      const pyodide = await loadPyodide({
        indexURL: `https://cdn.jsdelivr.net/pyodide/v${cfg.pyodide}/full/`,
      });

      status("Preparando la pantalla…");
      const canvas = document.getElementById("canvas");
      pyodide.canvas.setCanvas2D(canvas);
      pyodide.globals.set("js_sleep", (ms = 0) =>
        new Promise((resolve) =>
          ms > 0 ? setTimeout(resolve, ms) : requestAnimationFrame(() => resolve())
        )
      );
      pyodide.globals.set("js_game_started", () => window.jsGameStarted());

      status("Cargando pygame…");
      await pyodide.loadPackage("pygame-ce");

      status("Desempacando el juego…");
      await pyodide.runPythonAsync(`
import os, zipfile
os.makedirs("/game", exist_ok=True)
`);
      const response = await fetch(cfg.archive);
      const bytes = new Uint8Array(await response.arrayBuffer());
      pyodide.FS.writeFile("/tmp/game.zip", bytes);
      await pyodide.runPythonAsync(`
with zipfile.ZipFile("/tmp/game.zip") as archive:
    archive.extractall("/game")
`);

      pyodide.globals.set("GAME_TITLE", cfg.title || "Juego");
      pyodide.globals.set("GAME_ENTRY", cfg.entry || "main.pyc");
      pyodide.globals.set("GAME_SCREEN", cfg.screen || null);
      if (cfg.screen) {
        const [w, h] = cfg.screen;
        const c = document.getElementById("canvas");
        if (c) {
          c.width = w;
          c.height = h;
        }
      }
      await pyodide.runPythonAsync(PYTHON);

      // The call below never resolves: the game keeps the interpreter busy.
      pyodide.runPythonAsync(`
await _boot()
`).catch(fail);

      // Re-fit whenever the game changes the framebuffer size.
      new MutationObserver(fitCanvas).observe(canvas, {
        attributes: true,
        attributeFilter: ["width", "height"],
      });
      fitCanvas();
    } catch (err) {
      fail(err);
    }
  }

  document.addEventListener("DOMContentLoaded", () => {
    document.getElementById("player-start")?.addEventListener(
      "click",
      (event) => {
        event.currentTarget.setAttribute("hidden", "hidden");
        void boot();
      },
      { once: true }
    );
  });
})();
