#!/usr/bin/env python3
"""Extrae el icono embebido en los `.exe` de `public/Ejecutadores/`.

Dos modos:

    # A. un .ico por ejecutable (solo biblioteca estandar)
    python3 tools/extract-exe-icons.py public/Ejecutadores /tmp/iconos

    # B. el PNG normalizado que usan las tarjetas de /juegos (requiere ImageMagick)
    python3 tools/extract-exe-icons.py --png public/Ejecutadores public/juegos/icono

El lector de PE es propio: recorre `RT_GROUP_ICON` + `RT_ICON` y arma un `.ico`
valido por cada grupo. Windows guarda el icono como PNG (Formatos Vista en
adelante) o como DIB; en los dos casos el `.ico` armado se abre con cualquier
lector de iconos.

En el modo `--png` se elige el frame mas grande de cada grupo, se recorta el halo
casi transparente y se centra en un lienzo cuadrado de 252x252 con el nombre del
slug del juego.
"""

from __future__ import annotations

import os
import shutil
import struct
import subprocess
import sys
import tempfile

RT_ICON = 3
RT_GROUP_ICON = 14
DIRECTORY_ENTRY_RESOURCE = 2

# nombre del .exe (sin extension) -> slug usado por la pagina
SLUGS = {
    "ARCSPACE": "arcspace",
    "Astro-Kids": "preguntados-kids",
    "Boom Cosmico": "boom-cosmico",
    "cartas espaciales": "cartas-espaciales",
    "el cielo cordobez": "cielo-cordobes",
    "íViaje Galactico!": "viaje-galactico",
    "Solar Defender": "solar-defender",
    "Stellar Scrap": "stellar-scrap",
}


class PE:
    """Lector minimo de PE: solo lo necesario para llegar a los recursos."""

    def __init__(self, blob: bytes):
        self.b = blob
        if blob[:2] != b"MZ":
            raise ValueError("no es un .exe (no empieza con MZ)")
        pe_off = struct.unpack_from("<I", blob, 0x3C)[0]
        if blob[pe_off : pe_off + 4] != b"PE\0\0":
            raise ValueError("firma PE invalida")
        coff = pe_off + 4
        n_sections = struct.unpack_from("<H", blob, coff + 2)[0]
        opt_size = struct.unpack_from("<H", blob, coff + 16)[0]
        opt = coff + 20
        magic = struct.unpack_from("<H", blob, opt)[0]
        dir_off = opt + (96 if magic == 0x10B else 112)
        rva, size = struct.unpack_from("<II", blob, dir_off + DIRECTORY_ENTRY_RESOURCE * 8)
        if not rva:
            raise ValueError("el .exe no tiene recursos")
        self.sections = []
        sec = opt + opt_size
        for i in range(n_sections):
            raw = blob[sec + i * 40 : sec + (i + 1) * 40]
            v_size, v_addr, r_size, r_addr = struct.unpack_from("<IIII", raw, 8)
            self.sections.append((v_addr, v_size, r_addr, r_size))
        self.res_root = self.offset(rva)

    def offset(self, rva: int) -> int:
        for v_addr, v_size, r_addr, r_size in self.sections:
            if v_addr <= rva < v_addr + max(v_size, r_size):
                return r_addr + (rva - v_addr)
        raise ValueError(f"RVA {rva:#x} fuera de toda seccion")

    def entries(self, dir_off: int):
        """(id, nombre, offset) de un directorio de recursos."""
        named, ids = struct.unpack_from("<HH", self.b, dir_off + 12)
        out = []
        for i in range(named + ids):
            name, child = struct.unpack_from("<II", self.b, dir_off + 16 + i * 8)
            if name & 0x80000000:
                at = dir_off + 16 + i * 8
                ln = struct.unpack_from("<H", self.b, self.res_root + (name & 0x7FFFFFFF))[0]
                label = self.b[
                    self.res_root + (name & 0x7FFFFFFF) + 2 : self.res_root
                    + (name & 0x7FFFFFFF) + 2 + ln * 2
                ].decode("utf-16-le")
            else:
                label = name
            # el bit alto marca "esto es un subdirectorio, no un dato"
            out.append((label, self.res_root + (child & 0x7FFFFFFF)))
        return out

    def payload(self, data_entry_off: int) -> bytes:
        rva, size = struct.unpack_from("<II", self.b, data_entry_off)
        at = self.offset(rva)
        return self.b[at : at + size]

    def icon_groups(self) -> dict:
        """{id del grupo: [(id del icono, ancho, alto, bpp, bytes)]}."""
        groups, icons = {}, {}
        for rtype, tdir in self.entries(self.res_root):
            if rtype == RT_GROUP_ICON:
                for gid, gdir in self.entries(tdir):
                    for _lang, data in self.entries(gdir):
                        blob = self.payload(data)
                        count = struct.unpack_from("<H", blob, 4)[0]
                        items = []
                        for i in range(count):
                            off = 6 + i * 14
                            w, h, _colors, _res, _planes, bpp = struct.unpack_from(
                                "<BBBBHH", blob, off
                            )
                            iid = struct.unpack_from("<H", blob, off + 12)[0]
                            items.append((iid, w or 256, h or 256, bpp, None))
                        groups[gid] = items
            elif rtype == RT_ICON:
                for iid, idir in self.entries(tdir):
                    for _lang, data in self.entries(idir):
                        icons[iid] = self.payload(data)
        for gid, items in groups.items():
            groups[gid] = [(iid, w, h, bpp, icons.get(iid)) for iid, w, h, bpp, _ in items]
        return groups


def ico_bytes(frames: list) -> bytes:
    """Arma un .ico con los frames dados, que son (ancho, alto, bpp, bytes)."""
    header = struct.pack("<HHH", 0, 1, len(frames))
    directory, payload, offset = b"", b"", 6 + 16 * len(frames)
    for w, h, bpp, blob in frames:
        directory += struct.pack(
            "<BBBBHHII", w & 0xFF, h & 0xFF, 0, 0, 1, bpp, len(blob), offset
        )
        payload += blob
        offset += len(blob)
    return header + directory + payload


def valid_frame(blob: bytes | None) -> bool:
    """Un frame sirve si es un PNG o un DIB con datos suficientes para su tamaño."""
    if not blob:
        return False
    if blob[:8] == b"\x89PNG\r\n\x1a\n":
        return True
    if len(blob) < 40:
        return False
    header, width, height, _planes, bpp = struct.unpack_from("<IiiHH", blob, 0)
    if header not in (40, 52, 56, 64, 108, 124):
        return False
    if not 0 < width <= 4096 or height == 0 or abs(height) > 8192:
        return False
    # en un .ico el alto viene duplicado porque incluye la mascara AND
    xor_bytes = width * (abs(height) // 2) * max(bpp, 1) // 8
    return len(blob) >= 40 + xor_bytes


def write_ico(groups: dict, path: str) -> list:
    """Arma un .ico con todos los frames del grupo. Devuelve los tamaños."""
    sizes = []
    for gid, items in groups.items():
        valid = [(w, h, bpp, blob) for _iid, w, h, bpp, blob in items if valid_frame(blob)]
        if not valid:
            sizes.append((gid, []))
            continue
        with open(path, "wb") as fh:
            fh.write(ico_bytes(valid))
        sizes.append((gid, valid))
    return sizes


def biggest_frame(groups: dict):
    """El frame de mayor area (y a igual area, el de mas bits por pixel)."""
    candidates = [
        (w, h, bpp, blob)
        for items in groups.values()
        for _iid, w, h, bpp, blob in items
        if valid_frame(blob)
    ]
    if not candidates:
        return None
    return max(candidates, key=lambda f: (f[0] * f[1], f[2]))


def png_from_ico(frame: tuple, dst: str) -> None:
    """Recorta el halo sobrante y deja el icono centrado en un PNG cuadrado."""
    if shutil.which("magick") is None:
        raise RuntimeError("falta ImageMagick (magick)")
    with tempfile.NamedTemporaryFile(suffix=".ico", delete=False) as tmp:
        tmp.write(ico_bytes([frame]))
        tmp_path = tmp.name
    try:
        subprocess.run(
            [
                "magick", tmp_path,
                "-bordercolor", "none", "-border", "2", "-fuzz", "6%",
                "-trim", "+repage",
                "-filter", "Lanczos", "-resize", "232x232",
                "-background", "none", "-gravity", "center", "-extent", "252x252",
                dst,
            ],
            check=True,
        )
    finally:
        os.remove(tmp_path)


def main() -> int:
    args = [a for a in sys.argv[1:] if a != "--png"]
    as_png = len(args) != len(sys.argv[1:])
    src = args[0] if len(args) > 0 else "public/Ejecutadores"
    dst = args[1] if len(args) > 1 else ("public/juegos/icono" if as_png else "/tmp/iconos")
    if not os.path.isdir(src):
        print(f"no existe la carpeta {src}")
        return 1
    if as_png:
        os.makedirs(dst, exist_ok=True)
    for name in sorted(os.listdir(src)):
        if not name.lower().endswith(".exe"):
            continue
        path = os.path.join(src, name)
        base = os.path.splitext(name)[0]
        print(name)
        try:
            with open(path, "rb") as fh:
                groups = PE(fh.read()).icon_groups()
        except Exception as exc:  # noqa: BLE001
            print(f"  ERROR: {exc}")
            continue
        if not groups:
            print("  sin iconos")
            continue
        if as_png:
            slug = SLUGS.get(base)
            if slug is None:
                print(f"  sin slug asignado en SLUGS: {base}")
                continue
            frame = biggest_frame(groups)
            if frame is None:
                print("  el icono del .exe esta vacio o roto: la tarjeta usa el emoji")
                continue
            out = os.path.join(dst, f"{slug}.png")
            try:
                png_from_ico(frame, out)
            except Exception as exc:  # noqa: BLE001
                print(f"  no se pudo convertir: {exc}")
                continue
            print(f"  {frame[0]}x{frame[1]}@{frame[2]}bpp -> {os.path.basename(out)}")
            continue
        os.makedirs(dst, exist_ok=True)
        ico = os.path.join(dst, f"{base}.ico")
        for gid, frames in write_ico(groups, ico):
            if not frames:
                print(f"  grupo {gid}: el recurso de icono esta vacio")
                continue
            detail = ", ".join(
                f"{w}x{h}@{bpp}bpp{'/png' if blob[:8] == b'\x89PNG\r\n\x1a\n' else ''}"
                for w, h, bpp, blob in frames
            )
            print(f"  grupo {gid} -> {os.path.basename(ico)}: {detail}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
