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
import subprocess
import sys
import tempfile
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PUBLIC = ROOT / "public" / "jugar"
EXTRACT_ROOT = Path(os.environ.get("GAME_EXTRACT_ROOT", "/tmp/opencode/extract"))

# Optimización de assets: los juegos traen imágenes enormes que se ven a 200 px.
IMAGE_MAX = 1280   # lado mayor para imágenes comunes
GIF_MAX = 720      # los GIF son fondos animados, con menos alcanza
IMAGE_EXT = {".png", ".jpg", ".jpeg", ".gif", ".bmp", ".webp"}
VIDEO_EXT = {".mp4", ".avi", ".mov", ".mkv", ".webm", ".wmv"}
AUDIO_EXT = {".ogg", ".mp3"}
AUDIO_KB = 900      # recodificar música más pesada que esto
AUDIO_QUALITY = {"-c:a", "libvorbis", "-q:a", "3"}  # ogg; mp3 usa bitrate fijo


def _limit_for(arcname: str, rules, default: int) -> int:
    """Primer prefijo que coincide define el tamaño máximo de esa imagen."""
    for prefix, limit in rules:
        if prefix and arcname.startswith(prefix):
            return limit
    return default


def _reencode_audio(path: Path, out_dir: Path):
    out = out_dir / path.name
    codec = (
        ["-c:a", "libvorbis", "-q:a", "3"]
        if path.suffix.lower() == ".ogg"
        else ["-c:a", "libmp3lame", "-b:a", "96k"]
    )
    subprocess.run(
        ["ffmpeg", "-y", "-v", "error", "-i", str(path)] + codec + ["-vn", str(out)],
        check=False,
        timeout=300,
    )
    if out.exists() and out.stat().st_size < path.stat().st_size:
        return out
    return None


def _dimensions(path: Path):
    try:
        out = subprocess.run(
            ["ffprobe", "-v", "error", "-select_streams", "v:0",
             "-show_entries", "stream=width,height", "-of", "csv=p=0", str(path)],
            capture_output=True, text=True, timeout=30,
        ).stdout.strip()
        width, height = out.split(",")[:2]
        return int(width), int(height)
    except Exception:
        return None


def _shrink(path: Path, out_dir: Path, limit: int, animated: bool):
    """Reescala una imagen si excede el límite. Devuelve el archivo nuevo o None."""
    size = _dimensions(path)
    if not size:
        return None
    out = out_dir / path.name
    if animated:
        # Los GIF animados se animaban con PIL, que en el navegador no existe:
        # el juego ya mostraba solo el primer cuadro. Nos quedamos con ese.
        vf = f"scale='min({limit},iw)':-1:flags=lanczos"
        subprocess.run(
            ["ffmpeg", "-y", "-v", "error", "-i", str(path),
             "-vf", vf, "-frames:v", "1", "-loop", "0", str(out)],
            check=False,
            timeout=300,
        )
        if out.exists() and out.stat().st_size < path.stat().st_size:
            return out
        return None
    if max(size) <= limit:
        return None
    vf = f"scale='min({limit},iw)':-2:flags=lanczos"
    base = ["ffmpeg", "-y", "-v", "error", "-i", str(path), "-vf", vf]
    for extra in (["-compression_level", "9"], []):
        subprocess.run(base + extra + [str(out)], check=False, timeout=300)
        if out.exists() and out.stat().st_size > 0:
            break
    if out.exists() and out.stat().st_size < path.stat().st_size:
        return out
    return None


# slug -> (title, pyodide version matching the bytecode's CPython, extracted
# folder, entry .pyc inside it, files/dirs that belong to the game)
GAMES = {
    "arcspace": dict(
        title="ArcSpace",
        pyodide="0.29.5",  # Python 3.13
        folder="ARCSPACE.exe_extracted",
        entry="main.pyc",
        include=["assets", "data"],
        # Fotos de planetas y objetos que se ven a ~200 px.
        image_rules=[
            ("assets/Graphics/Reales/", 512),
            ("assets/Graphics/Astros/", 512),
            ("assets/Graphics/Keyboard & Mouse/", 128),
        ],
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
        # Las cartas se dibujan a ~150 px y los botones a 50; solo las pantallas
        # completas necesitan resolución grande.
        image_rules=[
            ("imagenes/fondo", 1280),
            ("imagenes/instrucciones", 1280),
            ("imagenes/ganador", 1280),
            ("imagenes/perdiste", 1280),
            ("imagenes/records.png", 1280),
            ("imagenes/", 256),
        ],
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
        # 16 MB de WAV de ambiente -> OGG (el source ya apunta a ambient.ogg).
        audio_to_ogg=["sounds/ambient.wav"],
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
    <link rel="preconnect" href="https://cdn.jsdelivr.net" crossorigin />
    <link rel="dns-prefetch" href="https://cdn.jsdelivr.net" />
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

    reasons = {"imagenes": 0, "gif": 0, "audio": 0, "video": 0}
    with tempfile.TemporaryDirectory() as tmpdir:
        tmp = Path(tmpdir)

        def add(path: Path, arcname: str) -> None:
            """Agrega un archivo, encogiéndolo si es de los pesados."""
            suffix = path.suffix.lower()
            if suffix in VIDEO_EXT:
                reasons["video"] += 1
                return
            if str(arcname) in spec.get("audio_to_ogg", []):
                return  # se agrega convertido, abajo
            if suffix in IMAGE_EXT:
                if suffix == ".gif":
                    limit = GIF_MAX
                else:
                    limit = _limit_for(arcname, spec.get("image_rules", []), IMAGE_MAX)
                shrunk = _shrink(path, tmp, limit, suffix == ".gif")
                if shrunk:
                    reasons["gif" if suffix == ".gif" else "imagenes"] += 1
                    z.write(shrunk, arcname)
                    return
            if suffix in AUDIO_EXT and path.stat().st_size > AUDIO_KB * 1024:
                lighter = _reencode_audio(path, tmp)
                if lighter:
                    reasons["audio"] += 1
                    z.write(lighter, arcname)
                    return
            z.write(path, arcname)

        with zipfile.ZipFile(archive, "w", zipfile.ZIP_DEFLATED, compresslevel=6) as z:
            # Always shipped as main.pyc so the runner needs no per-game knowledge.
            if spec.get("source"):
                z.write(ROOT / "tools" / "recovered" / spec["source"], "main.py")
            else:
                z.write(source / spec["entry"], "main.pyc")

            for item in spec["include"]:
                path = source / item
                if path.is_file():
                    add(path, item)
                elif path.is_dir():
                    for root, _dirs, files in os.walk(path):
                        for name in sorted(files):
                            full = Path(root) / name
                            add(full, full.relative_to(source).as_posix())
                else:
                    print(f"  ! {slug}: missing {item}")

            # Audio muy pesado que conviene pasar a OGG (mismo nombre, otra extensión).
            for wav in spec.get("audio_to_ogg", []):
                original = source / wav
                converted = tmp / (Path(wav).stem + ".ogg")
                subprocess.run(
                    ["ffmpeg", "-y", "-v", "error", "-i", str(original),
                     "-c:a", "libvorbis", "-q:a", "4", str(converted)],
                    check=False,
                    timeout=300,
                )
                if converted.exists():
                    reasons["audio"] += 1
                    z.write(converted, str(Path(wav).with_suffix(".ogg")))
                else:
                    print(f"  ! {slug}: no se pudo convertir {wav}")
                    add(original, wav)

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

    resumen = ", ".join(f"{k}: {v}" for k, v in reasons.items() if v)
    if resumen:
        print(f"    optimizado -> {resumen}")

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
