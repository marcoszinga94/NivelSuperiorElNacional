#!/usr/bin/env python3
"""
Repairs the PyLingual output for Solar Defender.

PyLingual reconstructs almost everything, but it flags a few functions with
"Failure" and, in the ones with nested control flow, it collapses the nesting
(blocks end up one or two levels too deep, and `elif` chains become
`else: if`). That is syntactically valid but changes the meaning, so the
broken blocks are re-indented and the two save-game parsers are rewritten.

Run it once to regenerate tools/recovered/solar-defender/main.py:

    python3 tools/recovered/solar-defender/repair.py <decompiled_solar-defender.py>
"""
import re
import sys

GAMEDATA_LOAD = '''    def load():
        GameData.ensure_dir()
        data = {'high_score': 0, 'upgrades': {'size': 0, 'speed': 0, 'damage': 0, 'health': 0}, 'difficulty': 'normal'}
        try:
            if os.path.exists(GameData.SAVE_FILE):
                with open(GameData.SAVE_FILE, 'r') as f:
                    for line in f:
                        if ':' not in line:
                            continue
                        k, v = line.strip().split(':', 1)
                        k = k.strip()
                        v = v.strip()
                        if k == 'HIGH_SCORE':
                            data['high_score'] = int(v)
                        elif k in ['SIZE_LEVEL', 'SPEED_LEVEL', 'DAMAGE_LEVEL', 'HEALTH_LEVEL']:
                            data['upgrades'][k.lower().replace('_level', '')] = int(v)
                        elif k == 'DIFFICULTY':
                            data['difficulty'] = v
        except Exception as e:
            import traceback
            traceback.print_exc()
        return data
'''

PLAYERDB_LOAD = '''    def load():
        PlayerDB.ensure_dir()
        players = []
        try:
            if os.path.exists(PlayerDB.DB_FILE):
                with open(PlayerDB.DB_FILE, 'r') as f:
                    p = None
                    for line in f:
                        s = line.strip()
                        if s.startswith('JUGADOR:'):
                            if p is not None:
                                players.append(p)
                            p = {'name': s.split(':', 1)[1].strip(), 'color': '', 'score': 0, 'ship': '', 'gender': '', 'age': 0, 'level': 0, 'medals': 0, 'status': ''}
                        elif p is not None and ':' in s:
                            k, v = s.split(':', 1)
                            k = k.strip().lower()
                            v = v.strip()
                            if k == 'puntaje':
                                p['score'] = int(v)
                            elif k == 'nave':
                                p['color'] = v
                                p['ship'] = v
                            elif k == 'genero':
                                p['gender'] = v
                            elif k == 'edad':
                                p['age'] = int(v)
                            elif k == 'planeta':
                                p['level'] = int(v)
                            elif k == 'medallas':
                                p['medals'] = int(v)
                            elif k == 'estado':
                                p['status'] = v
                    if p is not None:
                        players.append(p)
        except Exception as e:
            import traceback
            traceback.print_exc()
        return sorted(players, key=lambda x: x['score'], reverse=True)
'''

SOUND_PLAY = '''    def play(self, name):
        if not self.enabled or name not in self.sounds:
            return
        try:
            self.sounds[name].play()
        except Exception:
            pass
'''


def shift(lines, first, last, delta):
    """Move a 1-based, inclusive line range in or out by `delta` spaces."""
    for i in range(first - 1, last):
        line = lines[i]
        if not line.strip():
            continue
        if delta < 0:
            remove = min(-delta, len(line) - len(line.lstrip(" ")))
            lines[i] = line[remove:]
        else:
            lines[i] = " " * delta + line


def main(path: str) -> None:
    lines = open(path, encoding="utf-8").read().split("\n")

    # Game.run: the mouse and keyboard branches were nested inside QUIT.
    shift(lines, 2099, 2146, -4)
    shift(lines, 2147, 2300, -8)
    # check_collisions: the body lost its `for enemy in self.enemies:` loop.
    shift(lines, 1482, 1500, +4)

    def replace(first, last, block):
        """Swap an inclusive 1-based line range for the given source block."""
        lines[first - 1 : last] = block.rstrip("\n").split("\n")

    # Bottom-up so the earlier line numbers stay valid.
    replace(1092, 1129, PLAYERDB_LOAD)
    replace(1044, 1068, GAMEDATA_LOAD)
    replace(151, 157, SOUND_PLAY)

    text = "\n".join(lines)
    # PyLingual leaves these markers behind; the web port fixes them.
    text = re.sub(r"[ \t]*# \*\*\*<module>\.[^\n]*Failure:[^\n]*\n", "", text)
    text = re.sub(r"[ \t]*# irreducible cflow[^\n]*\n", "", text)

    open(path, "w", encoding="utf-8").write(text)
    compile(text, path, "exec")
    print(f"repaired and compiles: {path}")


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "main.py")
