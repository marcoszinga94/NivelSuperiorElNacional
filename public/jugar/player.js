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

  let revealTouchToggle = null;

  window.jsGameStarted = () => {
    document.getElementById("player-overlay")?.classList.add("is-hidden");
    setTimeout(() => document.getElementById("player-overlay")?.remove(), 600);
    revealTouchToggle?.();
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

  /**
   * Sample rate the device actually runs at. Phones usually use 48000 Hz; opening
   * the mixer at a different rate makes SDL resample and can sound dirty.
   */
  const audioRate = () => {
    try {
      const Ctx = window.AudioContext || window.webkitAudioContext;
      const probe = new Ctx();
      const rate = probe.sampleRate;
      void probe.close();
      return rate;
    } catch {
      return 44100;
    }
  };

  /* --- controles táctiles ------------------------------------------------
   * Los juegos son de teclado. En el celular agregamos un gamepad que manda
   * los mismos eventos que SDL escucha en el window del iframe. Se muestra
   * recién cuando arranca el juego, para no tapar la pantalla de inicio.
   */
  const KEY_EVENTS = {
    ArrowUp: { key: "ArrowUp", code: "ArrowUp", keyCode: 38 },
    ArrowDown: { key: "ArrowDown", code: "ArrowDown", keyCode: 40 },
    ArrowLeft: { key: "ArrowLeft", code: "ArrowLeft", keyCode: 37 },
    ArrowRight: { key: "ArrowRight", code: "ArrowRight", keyCode: 39 },
    Space: { key: " ", code: "Space", keyCode: 32 },
    Enter: { key: "Enter", code: "Enter", keyCode: 13 },
    Escape: { key: "Escape", code: "Escape", keyCode: 27 },
    Backspace: { key: "Backspace", code: "Backspace", keyCode: 8 },
  };

  function sendKey(type, name) {
    const spec = KEY_EVENTS[name];
    if (!spec) return;
    const canvas = document.getElementById("canvas");
    const targets = [window, document, canvas].filter(Boolean);
    for (const target of targets) {
      const event = new KeyboardEvent(type, {
        key: spec.key,
        code: spec.code,
        bubbles: true,
        cancelable: true,
      });
      // SDL/emscripten todavía consulta las propiedades viejas.
      Object.defineProperty(event, "keyCode", { get: () => spec.keyCode });
      Object.defineProperty(event, "which", { get: () => spec.keyCode });
      target.dispatchEvent(event);
    }
  }

  /** Manda una letra al juego como si se hubiera escrito en el teclado. */
  function sendChar(char) {
    if (char === " ") {
      sendKey("keydown", "Space");
      sendKey("keyup", "Space");
      return;
    }
    const code = /[a-z]/i.test(char)
      ? "Key" + char.toUpperCase()
      : /[0-9]/.test(char)
        ? "Digit" + char
        : "";
    const keyCode = char.toUpperCase().charCodeAt(0);
    const canvas = document.getElementById("canvas");
    const targets = [window, document, canvas].filter(Boolean);
    for (const type of ["keydown", "keyup"]) {
      for (const target of targets) {
        const event = new KeyboardEvent(type, {
          key: char,
          code,
          bubbles: true,
          cancelable: true,
        });
        Object.defineProperty(event, "keyCode", { get: () => keyCode });
        Object.defineProperty(event, "which", { get: () => keyCode });
        target.dispatchEvent(event);
      }
    }
  }

  function installTouchControls() {
    const coarse =
      window.matchMedia?.("(pointer: coarse)").matches || navigator.maxTouchPoints > 0;
    if (!coarse || document.getElementById("pg-touch-toggle")) return;

    const style = document.createElement("style");
    style.textContent = `
      #pg-touch-toggle,
      #pg-touch-keyboard {
        position: fixed;
        top: max(12px, env(safe-area-inset-top));
        left: max(12px, env(safe-area-inset-left));
        z-index: 40;
        display: grid;
        place-items: center;
        width: 44px;
        height: 44px;
        border: 1px solid rgba(255, 255, 255, 0.22);
        border-radius: 999px;
        background: rgba(8, 12, 24, 0.72);
        color: #eef2ff;
        font: 20px/1 system-ui, sans-serif;
        box-shadow: 0 6px 20px rgba(0, 0, 0, 0.4);
        backdrop-filter: blur(8px);
        touch-action: manipulation;
      }
      #pg-touch-keyboard {
        left: calc(max(12px, env(safe-area-inset-left)) + 52px);
        font-size: 18px;
      }
      #pg-touch-toggle[hidden],
      #pg-touch-keyboard[hidden],
      #pg-touch-pad[hidden] { display: none; }
      #pg-touch-input {
        position: fixed;
        left: 50%;
        bottom: 0;
        z-index: 45;
        width: 1px;
        height: 1px;
        margin: 0;
        padding: 0;
        border: 0;
        opacity: 0;
        transform: translateX(-50%);
      }
      #pg-touch-pad {
        position: fixed;
        inset: 0;
        z-index: 35;
        pointer-events: none;
      }
      .pg-touch-dpad {
        position: absolute;
        left: max(14px, env(safe-area-inset-left));
        bottom: max(14px, env(safe-area-inset-bottom));
        display: grid;
        grid-template-columns: repeat(3, 46px);
        grid-template-rows: repeat(3, 46px);
        gap: 6px;
      }
      .pg-touch-actions {
        position: absolute;
        right: max(14px, env(safe-area-inset-right));
        bottom: max(14px, env(safe-area-inset-bottom));
        display: flex;
        align-items: flex-end;
        gap: 10px;
      }
      .pg-touch-btn {
        pointer-events: auto;
        display: grid;
        place-items: center;
        width: 46px;
        height: 46px;
        border: 1px solid rgba(255, 255, 255, 0.2);
        border-radius: 13px;
        background: rgba(10, 16, 32, 0.7);
        color: #fff;
        font: 600 17px/1 system-ui, sans-serif;
        box-shadow: 0 4px 14px rgba(0, 0, 0, 0.35);
        backdrop-filter: blur(6px);
        touch-action: none;
        user-select: none;
        -webkit-user-select: none;
        transition: background 120ms ease, transform 120ms ease;
      }
      .pg-touch-btn.is-down {
        background: rgba(79, 127, 255, 0.8);
        transform: scale(0.95);
      }
      .pg-touch-a {
        width: 58px;
        height: 58px;
        border-radius: 50%;
        font-size: 20px;
      }
      .pg-touch-b {
        width: 52px;
        height: 52px;
        border-radius: 50%;
      }
      .pg-touch-menu {
        width: 42px;
        height: 42px;
        font-size: 15px;
      }
      @media (max-height: 380px) {
        .pg-touch-dpad {
          grid-template-columns: repeat(3, 40px);
          grid-template-rows: repeat(3, 40px);
          gap: 5px;
        }
        .pg-touch-a { width: 52px; height: 52px; }
        .pg-touch-b { width: 46px; height: 46px; }
      }
    `;
    document.head.appendChild(style);

    const toggle = document.createElement("button");
    toggle.id = "pg-touch-toggle";
    toggle.type = "button";
    toggle.hidden = true;
    toggle.textContent = "🎮";
    toggle.setAttribute("aria-label", "Mostrar controles táctiles");
    toggle.setAttribute("aria-pressed", "false");
    document.body.appendChild(toggle);

    const keyboard = document.createElement("button");
    keyboard.id = "pg-touch-keyboard";
    keyboard.type = "button";
    keyboard.hidden = true;
    keyboard.textContent = "⌨";
    keyboard.setAttribute("aria-label", "Abrir el teclado del teléfono");
    document.body.appendChild(keyboard);

    const keyboardInput = document.createElement("input");
    keyboardInput.id = "pg-touch-input";
    keyboardInput.type = "text";
    keyboardInput.autocomplete = "off";
    keyboardInput.autocapitalize = "words";
    keyboardInput.spellcheck = false;
    keyboardInput.setAttribute("aria-label", "Teclado para el juego");
    document.body.appendChild(keyboardInput);

    const pad = document.createElement("div");
    pad.id = "pg-touch-pad";
    pad.hidden = true;
    pad.innerHTML = `
      <div class="pg-touch-dpad">
        <button type="button" class="pg-touch-btn" data-key="ArrowUp" style="grid-area:1/2" aria-label="Arriba">▲</button>
        <button type="button" class="pg-touch-btn" data-key="ArrowLeft" style="grid-area:2/1" aria-label="Izquierda">◀</button>
        <button type="button" class="pg-touch-btn" data-key="ArrowDown" style="grid-area:2/2" aria-label="Abajo">▼</button>
        <button type="button" class="pg-touch-btn" data-key="ArrowRight" style="grid-area:2/3" aria-label="Derecha">▶</button>
      </div>
      <div class="pg-touch-actions">
        <button type="button" class="pg-touch-btn pg-touch-menu" data-key="Escape" aria-label="Menú o volver">≡</button>
        <button type="button" class="pg-touch-btn pg-touch-b" data-key="Enter" aria-label="Confirmar">B</button>
        <button type="button" class="pg-touch-btn pg-touch-a" data-key="Space" aria-label="Acción">A</button>
      </div>
    `;
    document.body.appendChild(pad);

    const setOpen = (open) => {
      pad.hidden = !open;
      toggle.textContent = open ? "✕" : "🎮";
      toggle.setAttribute("aria-pressed", String(open));
      toggle.setAttribute(
        "aria-label",
        open ? "Ocultar controles táctiles" : "Mostrar controles táctiles"
      );
      if (open) document.getElementById("canvas")?.focus?.();
    };

    toggle.addEventListener("click", () => setOpen(pad.hidden));

    keyboard.addEventListener("click", () => {
      if (document.activeElement === keyboardInput) {
        keyboardInput.blur();
        return;
      }
      keyboardInput.value = "";
      keyboardInput.focus();
    });

    keyboardInput.addEventListener("input", () => {
      const text = keyboardInput.value;
      keyboardInput.value = "";
      for (const char of text) sendChar(char);
    });

    keyboardInput.addEventListener("keydown", (event) => {
      event.stopPropagation();
      if (event.key === "Backspace" || event.key === "Enter" || event.key === "Escape") {
        event.preventDefault();
        sendKey("keydown", event.key);
        sendKey("keyup", event.key);
        return;
      }
      // Teclado físico: mandamos la letra directo. En los teclados virtuales
      // que no reportan la tecla, el evento "input" de abajo hace el trabajo.
      if (event.key.length === 1 && !event.ctrlKey && !event.metaKey && !event.altKey) {
        event.preventDefault();
        sendChar(event.key);
      }
    });
    keyboardInput.addEventListener("keyup", (event) => event.stopPropagation());

    pad.querySelectorAll(".pg-touch-btn").forEach((button) => {
      const name = button.dataset.key;
      if (!name) return;

      const down = (event) => {
        event.preventDefault();
        button.classList.add("is-down");
        try {
          button.setPointerCapture(event.pointerId);
        } catch {
          /* Pointer capture no disponible. */
        }
        sendKey("keydown", name);
      };
      const up = (event) => {
        event.preventDefault();
        button.classList.remove("is-down");
        sendKey("keyup", name);
      };

      button.addEventListener("pointerdown", down);
      button.addEventListener("pointerup", up);
      button.addEventListener("pointercancel", up);
      button.addEventListener("lostpointercapture", () => {
        if (button.classList.contains("is-down")) up(new Event("lostpointercapture"));
      });
      button.addEventListener("contextmenu", (event) => event.preventDefault());
    });

    revealTouchToggle = () => {
      toggle.hidden = false;
      keyboard.hidden = false;
    };
  }

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


# --- audio ------------------------------------------------------------------
# En el celular los callbacks de audio comparten el hilo con el juego, asi que
# un frame lento se escucha como estatica. Abrimos el mixer a la frecuencia del
# dispositivo (si no, SDL remuestrea) con un buffer holgado.
AUDIO_RATE = int(js_audio_rate) or 44100
_pre_init = pygame.mixer.pre_init
_init = pygame.mixer.init


def _mixer_args():
    return (AUDIO_RATE, -16, 2, 4096)


pygame.mixer.pre_init = lambda *args, **kwargs: _pre_init(*_mixer_args())
pygame.mixer.init = lambda *args, **kwargs: _init(*_mixer_args())

_breathe_at = [0.0]


def _breathe():
    now = time.monotonic()
    if now - _breathe_at[0] >= 0.016:
        _breathe_at[0] = now
        run_sync(js_breathe())


def _wrap_breathe(owner, name):
    original = getattr(owner, name, None)
    if original is None:
        return

    def wrapper(*args, **kwargs):
        result = original(*args, **kwargs)
        _breathe()
        return result

    setattr(owner, name, wrapper)


# Un frame con cientos de primitivas deja sordo al audio; esto lo corta en trozos.
for _name in ("circle", "rect", "line", "lines", "polygon", "ellipse", "arc", "aaline", "aalines"):
    _wrap_breathe(pygame.draw, _name)


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
      // Mid-frame pause: lets the Web Audio callbacks run without waiting for a
      // paint, so long frames on a phone don't turn the sound into static.
      pyodide.globals.set("js_breathe", () => new Promise((resolve) => setTimeout(resolve, 0)));
      pyodide.globals.set("js_audio_rate", audioRate());
      window.__playerPyodide = pyodide;
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
    installTouchControls();
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
