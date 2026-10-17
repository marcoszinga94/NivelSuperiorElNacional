#!/usr/bin/env python3
"""
Builds the browser versions of the recovered student games.

Each game is shipped as a zip holding its original Python bytecode plus its
assets; the runner (`public/jugar/player.js`) executes that bytecode with the
Pyodide build whose CPython matches the bytecode version.

Usage:
    python3 tools/build-web-games.py [slug ...]      # all games by default

The extracted PyInstaller folders are produced with pyinstxtractor-ng, see
tools/README.md.
"""
import json
import os
import shutil
import sys
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PUBLIC = ROOT / "public" / "jugar"
EXTRACT_ROOT = Path(os.environ.get("GAME_EXTRACT_ROOT", "/tmp/opencode/extract"))

# slug -> (title, pyodide version matching the bytecode's CPython, extracted
# folder, entry .pyc inside it, files/dirs that belong to the game)
GAMES = {
    "arcspace": dict(
        title="ArcSpace",
        pyodide="0.29.5",  # Python 3.13
        folder="ARCSPACE.exe_extracted",
        entry="main.pyc",
        include=["assets", "data"],
    ),
    "cielo-cordobes": dict(
        title="El Cielo Cordobés",
        pyodide="0.29.5",  # Python 3.13
        folder="el cielo cordobez.exe_extracted",
        entry="main.pyc",
        include=["assets"],
        # The game ships its own package inside the PyInstaller archive.
        extra_from_pyz={"modules": "modules"},
    ),
    "preguntados-kids": dict(
        title="Preguntados Kids",
        pyodide="0.26.4",  # Python 3.12
        folder="Astro-Kids.exe_extracted",
        entry="preguntados_espacio.pyc",
        include=["fuentes", "gif", "imagenes", "preguntas.json"],
        # The game sizes its virtual surface from the reported screen size.
        screen=[1366, 768],
    ),
    "cartas-espaciales": dict(
        title="Cartas Espaciales",
        pyodide="0.29.5",
        # The original is a Tkinter desktop app, so this is a Pygame port that
        # keeps its rules and assets (see tools/recovered/cartas-espaciales).
        source="cartas-espaciales/main.py",
        entry="main.py",
        folder="cartas espaciales.exe_extracted",
        include=["imagenes", "sonidos"],
    ),
    "solar-defender": dict(
        title="Solar Defender",
        pyodide="0.29.5",
        # Python 3.10 bytecode: same story as Boom Cósmico, it runs from the
        # source recovered with PyLingual (tools/recovered/).
        source="solar-defender/main.py",
        entry="main.py",
        folder="Solar Defender.exe_extracted",
        include=["assets", "sounds", "datos-de-jugadores"],
    ),
    "viaje-galactico": dict(
        title="¡Viaje Galáctico!",
        pyodide="0.29.5",
        # The original is a Tkinter app that asked Gemini to generate the
        # narration. The port draws the solar system with Pygame, keeps the
        # same content and uses the browser voice instead.
        source="viaje-galactico/main.py",
        entry="main.py",
        folder="íViaje Galactico!.exe_extracted",
        include=["cuerpos_celestes.json", "logo aventura espacial.png", "logo_nacional.png"],
    ),
    "stellar-scrap": dict(
        title="Stellar Scrap",
        pyodide="314.0.7",  # Python 3.14
        folder="Stellar Scrap.exe_extracted",
        entry="main.pyc",
        include=["assets", "data"],
        # The game spreads itself over several modules inside the archive.
        pyz_modules=[
            "assets_manager",
            "asteroid",
            "bubble",
            "effects",
            "player",
            "save_system",
            "settings",
            "trash",
            "ui",
        ],
    ),
    "boom-cosmico": dict(
        title="Boom Cósmico",
        pyodide="0.29.5",
        # Python 3.10 bytecode has no pygame build in Pyodide, so this game runs
        # from the source recovered with PyLingual (tools/recovered/).
        source="boom-cosmico/main.py",
        entry="main.py",
        folder="Boom Cosmico.exe_extracted",
        include=[
            "ambiente_menu.wav",
            "arrows.png",
            "constelacion.wav",
            "estrella_nueva.wav",
            "estrella.wav",
            "gameover.wav",
            "golpe.wav",
            "icono.png",
            "musica.wav",
            "powerup.wav",
        ],
    ),
}

PAGE = """<!doctype html>
<html lang="es">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width,initial-scale=1" />
    <title>Jugar a {title}</title>
    <style>
      :root {{ color-scheme: dark; }}
      html, body {{ height: 100%; margin: 0; background: #05060a; overflow: hidden;
        font-family: system-ui, sans-serif; }}
      body {{ display: grid; place-items: center; }}
      #canvas {{ display: block; background: #000; }}
      #player-overlay {{ position: fixed; inset: 0; display: grid; place-items: center;
        padding: 24px; text-align: center; z-index: 10;
        background: radial-gradient(circle at 50% 20%, #101a3a 0%, #05060a 70%);
        transition: opacity 500ms cubic-bezier(0.32, 0.72, 0, 1); }}
      #player-overlay.is-hidden {{ opacity: 0; pointer-events: none; }}
      .panel {{ max-width: 420px; display: flex; flex-direction: column; gap: 16px;
        align-items: center; }}
      h1 {{ margin: 0; font-size: 24px; font-weight: 700; letter-spacing: -0.02em;
        color: #eef2ff; }}
      #player-status {{ margin: 0; font-size: 14px; line-height: 1.6; color: #93a2c4; }}
      #player-status.is-error {{ color: #ff9d9d; }}
      button {{ padding: 8px 12px; font-size: 16px; font-weight: 600; color: #fff;
        background: #3b62e8; border: 0; border-radius: 12px; cursor: pointer;
        transition: background 500ms cubic-bezier(0.32, 0.72, 0, 1); }}
      button:hover {{ background: #4f7fff; }}
      button:focus-visible {{ outline: 2px solid #9bb0ff; outline-offset: 2px; }}
      .hint {{ margin: 0; font-size: 12px; color: #64708c; }}
    </style>
  </head>
  <body>
    <canvas id="canvas" width="1280" height="720"></canvas>
    <div id="player-overlay">
      <div class="panel">
        <h1>{title}</h1>
        <p id="player-status">
          Se juega con teclado. La primera vez tarda unos segundos en cargar el motor.
        </p>
        <button id="player-start" type="button">▶ Jugar</button>
        <p class="hint">Si el teclado no responde, hacé clic sobre la imagen.</p>
      </div>
    </div>
    <script>
      window.GAME_CONFIG = {config};
    </script>
    <script src="/jugar/player.js"></script>
  </body>
</html>
"""


def build(slug: str) -> None:
    spec = GAMES[slug]
    source = EXTRACT_ROOT / spec["folder"]
    if not source.is_dir():
        raise SystemExit(f"missing extracted folder: {source}")

    target = PUBLIC / slug / "juego"
    target.mkdir(parents=True, exist_ok=True)
    archive = target / "game.zip"

    with zipfile.ZipFile(archive, "w", zipfile.ZIP_DEFLATED, compresslevel=6) as z:
        # Always shipped as main.pyc so the runner needs no per-game knowledge.
        if spec.get("source"):
            z.write(ROOT / "tools" / "recovered" / spec["source"], "main.py")
        else:
            z.write(source / spec["entry"], "main.pyc")
        for item in spec["include"]:
            path = source / item
            if path.is_file():
                z.write(path, item)
            elif path.is_dir():
                for root, _dirs, files in os.walk(path):
                    for name in files:
                        full = Path(root) / name
                        z.write(full, full.relative_to(source).as_posix())
            else:
                print(f"  ! {slug}: missing {item}")

        # Modules the game ships inside the PyInstaller PYZ archive.
        pyz = source / "PYZ.pyz_extracted"
        for name, dest in spec.get("extra_from_pyz", {}).items():
            path = pyz / name
            if path.is_file():
                z.write(path, dest)
            elif path.is_dir():
                for root, _dirs, files in os.walk(path):
                    for fname in files:
                        full = Path(root) / fname
                        z.write(full, (Path(dest) / full.relative_to(path)).as_posix())
            else:
                print(f"  ! {slug}: missing pyz module {name}")

        for name in spec.get("pyz_modules", []):
            path = pyz / f"{name}.pyc"
            if path.is_file():
                z.write(path, f"{name}.pyc")
            else:
                print(f"  ! {slug}: missing pyz module {name}.pyc")

    config = json.dumps(
        {
            "title": spec["title"],
            "pyodide": spec["pyodide"],
            # The zip always ships the entry point as main.py / main.pyc.
            "entry": "main.py" if spec.get("source") else "main.pyc",
            "archive": "game.zip",
            **({"screen": spec["screen"]} if spec.get("screen") else {}),
        },
        ensure_ascii=False,
    )
    (target / "index.html").write_text(
        PAGE.format(title=spec["title"], config=config), encoding="utf-8"
    )
    size = archive.stat().st_size / 1e6
    print(f"  {slug}: game.zip {size:.1f} MB -> {target}")


def main() -> None:
    wanted = sys.argv[1:] or list(GAMES)
    for slug in wanted:
        if slug not in GAMES:
            raise SystemExit(f"unknown game: {slug}")
        build(slug)


if __name__ == "__main__":
    main()
