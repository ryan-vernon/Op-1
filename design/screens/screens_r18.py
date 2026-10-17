"""Round 18 changes to the drawings: no corner numbers except the Tombola (and the numbers inside Punch, Phone, Delay and Grid,
which the original draws), Crank and Bend removed, a centred spring coil, an outlined mixer knob, one uniform line weight."""
import math, os, sys, re
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import screens as base
import screens_r13
from screens import t, num, ln, circ, dot, rect, poly, B, G, W, O, P, PK, CY, GR, DIM
S = base.S
base.S[:] = [s for s in S if s["id"] not in ("lfo_crank", "lfo_bend")]
by = {s["id"]: s for s in base.S}
for s in base.S:
    if s["id"] not in ("seq_tombola",): s["ro"] = []

def embed(i, aw, ah, parts, dx, dy=0, W2=None, H2=None):
    s = by[i]; ow, oh, art = s["art"]
    s["art"] = (W2 or aw, H2 or ah, f'<g transform="translate({dx} {dy})">{art}</g>' + parts); s["ro"] = []
def lbl(x, y, s, c, a="start"): return t(x, y, s, c, 11, a, 500, 0.8)
# Punch and master effect: the four numbers sit in the corners of the 2:1 picture, as in the original
def four(tl, bl, tr, br, w, h):
    o = lbl(0, 10, tl[0], tl[1]) + circ(11, 32, 9, tl[1], "none", 1.4) + ln("M11 32 L16 25", tl[1], 1.4)
    o += lbl(0, h - 44, bl[0], bl[1]) + num(0, h - 6, "45", bl[1], 40)
    o += lbl(w, 10, tr[0], tr[1], "end") + num(w, 48, "45", tr[1], 40, "end")
    o += lbl(w, h - 44, br[0], br[1], "end") + num(w, h - 6, "45", br[1], 40, "end")
    return o
for i in ("fx_punch", "mx_fx"): embed(i, 316, 132, four(("FREQ", P), ("PUNCH", G), ("ROUNDS", G), ("POWER", PK), 316, 132), 80, 6)
embed("fx_phone", 316, 132, four(("TONE", B), ("PHONIC", G), ("BAUD", W), ("TELEMATIC", PK), 316, 132), 50, 8)
# Delay: feedback and speed on the right; Grid: mix at the top right
embed("fx_delay", 290, 120, lbl(290, 10, "FDB", G, "end") + num(290, 50, "45", G, 40, "end") + lbl(290, 74, "SPEED", W, "end") + num(290, 114, "45", W, 40, "end"), 0)
embed("fx_grid", 250, 120, lbl(250, 10, "MIX", PK, "end") + num(250, 36, "45", PK, 22, "end"), 0)
# Spring: the coil is centred on the straight lines at both ends
N = 11; pts = []; x0 = 64; x1 = 214; a_ = (x1 - x0) / (2 * math.pi * N)
th0 = math.pi / 2
for k in range(int(N * 28) + 1):
    th = th0 + 2 * math.pi * N * k / (N * 28)
    pts.append((a_ * (th - th0) - 6.5 * (math.sin(th) - 1) + x0, 60 - 16 * math.cos(th)))
coil = "M40 60 H%.1f" % pts[0][0] + "".join(f" L{x:.1f} {y:.1f}" for x, y in pts) + f" H246"
a = t(0, 72, "T", B, 40, "start", 200) + ln(coil, W, 1.4) + t(140, 14, "TURNS", G, 14, "middle", 400) + t(140, 112, "DAMP", W, 14, "middle", 400)
a += ln("M270 24 V96", PK, 1.6, 'stroke-dasharray="2 4"') + dot(270, 24, 3, PK) + dot(270, 96, 3, PK)
by["fx_spring"]["art"] = (276, 118, a)
# Mixer: the four knobs are outlines
m = by["mx_mixer"]; aw, ah, art = m["art"]
art = re.sub(r'(<circle cx="[\d.]+" cy="70" r="8") fill="(#[0-9A-Fa-f]+)" stroke="\2"', r'\1 fill="none" stroke="\2"', art)
cols = re.findall(r'<circle cx="[\d.]+" cy="70" r="8" fill="none" stroke="(#[0-9A-Fa-f]+)"', art)
parts = art.split('stroke="#0A0A0A"')
art = parts[0]
for k, p in enumerate(parts[1:]): art += f'stroke="{cols[k] if k < len(cols) else W}"' + p
m["art"] = (aw, ah, art)

# one line weight for the whole screen: stroke widths are given in screen units and divided by the art scale
LW = 1.4
def _fit_scale(box, aw, ah): return min(box[0] / aw, box[1] / ah)
def uniform(art, s): return re.sub(r'stroke-width="[\d.]+"', f'stroke-width="{LW / s:.3f}"', art)
_tall, _wide = base.tall, base.wide
def tall(sc, header=True):
    aw, ah, art = sc["art"]; ro = sc["ro"]
    box = (296, 196) if ro else (296, 296)
    s2 = dict(sc); s2["art"] = (aw, ah, uniform(art, _fit_scale(box, aw, ah))); return _tall(s2, header)
def wide(sc):
    aw, ah, art = sc["art"]; ro = sc["ro"] if sc["wide_ro"] else []
    box = (176, 140) if ro else (304, 144)
    s2 = dict(sc); s2["art"] = (aw, ah, uniform(art, _fit_scale(box, aw, ah))); return _wide(s2)
