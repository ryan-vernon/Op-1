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

# Nitro, redrawn like the app's: a blue low-pass gauge, a red high-pass gauge, a road, the green FF marker and the white stick shifter
LV, V4 = "#B5B9E8", "#4A4AA8"
def nitro():
    v0 = v1 = v2 = v3 = 0.45
    o = ln("M12 20 L100 31 H352 L440 19", B, 1.4) + t(28, 66, "FREQ", B, 26, "start", 400) + t(424, 66, "FREQ", O, 26, "end", 400)
    lx, rx = 25 + v0 * 62, 427 - v3 * 62
    o += ln(f"M25 108 H{lx}", B) + dot(lx, 108, 4.5, B) + ln(f"M427 108 H{rx}", O) + dot(rx, 108, 4.5, O)
    for x1, y1, x2, y2 in [(36, 84, 41, 90), (59, 75, 59, 83), (78, 84, 73, 90), (86, 108, 94, 108)]:
        o += ln(f"M{x1} {y1} L{x2} {y2}", G) + ln(f"M{452-x1} {y1} L{452-x2} {y2}", G)
    o += ln("M155 70 H168 V63 H175 V55 H182 V62 H190 V38 H202 V52 H208 V44 H214 V66 H224 V50 H232 V64 H240 V48 H246 V70 H300", V4) + ln("M206 70 V40 H219 V70 M232 70 V52 H240 V70", B)
    for k in range(14):
        u = k / 13; y = 80 + u * u * 80 + u * 18; half = 40 + u * 150; seg = 8 + u * 22; gap = 5 + u * 14; x = 226 - half
        d = ""
        while x < 226 + half:
            x1, x2 = max(226 - half, x), min(226 + half, x + seg)
            if x2 > x1: d += f"M{x1:.1f} {y:.1f} H{x2:.1f} "
            x += seg + gap
        o += f'<g opacity="{0.45 + 0.55 * u:.2f}">' + ln(d, "#1A8A8A" if k < 5 else G) + "</g>"
    o += ln("M10 148 H145 L178 176 H442", B) + ln("M10 160 H140 L168 186", B) + ln("M298 186 H452 M298 186 V222", B) + ln("M186 186 V224 M262 186 V224", V4)
    o += "".join(ln(f"M270 {194 + k * 8} H288", V4) for k in range(3)) + circ(360, 205, 9, V4, "none", 1.4)
    gx = 78 + v1 * 62
    o += t(24, 198, "FF", G, 28, "start", 400) + ln("M66 180 H146", LV) + ln(f"M{gx} 158 V180", G) + "".join(t(74 + i * 22, 202, n, LV, 15, "middle", 400) for i, n in enumerate("4567"))
    o += "".join(ln(f"M{x} 214 H{x + 12}", c, 3) for x, c in [(22, G), (38, O), (60, V4), (78, W), (92, LV), (106, B), (122, G), (138, O)])
    sx = 196 + v2 * 60; by = 214; lxs = 226 + (sx - 226) * 0.35
    o += ln(f"M{sx} 168 L{lxs} {by - 4}", W, 5) + ln(f"M{sx} 168 L{lxs} {by - 4}", "#000", 2.5)
    o += f'<ellipse cx="226" cy="{by}" rx="22" ry="8" fill="none" stroke="{W}" stroke-width="1.4"/><ellipse cx="226" cy="{by + 5}" rx="28" ry="10" fill="none" stroke="{W}" stroke-width="1.4"/>'
    o += poly([(sx - 11, 140), (sx + 11, 140), (sx + 16, 156), (sx + 8, 170), (sx - 8, 170), (sx - 16, 156)], W, "none", 1.6) + t(sx, 162, "R", W, 17, "middle", 600)
    return (452, 234, o)
by["fx_nitro"]["art"] = nitro(); by["fx_nitro"]["ro"] = []
# Spring: the coil colour follows tone (blue to white)
def _mix(c1, c2, u): return "#" + "".join(f"{round(int(c1[i:i+2], 16) * (1 - u) + int(c2[i:i+2], 16) * u):02x}" for i in (1, 3, 5))
sp = by["fx_spring"]; aw, ah, art = sp["art"]
sp["art"] = (aw, ah, art.replace(f'stroke="{W}"', f'stroke="{_mix(B, W, 0.45)}"', 1))

# ---- Round 24: Punch, Phone and Cow from the original artwork (vectors extracted from the manual and the guide), live-style gauges, labels and numbers ----
import json
VEC = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "vec.json")))
def vec(V, dx=0, dy=0, sc=1):
    o = f'<g transform="translate({dx} {dy}) scale({sc}) translate({-V["ox"]} {-V["oy"]})">'
    for d, st, fi, w in V["items"]:
        o += f'<path d="{d}" fill="{fi or "none"}" stroke="{st or "none"}" stroke-width="{w or 0.6}" stroke-linecap="round" stroke-linejoin="round"/>'
    return o + "</g>"
def gauge(px, py, val, col):
    th = math.pi * (1 - val); o = ""
    for a in (200, 235, 270, 305, 340):
        r = math.radians(a); o += ln(f"M{px + 15*math.cos(r):.1f} {py + 15*math.sin(r):.1f} L{px + 19*math.cos(r):.1f} {py + 19*math.sin(r):.1f}", G)
    return o + ln(f"M{px} {py} L{px + 17*math.cos(th):.1f} {py - 17*math.sin(th):.1f}", col) + dot(px, py, 3, col)
LAV, LAV2, PUR, PNK2 = "#DFD9FF", "#ADADFF", "#9256D7", "#FF3A5D"
def lab(x, y, s_, c, a="start", sz=15): return t(x, y, s_, c, sz, a, 400)
punch_art = vec(VEC["punch"]) + lab(8, 16, "FREQ", PUR) + gauge(25, 43, .45, B) + lab(8, 67, "PUNCH", PUR) + num(5, 102, "45", G, 44) + lab(222, 16, "ROUNDS", G, "end") + num(219, 50, "45", LAV, 44, "end") + lab(222, 67, "POWER", G, "end") + num(219, 102, "45", PNK2, 44, "end")
for i in ("fx_punch", "mx_fx"): by[i]["art"] = (225, 107, punch_art); by[i]["ro"] = []
by["fx_phone"]["art"] = (226, 117, vec(VEC["phone"]) + lab(12, 22, "TONE", B) + gauge(32.5, 47, .45, B) + lab(12, 70, "PHONIC", G, sz=13) + num(14, 104, "45", LAV2, 44) + lab(212, 22, "BAUD", LAV, "end") + num(212, 56, "45", LAV2, 44, "end") + rect(176, 60, 38, 10, PNK2, sw=1.4) + t(195, 68, "TELEMATIC", PNK2, 7.5, "middle", 500) + num(212, 104, "45", LAV2, 44, "end"))
by["fx_phone"]["ro"] = []
by["fx_cwo"]["art"] = (230, 106, vec(VEC["cow"], 62, 12, 0.84) + lab(6, 16, "FREQ", B, sz=13) + gauge(25, 41, .45, B) + lab(6, 66, "DELAY", G, sz=13) + num(4, 100, "45", G, 40) + lab(226, 16, "FEEDBACK", W, "end", 13) + num(224, 50, "45", W, 40, "end") + lab(226, 66, "SIDEBAND", O, "end", 13) + num(224, 100, "45", O, 40, "end"))
by["fx_cwo"]["ro"] = []
# nitro: needles that turn, and an all-white stick shifter
_n = by["fx_nitro"]["art"][2]
_n = _n.replace(ln("M25 108 H%s" % (25 + .45*62), B), "").replace(dot(25 + .45*62, 108, 4.5, B), "").replace(ln("M427 108 H%s" % (427 - .45*62), O), "").replace(dot(427 - .45*62, 108, 4.5, O), "")
th1, th2 = math.pi * .55, math.pi * .45
_n += ln(f"M58 108 L{58 + 31*math.cos(th1):.1f} {108 - 31*math.sin(th1):.1f}", B) + dot(58, 108, 4.5, B) + ln(f"M394 108 L{394 + 31*math.cos(th2):.1f} {108 - 31*math.sin(th2):.1f}", O) + dot(394, 108, 4.5, O)
_n = _n.replace(LV if False else "#B5B9E8", "#B5B9E8")
by["fx_nitro"]["art"] = (452, 234, _n)

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
