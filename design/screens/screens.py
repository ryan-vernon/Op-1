"""OP-1 screen definitions. Each screen = main art (own box) + readouts.
wide(): 320x160 (OP-1 2:1, iPad). tall(): 320x338 (phone)."""
import math
B, G, W, O = "#5B7CFA", "#1ED68F", "#E9E9E9", "#FF4D3D"
P, PK, CY, GR, DIM = "#6E56E8", "#FF4F8B", "#2EC4F2", "#8A8A8A", "#2E2E52"
FONT = "Encode Sans Condensed, sans-serif"

def t(x, y, s, c=W, sz=10, a="start", w=400, ls=0.6):
    return f'<text x="{x}" y="{y}" fill="{c}" font-size="{sz}" font-weight="{w}" text-anchor="{a}" letter-spacing="{ls}">{s}</text>'
def num(x, y, s, c=W, sz=30, a="start"):
    return f'<text x="{x}" y="{y}" fill="{c}" font-size="{sz}" font-weight="200" text-anchor="{a}">{s}</text>'
def ln(d, c=W, w=1.4, extra=""):
    return f'<path d="{d}" fill="none" stroke="{c}" stroke-width="{w}" stroke-linecap="round" stroke-linejoin="round" {extra}/>'
def circ(x, y, r, c=W, fill="none", w=1.4):
    return f'<circle cx="{x}" cy="{y}" r="{r}" fill="{fill}" stroke="{c}" stroke-width="{w}"/>'
def dot(x, y, r, c):
    return f'<circle cx="{x}" cy="{y}" r="{r}" fill="{c}"/>'
def rect(x, y, w, h, c=W, fill="none", sw=1.4, rx=0, extra=""):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{fill}" stroke="{c}" stroke-width="{sw}" {extra}/>'
def hexp(cx, cy, r, rot=0):
    return " ".join(f"{cx + r*math.cos(math.radians(60*i+rot)):.1f},{cy + r*math.sin(math.radians(60*i+rot)):.1f}" for i in range(6))
def poly(pts, c=W, fill="none", w=1.4):
    return f'<polygon points="{pts}" fill="{fill}" stroke="{c}" stroke-width="{w}" stroke-linejoin="round"/>'
def dial(x, y, r, ang, c, tick=True):
    a = math.radians(ang - 90)
    s = circ(x, y, r, c) + ln(f"M{x} {y} L{x + r*0.85*math.cos(a):.1f} {y + r*0.85*math.sin(a):.1f}", c, 1.6) + dot(x, y, 1.8, c)
    if tick:
        for k in range(-135, 136, 45):
            b = math.radians(k - 90)
            s += ln(f"M{x + (r+3)*math.cos(b):.1f} {y + (r+3)*math.sin(b):.1f} L{x + (r+6)*math.cos(b):.1f} {y + (r+6)*math.sin(b):.1f}", c, 1)
    return s
def sine(x0, y0, w, amp, cycles, c, sw=1.6, n=60):
    pts = [f"{x0 + w*i/n:.1f},{y0 - amp*math.sin(2*math.pi*cycles*i/n):.1f}" for i in range(n+1)]
    return f'<polyline points="{" ".join(pts)}" fill="none" stroke="{c}" stroke-width="{sw}" stroke-linejoin="round"/>'
def wave(x0, y0, w, h, seed, c, sw=1.4, n=90, peaks=()):
    import random
    r = random.Random(seed); pts = []
    for i in range(n+1):
        x = x0 + w*i/n; base = 0.08 + 0.12*r.random()
        for (px, ph) in peaks:
            d = abs(i/n - px); base += ph*max(0, 1 - d*14)*(0.6 + 0.4*r.random())
        pts.append(f"{x:.1f},{y0 - h*min(base,1):.1f}")
    return f'<polyline points="{" ".join(pts)}" fill="none" stroke="{c}" stroke-width="{sw}" stroke-linejoin="round"/>'


def swv(x, y, c, k=1.0):
    return f'<path transform="translate({x} {y}) scale({k})" d="M0 12 V4 a2.5 2.5 0 0 1 5 0 v6 a2.5 2.5 0 0 0 5 0 V4 a2.5 2.5 0 0 1 5 0 v6 a2.5 2.5 0 0 0 5 0 V0" fill="none" stroke="{c}" stroke-width="{1.6/k:.2f}" stroke-linecap="round"/>'
def metro(x, y, c, k=1.0):
    return f'<path transform="translate({x} {y}) scale({k})" d="M6 0 H10 L16 22 H0 Z M8 18 L14 4" fill="none" stroke="{c}" stroke-width="{1.4/k:.2f}" stroke-linejoin="round"/>'

S = []  # (id, group, title, (artW, artH, art), readouts[(label,value,color)], wide_readouts:bool)
def add(i, g, title, art, ro=(), wide_ro=True):
    S.append(dict(id=i, group=g, title=title, art=art, ro=list(ro), wide_ro=wide_ro))

# ---------- Synth engines ----------
a = "".join(dial(45 + 70*k, 16, 8, ang, c) for k, (ang, c) in enumerate([(-60, B), (-30, G), (-45, W), (-25, O)]))
for c, d in [(CY, "M0 70 C40 70 60 69 90 66 S150 52 170 64 S230 80 260 66 S290 64 300 64"),
             (P, "M0 80 C50 80 90 76 120 62 S180 52 210 72 S260 82 300 78"),
             (PK, "M0 94 C30 94 40 78 60 80 S80 36 120 36 S160 82 200 86 S260 90 300 88"),
             (O, "M0 100 C40 100 80 98 120 97 S220 96 300 96"),
             (B, "M0 66 C60 66 100 66 140 64 S200 70 300 70")]:
    a += ln(d, c, 1.6)
add("eng_cluster", "Synth engines", "Cluster", (300, 108, a), [("WAVES", "06", B), ("WAVE ENV", "34", G), ("SPREAD", "45", W), ("UNITOR", "23", O)], False)
a = ln("M30 12 L220 62 L50 92 L22 44 Z", P, 1.6) + ln("M0 80 L220 62 L196 34", P, 1.6)
a += dot(30, 12, 3.5, W) + dot(22, 44, 3.5, B) + dot(0, 80, 3.5, B) + dot(50, 92, 3.5, B) + dot(196, 34, 3.5, G) + dot(220, 62, 3.5, O)
add("eng_digital", "Synth engines", "Digital", (222, 98, a), [("WAVE SHAPER", "34", B), ("OCTAVE", "+1", G), ("DETUNE/RING", "12", W), ("DIGITALNESS", "45", O)], False)
a = t(0, 12, "MAX", P, 10, w=600) + t(0, 98, "MIN", P, 10, w=600) + "".join(ln(f"M24 {10+k*9} H38", G, 1.6) for k in range(10))
cols = [B]*4 + [CY]*2 + [G]*3 + [W]*4 + [PK]*3 + [O]*3
for k, c in enumerate(cols):
    x = 60 + k*7
    a += ln(f"M{x} 6 C{x+4} 40 {x+10} 70 {x+40} 84 L{x+96} 92", c, 1.3)
a += ln("M60 10 C64 40 64 70 110 106 L160 110", B, 1.2, 'stroke-dasharray="3 3"') + ln("M120 104 L280 88 M160 112 L300 96", P, 1)
a += dot(258, 82, 3, W) + ln("M258 82 L272 88", W) + dot(150, 108, 3, W) + ln("M150 108 L164 112", W) + ln("M280 6 V60", PK, 1)
add("eng_string", "Synth engines", "String", (300, 114, a), [("TENSION", "34", B), ("IMPULSE DEC", "45", G), ("DETUNE", "12", W), ("IMPULSE TYPE", "02", O)], False)
a = t(0, 14, "F", B, 16) + circ(22, 9, 6, B) + circ(32, 9, 6, B) + ln("M46 14 H56 V4 H62 V14 H70 V4 H76 V14 H96 V4 H102 V14 H110 V4 H116 V14 H130", CY)
a += t(146, 14, "M", O, 16) + ln("M164 6 H192 M164 12 H172 V16 H184 V12 H192", O)
a += ln("M0 112 H54 V30 H64 V112 H98 V66 H106 V112 H170 V26 H180 V112 H222 V66 H230 V112 H260", W, 1.6)
a += ln("M24 30 V112 M54 76 H110 M118 50 H220", CY, 1, 'stroke-dasharray="2 3"') + t(14, 74, "H", CY, 14) + t(76, 66, "T", CY, 14) + t(124, 48, "L", CY, 12)
add("eng_pulse", "Synth engines", "Pulse", (262, 114, a), [("FILTER", "34", B), ("AMPLITUDE", "45", G), ("2ND PULSE", "12", W), ("MODULATION", "23", O)], False)
a = "".join(poly(hexp(x, y, 22, 30), DIM) for x, y in [(30, 30), (110, 50), (66, 92), (130, 96)])
a += poly(hexp(30, 30, 20, 30), "#22306E") + num(30, 40, "02", B, 26, "middle")
a += poly(hexp(74, 50, 24, 30), G) + num(74, 60, "34", G, 26, "middle")
a += num(130, 72, "23", O, 26, "middle") + num(70, 104, "02", W, 26, "middle")
add("eng_fm", "Synth engines", "FM", (156, 118, a), [("TOPOLOGY", "03", B), ("FREQ", "45", G), ("FM AMOUNT", "62", W), ("DETUNE", "12", O)], False)
a = ln("M10 4 V110 M0 66 H120", GR, 1) + sine(10, 66, 90, 50, 1, B) + sine(10, 66, 90, 30, 1.1, G) + t(78, 22, "B", B, 14) + t(32, 100, "A", G, 14)
a += dot(14, 66, 3, G) + dot(98, 66, 3, G) + ln("M10 92 H100 M10 44 H100", "#244a80", 1, 'stroke-dasharray="2 3"')
a += ln("M150 4 V110 M146 44 H270", GR, 1) + ln("M150 44 H270", W, 1.2, 'stroke-dasharray="4 3"') + sine(154, 66, 116, 40, 3.5, O) + sine(154, 66, 116, 40, 2.4, "#5a1d2a", 1.2)
a += t(260, 22, "R", W, 14) + t(160, 96, "W", "#6a1d2d", 14) + dot(158, 66, 3, O) + dot(150, 44, 2.5, W)
add("eng_phase", "Synth engines", "Phase", (272, 112, a), [("PHASE SHIFT", "34", B), ("DISTORTION", "45", G), ("PHASE FILTER", "12", W), ("PHASE TILT", "23", O)], False)
a = ""
for row, yy in enumerate([20, 52]):
    for k in range(18):
        x = 6 + k*17 + row*6
        a += ln(f"M{x} {yy+22} L{x+12} {yy}", O, 1.6)
a += ln("M0 46 L16 40 M290 44 L306 40", O, 1.4)
add("eng_drwave", "Synth engines", "Dr Wave", (310, 80, a), [("WAVE TYPE", "34", B), ("FILTER", "45", G), ("PHASE", "12", W), ("CHORUS", "23", O)], False)
a = wave(20, 18, 260, 14, 3, B, 1, 70, ((0.3, .5), (0.85, .4)))
a += wave(10, 108, 280, 90, 7, B, 1.3, 110, ((0.06, .7), (0.4, .8), (0.43, .6), (0.7, .9), (0.74, .7)))
a += ln("M42 40 V110 M150 40 V110 M246 40 V110", B, 1, 'stroke-dasharray="2 3"') + ln("M286 30 V110", O, 1.6) + ln("M10 46 H286", B, .8, 'stroke-dasharray="2 3"')
a += circ(42, 94, 5, B, w=1.6) + dot(42, 94, 1.8, B) + circ(150, 104, 5, G, w=1.6) + dot(150, 104, 1.8, G) + circ(246, 60, 5, W, w=1.6) + dot(246, 60, 1.8, W)
add("eng_sampler", "Synth engines", "Synth sampler", (300, 114, a), [("START", "0.12", B), ("LOOP IN", "0.40", G), ("LOOP OUT", "0.92", W), ("END", "1.10", O)], False)

# ---------- Synth pages ----------
a = ln("M10 100 Q30 10 70 6", B, 2) + ln("M70 6 Q86 54 130 56", G, 2) + ln("M130 56 H220", W, 2) + ln("M220 56 Q250 98 280 100", O, 2)
a += ln("M70 6 V100 M130 56 V100 M220 56 V100", "#2A2A2A", 1, 'stroke-dasharray="3 3"') + ln("M10 100 H280", "#3A3A3A", 1.2)
a += dot(10, 100, 3.5, B) + dot(70, 6, 3.5, G) + dot(130, 56, 3.5, W) + dot(220, 56, 3.5, O) + dot(280, 100, 3.5, B)
add("pg_envelope", "Synth pages", "T2 · Envelope", (290, 106, a), [("ATTACK", "12", B), ("DECAY", "40", G), ("SUSTAIN", "62", W), ("RELEASE", "30", O)], False)
a = t(0, 34, "PLAYMODE", B, 30, w=200) + t(200, 34, "POLY", B, 30, w=200) + t(0, 80, "PORTAMENTO", G, 30, w=200) + t(200, 80, "01", G, 30, w=200)
add("pg_playmode", "Synth pages", "T2 + SHIFT · Play mode", (270, 88, a))
a = t(0, 24, "TONE", "#3a5aa0", 14) + t(0, 74, "45", "#3a5aa0", 30, w=200) + t(210, 24, "BAUD", "#555", 14) + t(210, 74, "45", "#555", 30, w=200)
a += rect(84, 34, 34, 22, B, sw=1.6) + t(101, 51, "FX", B, 16, "middle") + num(128, 56, "OFF", W, 34)
add("pg_fxoff", "Synth pages", "T3 · Effect off", (260, 80, a))

# ---------- Effects ----------
a = '<ellipse cx="80" cy="56" rx="62" ry="40" fill="none" stroke="#E9E9E9" stroke-width="1.6"/>'
a += ln("M30 34 Q16 10 34 6 M130 34 Q144 10 126 6", W) + '<ellipse cx="80" cy="74" rx="30" ry="16" fill="none" stroke="#E9E9E9" stroke-width="1.6"/>'
a += dot(70, 74, 3, W) + dot(90, 74, 3, W) + dot(58, 44, 3, W) + dot(102, 44, 3, W) + '<ellipse cx="42" cy="58" rx="10" ry="7" fill="#E9E9E9" opacity="0.25"/>'
add("fx_cwo", "Effects", "CWO (not in the v1.2 manual)", (160, 100, a), [("A", "45", B), ("B", "45", G), ("C", "45", W), ("D", "45", O)])
a = rect(60, 4, 106, 106, P, sw=1.2) + t(66, 16, "R", P, 10) + "".join(circ(110 - k*8, 57, 18 + k*12, B if k < 2 else "#3c4fa0", w=1.4) for k in range(4))
a = f'<defs><clipPath id="dlc"><rect x="60" y="4" width="106" height="106"/></clipPath></defs><g clip-path="url(#dlc)">{a}</g>' + rect(60, 4, 106, 106, P, sw=1.2)
a += ln("M0 57 H112", O, 1.6) + t(0, 52, "INPUT", O, 10, w=600) + dot(112, 57, 2.5, O)
add("fx_delay", "Effects", "Delay", (170, 114, a), [("SIZE", "45", B), ("SPEED", "45", G), ("FEEDBACK", "45", P), ("MIX", "45", O)])
a = poly("10,70 120,30 210,62 100,104", B, w=1.6) + poly("10,70 10,78 100,112 100,104", B) + poly("100,112 210,70 210,62 100,104", B)
a += "".join(ln(f"M{10+k*11} {70-k*4} L{100+k*11} {104-k*4.2}", "#33449a", .8) for k in range(1, 10)) + "".join(ln(f"M{10+k*9} {70+k*3.4} L{120+k*9} {30+k*3.2}", "#33449a", .8) for k in range(1, 10))
a += poly("70,52 110,38 140,48 100,62", G, w=1.6) + poly("70,52 70,64 100,74 100,62", G) + poly("100,74 140,60 140,48 100,62", G)
add("fx_grid", "Effects", "Grid", (214, 114, a), [("X SIZE", "45", B), ("Y SIZE", "45", G), ("Z FDB", "45", W), ("MIX", "45", O)])
a = ln("M0 8 Q90 18 180 18 Q270 18 360 8", B, 2) + "".join(ln(f"M{180-30-k*22} {40+k*10} H{180+30+k*22}", G, 1.2, 'stroke-dasharray="6 4"') for k in range(6))
a += ln("M150 30 V18 M160 30 V22 M170 30 V12 M180 30 V24 M190 30 V16 M200 30 V22 M210 30 V26", B, 1.2)
a += rect(170, 52, 20, 18, W, sw=1.4, rx=4) + t(180, 66, "R", W, 12, "middle", 600) + ln("M180 70 V96 M168 96 H192 L196 104 H164 Z", W)
a += ln("M20 104 H120 L150 82 M240 104 H340 L360 84", B, 1.6)
add("fx_nitro", "Effects", "Nitro", (362, 110, a), [("FREQ", "45", B), ("FF", "45", G), ("RES", "45", W), ("FREQ", "45", O)])
a = ln("M20 64 Q30 34 70 30 L150 18 Q178 16 182 34 L184 50 Q182 64 160 70 L80 92 Q40 100 26 84 Z", W, 1.6)
a += ln("M60 46 L120 34 M70 58 L132 46 M80 70 L140 58", W, 1.2) + "".join(dot(100 + (k % 3)*10, 66 + (k//3)*6, 1.6, W) for k in range(6))
a += ln("M4 96 C10 86 20 106 26 94 C30 86 40 104 46 92", G, 1.4) + circ(170, 32, 8, O, w=1.6) + ln("M170 24 V40 M162 32 H178", O, 1)
add("fx_phone", "Effects", "Phone", (190, 108, a), [("TONE", "45", B), ("PHONIC", "45", G), ("BAUD", "45", W), ("TELEMATIC", "45", O)])
a = ln("M60 30 Q60 10 80 10 Q100 10 100 30 Q100 46 80 48 Q60 46 60 30 Z", G, 1.6) + ln("M70 26 H90 M72 36 Q80 40 88 36", G, 1.2)
a += ln("M40 96 Q50 60 80 56 Q110 60 120 96", G, 1.6) + ln("M30 70 Q14 66 18 52 Q24 40 40 46 Q50 52 44 66 Z", O, 1.6) + ln("M130 70 Q146 66 142 52 Q136 40 120 46 Q110 52 116 66 Z", B, 1.6)
a += ln("M150 20 V40 M156 16 V44 M162 22 V38", W, 1.2) + rect(146, 84, 20, 12, P, sw=1.2) + t(156, 94, "FX", P, 9, "middle")
add("fx_punch", "Effects", "Punch", (170, 104, a), [("FREQ", "45", P), ("ROUNDS", "45", G), ("PUNCH", "45", G), ("POWER", "45", O)])
coil = "M0 60 h14 " + " ".join(f"c-5 -{40-k*1.6:.0f} 17 -{40-k*1.6:.0f} 12 0" for k in range(14)) + " h30"
a = t(0, 70, "T", B, 64, w=200) + f'<g transform="translate(46 0)">{ln(coil, W, 1.6)}</g>' + ln("M284 20 V100", O, 1.6, 'stroke-dasharray="2 5"') + dot(284, 20, 3, O) + dot(284, 100, 3, O)
add("fx_spring", "Effects", "Spring", (290, 104, a), [("TONE", "20", B), ("TURNS", "34", G), ("DAMP", "80", W), ("SEND", "45", O)])

# ---------- LFOs ----------
def tri(x, y, s, c, label):
    return poly(f"{x},{y} {x+s},{y+s/2} {x},{y+s}", c, w=1.6) + num(x + 6, y + s/2 + 9, label, c, 24)
def box(x, y, s, c):
    return rect(x, y, s, s, c, sw=1.4)
a = box(0, 20, 52, "#3a3a80") + ln("M10 46 H34 M34 40 H42 V52 H34", W, 1.6) + ln("M52 46 H64", P) + tri(64, 20, 52, G, "34") + ln("M116 46 H130", P)
a += box(130, 20, 52, "#3a3a80") + swv(146, 38, B, 1.0) + ln("M182 46 H196", P) + circ(222, 46, 26, "#3a3a80") + dot(212, 46, 3, B) + dot(222, 34, 2.5, O) + dot(232, 46, 3, W) + dot(222, 58, 2.5, G)
add("lfo_element", "LFOs", "Element", (250, 92, a), [("SOURCE", "G-F", B), ("AMOUNT", "34", G), ("DEST", "FX", W), ("PARAM", "BLUE", O)])
a = poly("0,10 70,46 0,82", P, w=1.6) + num(8, 56, "34", P, 26) + ln("M70 46 H96 L102 34 H112 V58 H120 V34 H130 V58 H140 V46 H170", G, 1.6) + dot(100, 46, 3, G)
a += rect(180, 4, 40, 34, W, sw=1.6) + ln("M186 30 Q196 10 204 22 T214 26", G, 1.4) + ln("M170 46 H250", P) + rect(180, 58, 40, 34, P) + ln("M186 86 L214 64", O, 1.6) + dot(186, 86, 3, O)
a += dot(260, 40, 3, B) + dot(270, 32, 3, G) + dot(270, 48, 3, W) + dot(280, 40, 3, O)
add("lfo_random", "LFOs", "Random", (284, 96, a), [("AMOUNT", "34", B), ("SPEED", "45", G), ("DEST", "ALL", W), ("ENV", "+10", O)])
a = rect(0, 26, 52, 52, P) + ln("M26 52 L40 46", B, 1.6) + dot(26, 52, 3, B) + "".join(ln(f"M{26+20*math.cos(math.radians(k)):.0f} {52+20*math.sin(math.radians(k)):.0f} l{3*math.cos(math.radians(k)):.0f} {3*math.sin(math.radians(k)):.0f}", B, 1) for k in range(0, 360, 45))
a += ln("M52 52 H70 V20 H80 M70 52 V84 H80", P) + tri(80, 0, 44, G, "34") + tri(80, 62, 44, W, "34") + ln("M124 22 H140 V52 M124 84 H140 V52 H160", P)
a += rect(160, 30, 46, 46, P) + ln("M168 66 L198 40", O, 1.6) + dot(168, 66, 3, O)
add("lfo_tremolo", "LFOs", "Tremolo", (208, 106, a), [("SPEED", "1/8", B), ("PITCH", "34", G), ("VOLUME", "34", W), ("ENV", "+10", O)])
a = rect(0, 30, 44, 44, P) + ln("M22 40 V64", B, 1.6) + circ(22, 14, 12, P) + ln("M22 26 V30", P) + ln("M44 52 H60", P) + tri(60, 30, 44, G, "34") + ln("M104 52 H120", P)
a += rect(126, 34, 44, 40, P) + rect(122, 30, 44, 40, P) + swv(134, 44, B, 1.0) + ln("M170 52 H184", P) + circ(206, 52, 22, P) + dot(198, 52, 3, B) + dot(206, 42, 2.5, O) + dot(214, 52, 2.5, W) + dot(206, 62, 2.5, G)
add("lfo_value", "LFOs", "Value", (230, 80, a), [("SPEED", "1", B), ("AMOUNT", "34", G), ("DEST", "SYN", W), ("P.DEST", "BLUE", O)])
a = ""
for k, (c, lab) in enumerate([(B, "CC1"), (G, "CC2"), (W, "CC3"), (O, "CC4")]):
    x = k*62
    a += ln(f"M{x+2} 26 A26 26 0 0 1 {x+54} 26", P) + dot(x+12, 18, 2, G) + dot(x+28, 8, 2, W) + dot(x+44, 18, 2, O) + ln(f"M{x+8} 26 H{x+28}", c, 1.6) + dot(x+28, 26, 3, c)
    a += rect(x+4, 54, 48, 24, c) + t(x+28, 72, lab, c, 16, "middle", 300) + ln(f"M{x+28} 78 V92 H{124}", P, 1)
add("lfo_midi", "LFOs", "MIDI", (244, 96, a), [("CC1", "74", B), ("CC2", "71", G), ("CC3", "73", W), ("CC4", "72", O)], False)
a = ln("M24 20 L120 4 M24 68 L120 92", O, 1.6) + circ(24, 44, 24, P) + circ(24, 44, 12, B) + ln("M18 50 L30 38", W, 2) + circ(120, 48, 44, O) + circ(120, 48, 34, P) + t(120, 58, "FX", P, 26, "middle", 200)
add("lfo_crank", "LFOs", "Crank", (166, 96, a), [("SPEED", "CRANK", B), ("AMOUNT", "34", G), ("DEST", "FX", W)])
a = "".join(dot(50 + 40*math.cos(math.radians(k)), 46 + 40*math.sin(math.radians(k)), 3, c) for k, c in zip(range(0, 360, 45), [O, "#555", W, "#555", G, "#555", B, "#555"]))
a += t(50, 52, "♩◁", W, 16, "middle") + circ(150, 46, 16, P) + ln("M110 46 H186", O, 1.6) + circ(150, 46, 9, O) + circ(196, 46, 22, O)
add("lfo_bend", "LFOs", "Bend", (220, 92, a), [("DEST", "ENV", B), ("PARAM", "BLUE", G), ("AMOUNT", "95", W), ("BEND", "+", O)])

# ---------- Sequencers ----------
a = dot(6, 26, 2.5, B) + dot(14, 20, 2.5, B) + dot(20, 28, 2.5, B) + t(40, 34, "ENDLESS", B, 28, w=200) + rect(36, 44, 136, 32, B, fill=B) + t(40, 70, "FINGER", "#0A0A0B", 28, w=300)
a += t(40, 106, "PATTERN", B, 28, w=200) + t(40, 140, "TOMBOLA", B, 28, w=200)
add("seq_browser", "Sequencers", "SHIFT + SEQ · Sequencer list", (180, 146, a))
a = t(0, 28, "1/8", B, 26, w=200) + "".join(dot(4 + (k % 6)*7, 46 + (k//6)*7, 1.6, W if k in (1, 3, 8, 14, 16) else "#555") for k in range(18))
a += num(70, 104, "44", W, 110) + t(220, 30, "55%", G, 26, w=200) + rect(222, 44, 46, 20, O) + t(245, 59, "HOLD", O, 14, "middle")
add("seq_endless", "Sequencers", "Endless", (270, 108, a))
a = ln("M10 12 L18 6 L24 12 L16 18 Z", W, 1.2) + "".join(ln(f"M{40+k*12} 4 V112", "#3a3a80" if k % 4 else B, 1) for k in range(17)) + "".join(ln(f"M40 {4+k*12} H232", "#3a3a80", 1) for k in range(10))
a += ln("M40 4 V112", W, 1.6) + ln("M24 112 H36 M30 106 L36 112 L30 118", B, 1.4) + "".join(dot(40 + x*12, 4 + y*12, 3, G) for x, y in [(3, 5), (4, 5), (7, 5), (11, 3), (11, 7), (12, 7), (15, 5), (16, 6)])
a += "".join(dot(40 + x*12, 112, 3, B) for x in (0, 5, 10, 15)) + t(244, 30, "55%", G, 26, w=200) + rect(246, 44, 46, 20, O) + t(269, 59, "HOLD", O, 14, "middle")
add("seq_pattern", "Sequencers", "Pattern", (296, 120, a))
a = poly(hexp(70, 60, 56, 0), W, w=1.8) + "".join(dot(x, y, 3.2, W) for x, y in [(56, 36), (90, 64), (100, 82), (64, 92), (80, 30)])
add("seq_tombola", "Sequencers", "Tombola", (140, 120, a), [("SPEED", "↻3", B), ("GRAVITY", "G", G), ("OPEN", "0", W), ("MASS", "M", O)])
def player(x, c):
    return circ(x, 22, 12, c) + dot(x-4, 21, 1.5, c) + dot(x+4, 21, 1.5, c) + ln(f"M{x-12} 64 Q{x} 40 {x+12} 64 V84 H{x-12} Z M{x-12} 66 L{x-24} 46 M{x+12} 66 L{x+24} 46", c, 1.4) + ln(f"M{x-28} 96 H{x+28} L{x+22} 106 H{x-22} Z", c, 1.4)
a = player(24, B) + player(256, B) + rect(96, 6, 88, 28, "#3a3a80", sw=1) + ln("M118 6 V34 M140 6 V34 M162 6 V34 M96 20 H184", "#3a3a80", 1)
a += "".join(ln(f"M{x-4} {y-4} l8 8 M{x+4} {y-4} l-8 8", W, 1.2) for x, y in [(107, 13), (129, 13), (151, 27), (173, 13), (107, 27)]) + rect(144, 4, 14, 14, B, sw=1.6) + dot(140, 2, 2.5, G)
a += rect(114, 46, 52, 22, W) + t(140, 62, "JOIN", W, 13, "middle") + t(140, 96, "0300000", W, 22, "middle", 200) + t(108, 80, "-1", O, 10) + t(166, 80, "+1", G, 10)
add("seq_finger", "Sequencers", "Finger", (290, 110, a), [("CURSOR", "07", B), ("SWING", "50%", G), ("LENGTH", "16", W), ("HOLD", "ON", O)], False)

# ---------- Drum ----------
a = t(0, 26, "C2", W, 30, w=200) + t(44, 26, "♩+10", G, 24, w=200) + wave(100, 22, 150, 12, 2, "#1A8A6A", 1, 60, ((0.2, .5),)) + ln("M262 18 h22 a8 8 0 0 0 0 -14 h-16 M272 0 l-6 4 l6 4", O, 1.6)
a += wave(10, 120, 280, 96, 11, G, 1.4, 120, ((0.12, .8), (0.16, .9), (0.62, .7), (0.66, .95)))
a += dot(30, 100, 3, B) + circ(196, 56, 4, W, w=1.6) + dot(196, 56, 1.6, W) + ln("M10 120 H290", "#1A6A5A", 1)
add("dr_sampler", "Drum", "Drum sampler", (292, 124, a), [("PITCH", "+10", B), ("IN", "0.42", G), ("OUT", "1.10", W), ("PLAY", "LOOP", O)], False)
def osc(x, y, n):
    s = rect(x, y, 140, 58, "#33449a", rx=4) + t(x+6, y+14, n, W if n == "1" else "#555", 12) + dial(x+28, y+34, 10, -30, B, True) + t(x+30, y+12, "+10 ♩", B, 8)
    s += "".join(ln(f"M{x+58} {y+12+k*7} H{x+66} M{x+70} {y+12+k*7} H{x+76}", "#888", 1) for k in range(6)) + rect(x+60, y+46, 14, 7, G, sw=1.2)
    s += t(x+86, y+12, "DECAY", "#666", 7) + t(x+114, y+12, "LONG", W, 7) + circ(x+108, y+32, 8, W) + ln(f"M{x+108} {y+24} V{y+32}", W) + t(x+86, y+54, "SHORT", W, 7) + t(x+112, y+54, "ATTACK", W, 7)
    return s
a = osc(0, 0, "1") + osc(0, 62, "2") + rect(146, 0, 126, 96, "#33449a", rx=4) + t(152, 12, "MODE", W, 8) + t(266, 12, "FILTER", W, 8, "end")
a += circ(209, 50, 22, W, w=1.6) + ln("M209 50 V32", O, 1.8) + "".join(rect(209 + 38*math.cos(math.radians(150 + k*40)) - 6, 50 + 38*math.sin(math.radians(150 + k*40)) - 6, 12, 12, O, sw=1.2) + t(209 + 38*math.cos(math.radians(150 + k*40)), 54 + 38*math.sin(math.radians(150 + k*40)), str(k+1), O, 9, "middle") for k in range(7))
a += rect(146, 100, 66, 20, "#33449a", rx=3) + ln("M150 110 H168 L172 102 L178 118 L182 110 H208", G, 1.4) + "".join(rect(218 + (k % 6)*9, 102 + (k//6)*6, 7, 4, O, sw=.8) for k in range(18))
add("dr_dbox", "Drum", "DBox", (274, 122, a), [("PITCH", "+10", B), ("WAVE", "SQR", G), ("ENVELOPE", "34", W), ("X-MOD", "45", O)], False)
a = ln("M10 40 H290", "#1A5A5A", 1.2, 'stroke-dasharray="6 4"') + ln("M10 40 Q60 70 110 80 V40 H210 V8 Q230 40 290 40", G, 1.8) + dot(10, 40, 3.5, G) + dot(110, 80, 3.5, G) + dot(110, 40, 3.5, G) + dot(210, 40, 3.5, G) + dot(210, 8, 3.5, G) + dot(290, 40, 3.5, G)
add("dr_dynenv", "Drum", "T2 · Dynamic envelope", (300, 86, a), [("ATTACK", "34", B), ("MID", "45", G), ("RELEASE", "12", W), ("REGION", "23", O)], False)

# ---------- Tape ----------
def reel(x, y, r):
    return circ(x, y, r, W, w=1.6) + circ(x, y, r*0.28, W) + circ(x, y, 3, W) + "".join(ln(f"M{x + r*0.3*math.cos(math.radians(k)):.1f} {y + r*0.3*math.sin(math.radians(k)):.1f} L{x + r*0.85*math.cos(math.radians(k)):.1f} {y + r*0.85*math.sin(math.radians(k)):.1f}", W, 1.4) for k in (-90, 30, 150))
a = rect(0, 4, 24, 24, W) + t(12, 23, "4", W, 18, "middle", 200) + reel(80, 52, 40) + reel(210, 52, 40) + t(145, 22, "2:50:20", W, 22, "middle", 200) + ln("M132 36 h22 a6 6 0 0 0 0 -12 M140 30 l-6 6 l6 6", W, 1.2)
a += ln("M48 76 L100 104 H190 L242 76", GR, 1.2) + circ(100, 104, 4, W) + circ(118, 100, 4, W) + rect(140, 96, 12, 10, W) + circ(170, 100, 4, W) + circ(190, 104, 4, W)
a += ln("M10 118 H60 M70 118 H120", O, 2) + ln("M100 122 H180", B, 2) + ln("M150 118 H210", G, 2) + ln("M220 122 H260", O, 2) + ln("M146 110 V128", G, 1.4) + ln("M286 30 V110", O, 1.6) + dot(286, 60, 3, O)
add("tp_tape", "Tape", "Tape", (292, 130, a), [("SCRUB", "", B), ("LOOP", "OUT", G), ("SPEED", "1.0", W), ("LEVEL", "80", O)], False)
a = reel(14, 14, 12).replace(W, O) + reel(44, 14, 12).replace(W, O) + t(66, 26, "ERASE TAPE?", W, 30, w=200) + "".join(rect(40 + k*36, 46, 30, 30, GR) + t(55 + k*36, 70, str(k+1), GR, 22, "middle", 200) for k in range(4))
a += t(110, 96, "PRESS ALL TRACK KEYS 1–4 TO", W, 10, "middle") + t(110, 110, "START ERASING PROCESS", W, 10, "middle")
add("tp_erase", "Tape", "SHIFT + TAPE · Erase tape", (240, 114, a))

# ---------- Mixer ----------
a = ""
for k, (c, n) in enumerate([(B, "02"), (G, "34"), (W, "45"), (O, "23")]):
    x = 30 + k*72
    a += ln(f"M{x-26} 30 A26 26 0 0 1 {x+26} 30", DIM, 1.6) + ln(f"M{x} 30 V4", W, 1.6) + dot(x+16, 16, 2.5, O) + t(x, 26, str(k+1), DIM, 18, "middle", 200)
    a += circ(x, 50, 8, W) + ln(f"M{x} 50 V42", W) + t(x-18, 54, "L", GR, 10) + t(x+12, 54, "R", GR, 10) + num(x, 104, n, c, 46, "middle")
add("mx_mixer", "Mixer", "T1 · Mixer", (290, 108, a))
a = '<ellipse cx="20" cy="30" rx="16" ry="6" fill="none" stroke="#5B7CFA" stroke-width="1.6"/>' + ln("M4 30 V62 A16 6 0 0 0 36 62 V30", B, 1.6)
a += poly("74,18 90,8 106,18 106,62 90,72 74,62", G, w=1.6) + ln("M90 8 V72 M74 18 L90 28 L106 18", G, 1.2) + poly("150,6 166,64 134,64", W, w=1.6) + ln("M150 6 L150 64", W, 1)
a += t(20, 92, "LOW", B, 18, "middle", 200) + t(90, 92, "MID", G, 18, "middle", 200) + t(150, 92, "HIGH", W, 18, "middle", 200)
a += ln("M196 16 H218 M212 10 L218 16 L212 22", O, 1.4) + rect(224, 6, 62, 20, O) + t(255, 21, "MAX EQ", O, 13, "middle") + rect(224, 78, 62, 20, B) + t(255, 93, "CLEAN", B, 13, "middle")
add("mx_eq", "Mixer", "T2 · EQ", (290, 100, a), [("LOW", "45", B), ("MID", "34", G), ("HIGH", "23", W), ("AMOUNT", "60", O)], False)
add("mx_fx", "Mixer", "T3 · Master effect (Punch)", S[[s["id"] for s in S].index("fx_punch")]["art"], [("FREQ", "45", P), ("ROUNDS", "45", G), ("PUNCH", "45", G), ("POWER", "45", O)])
a = "".join(ln(f"M{x} {10+k*7} H{x+16}", "#3a3a5a", 1.2) for x in (0, 22, 48, 70) for k in range(14)) + ln("M0 24 H16 M22 10 H38", B, 1.6) + ln("M48 52 H64 M70 10 H86", G, 1.6) + ln("M0 104 H16 M48 104 H64", W, 1.6)
a += rect(0, 112, 18, 18, GR) + t(9, 126, "L", GR, 12, "middle") + rect(48, 112, 18, 18, GR) + t(57, 126, "R", GR, 12, "middle")
a += ln("M128 10 V104 M160 10 V104", GR, 1.2) + ln("M120 70 H136", B, 1.6) + ln("M152 50 H168", G, 1.6) + t(116, 74, "20", B, 18, "end", 200) + t(172, 54, "45", G, 18, "start", 200)
a += rect(118, 112, 18, 18, B) + t(127, 126, "L", B, 12, "middle") + rect(150, 112, 18, 18, G) + t(159, 126, "R", G, 12, "middle")
a += t(206, 16, "DRIVE", "#9A9AAA", 18, w=200) + num(206, 62, "76", W, 44) + t(206, 82, "RELEASE", O, 18, w=200) + num(206, 126, "30", O, 44)
add("mx_out", "Mixer", "T4 · Master out", (270, 132, a))
a = rect(46, 2, 30, 20, W) + t(61, 17, "LFO", W, 11, "middle") + ln("M61 22 V36 M34 26 V36", W) + swv(6, 34, B, 1.2) + rect(46, 32, 30, 20, W) + t(61, 47, "FX", W, 12, "middle")
a += ln("M76 42 H96 M92 38 L96 42 L92 46", W) + rect(100, 32, 18, 20, W) + t(109, 47, "1", W, 12, "middle") + t(130, 48, "⚠", W, 14)
a += "".join(ln(f"M{168+k*24} 2 V18 M{164+k*24} 14 L{168+k*24} 18 L{172+k*24} 14", W) + circ(168 + k*24, 30, 6, W) for k in range(4)) + t(262, 34, "⚠", W, 14)
a += reel(110, 82, 10) + reel(136, 82, 10) + ln("M152 74 V92 M156 82 H176", W) + rect(176, 72, 30, 20, W) + t(191, 87, "EQ", W, 12, "middle") + t(212, 88, "⚠", W, 14)
a += ln("M191 46 V72 M168 36 V46 H240 V36", W) + rect(176, 104, 30, 20, W) + t(191, 119, "FX", W, 12, "middle") + rect(206, 104, 44, 20, W) + t(228, 119, "DRIVE", W, 10, "middle")
a += ln("M191 92 V104 M250 114 H270 V60 H286", W) + poly("286,52 300,40 300,92 286,80", W) + t(212, 140, "⚠", W, 14) + rect(46, 98, 30, 20, W) + "".join(dot(52 + k*8, 110, 2, W) for k in range(3)) + ln("M80 108 H100 M96 104 L100 108 L96 112", W)
add("mx_path", "Mixer", "SHIFT + MIXER · Sound path", (302, 142, a))

# ---------- Utility ----------
a = rect(0, 0, 112, 36, "#33449a") + metro(10, 8, B) + t(32, 28, "BPM", B, 24, w=200) + num(10, 92, "120", B, 64) + rect(0, 36, 112, 64, "#33449a") + rect(0, 100, 112, 34, "#33449a") + t(10, 126, "2 BPS", W, 24, w=200)
a += ln("M112 18 H136", G) + t(140, 24, "LINK", G, 14, w=600) + ln("M178 18 H196", G) + t(150, 92, "TAP", W, 24, "middle", 200) + rect(122, 100, 56, 34, G) + t(150, 115, "BEAT", G, 12, "middle", 600) + t(150, 130, "MATCH", G, 12, "middle", 600)
a += rect(196, 0, 112, 36, "#33449a") + t(202, 28, "T.SPEED", W, 24, w=200) + rect(196, 36, 112, 64, "#33449a") + ln("M240 46 V90 M262 46 V90", W, 1.6) + dot(251, 62, 1.6, W) + dot(251, 74, 1.6, W)
a += rect(196, 100, 112, 34, "#33449a") + t(202, 126, "19 cm/s  7.5 ips", W, 15, w=200) + metro(314, 4, O) + ln("M322 30 V132", O, 1.6)
add("ut_tempo", "Utility", "Tempo", (334, 136, a), [("TEMPO", "120", B), ("MODE", "BEAT", G), ("SWING", "0", W), ("METRONOME", "C4", O)], False)
a = t(110, 20, "INPUT", W, 26, "middle", 200) + rect(0, 60, 40, 12, "#666", rx=2) + ln("M40 66 H58", "#666") + rect(84, 52, 34, 24, B, rx=3) + "".join(dot(94 + (k % 3)*5, 60 + (k//3)*6, 1.4, B) for k in range(6)) + ln("M118 50 Q126 64 118 78", B)
a += t(100, 98, "98.8", G, 20, "middle", 200) + ln("M160 52 Q176 44 180 62 Q182 76 168 86", "#666", 1.6) + t(240, 26, "+23", O, 22, "middle", 200) + ln("M240 34 V106", O, 1.6) + ln("M232 70 H248", W, 1.6) + dot(240, 70, 3, W) + t(240, 128, "TRIG", W, 18, "middle", 200)
add("ut_input", "Utility", "MIC/INPUT", (270, 132, a), [("SOURCE", "RADIO", B), ("TUNE", "98.8", G), ("THRESHOLD", "12", W), ("GAIN", "+23", O)], False)
a = rect(0, 30, 78, 32, O, sw=1.6) + rect(4, 34, 12, 11, O) + t(10, 43, "A", O, 9, "middle") + rect(4, 48, 12, 11, "#666") + t(10, 57, "B", "#666", 9, "middle") + num(22, 58, "0:20", O, 30) + ln("M78 46 H96", O) + dot(96, 46, 3, O)
a += rect(100, 2, 116, 98, P, sw=1.4) + circ(152, 50, 42, W) + circ(152, 50, 14, P) + t(152, 56, "A", P, 16, "middle") + ln("M200 10 V64 L182 82", G, 1.6) + circ(200, 14, 6, G)
a += t(242, 14, "SIDE", W, 12, "middle") + rect(230, 20, 24, 26, W) + t(242, 40, "A", W, 18, "middle", 200) + rect(230, 52, 24, 26, "#555") + t(242, 72, "B", "#555", 18, "middle", 200)
a += t(0, 124, "RECORD", O, 18, w=200) + t(88, 124, "PLAY", "#3a5aa0", 18, w=200) + t(150, 124, "STOP", "#3a5aa0", 18, w=200) + t(210, 124, "SIDE", "#3a5aa0", 18, w=200)
add("ut_album", "Utility", "ALBUM", (262, 130, a))
a = rect(0, 30, 110, 40, P, rx=4) + "".join(rect(6 + k*10, 36, 8, 8, P, sw=.8) for k in range(10)) + "".join(rect(6 + k*7, 50, 5, 16, P, sw=.8) for k in range(14)) + ln("M110 50 H126 V70 H140", P)
a += rect(140, 20, 60, 40, P, rx=3) + rect(134, 62, 72, 18, P, rx=3) + t(55, 92, "DISK MODE", P, 14, "middle")
a += "".join(rect(k*56, 104, 50, 26, P) + t(25 + k*56, 123, s, P if k != 2 else W, 18, "middle", 200) for k, s in enumerate(["OP-1", "CTRL", "DISK", "OPT"]))
add("ut_com", "Utility", "SHIFT + ALBUM · COM", (222, 132, a))
a = t(0, 60, "OCT 2026", B, 40, w=200) + t(200, 60, "12", G, 40, w=200) + t(0, 120, "14", W, 40, w=200) + t(54, 116, ":", "#666", 36, w=200) + t(70, 120, "05", O, 40, w=200)
add("ut_tools", "Utility", "SHIFT + HELP · Tools", (260, 126, a), [("MONTH/YEAR", "OCT", B), ("DAY", "12", G), ("HOUR", "14", W), ("MINUTE", "05", O)], False)
a = ln("M10 10 H250 Q262 10 262 22 V70 Q262 82 250 82 H70 L50 100 L54 82 H10 Q0 82 0 70 V22 Q0 10 10 10 Z", W, 1.6) + t(130, 42, "SYNTH MODE", W, 20, "middle", 200) + t(130, 68, "SOUND 3 · DR WAVE", B, 14, "middle")
add("ut_help", "Utility", "HELP", (264, 102, a))
a = t(0, 18, "ENGINE", "#888", 11, w=600) + "".join(t(0, 44 + k*22, n, B, 18, w=200) for k, n in enumerate(["FM", "CLUSTER", "DR WAVE"])) + rect(-4, 94, 110, 22, B, fill=B) + t(0, 111, "DIGITAL", "#0A0A0B", 18, w=300)
a += "".join(t(0, 136 + k*22, n, B, 18, w=200) for k, n in enumerate(["STRING", "PULSE"]))
add("ut_engines", "Utility", "SHIFT + T1 · Engine browser", (120, 166, a))
a = t(0, 18, "ENGINE", "#888", 11, w=600) + t(130, 18, "PRESET", "#888", 11, w=600) + "".join(t(0, 44 + k*22, n, B, 18, w=200) for k, n in enumerate(["CLUSTER", "DIGITAL", "DR WAVE", "FM", "STRING"]))
a += rect(-4, 72, 104, 22, B) + "".join(t(130, 44 + k*22, n, G, 18, w=200) for k, n in enumerate(["ALPS", "BELLTONE", "CHIME", "DEEP"])) + rect(126, 50, 120, 22, G, fill=G) + t(130, 67, "BELLTONE", "#0A0A0B", 18, w=300)
add("ut_presets", "Utility", "SHIFT + 1–8 · Sound presets", (250, 146, a))

GROUPS = ["Synth engines", "Synth pages", "Effects", "LFOs", "Sequencers", "Drum", "Tape", "Mixer", "Utility"]

def fit(box, aw, ah, x0, y0):
    s = min(box[0]/aw, box[1]/ah)
    return f'<g transform="translate({x0 + (box[0]-aw*s)/2:.1f} {y0 + (box[1]-ah*s)/2:.1f}) scale({s:.3f})">'

def wide(sc):
    aw, ah, art = sc["art"]; ro = sc["ro"] if sc["wide_ro"] else []
    out = ""
    if ro:
        out += fit((176, 140), aw, ah, 72, 10) + art + "</g>"
        pos = [(8, 16, "start"), (312, 16, "end"), (8, 96, "start"), (312, 96, "end")]
        for (lab, val, c), (x, y, an) in zip(ro, pos):
            out += t(x, y, lab, c, 9, an, 500) + num(x, y + 34, val, c, 32, an)
    else:
        out += fit((304, 144), aw, ah, 8, 8) + art + "</g>"
    return f'<svg viewBox="0 0 320 160" xmlns="http://www.w3.org/2000/svg" font-family="{FONT}" style="display:block;width:100%;height:100%;background:#000">{out}</svg>'

def tall(sc, header=True):
    # phone screen: the four readouts sit in the corners (as on the OP-1), the title at the top centre,
    # and the drawing fills the middle
    aw, ah, art = sc["art"]; ro = sc["ro"]
    out = t(160, 16, sc["title"].upper().split(" (")[0], "#6A6A6A", 9, "middle", ls=1.2) if header else ""
    if ro:
        out += fit((296, 196), aw, ah, 12, 72) + art + "</g>"
        pos = [(14, 22, "start"), (306, 22, "end"), (14, 290, "start"), (306, 290, "end")]
        for (lab, val, c), (x, y, an) in zip(ro, pos):
            out += t(x, y, lab, c, 11, an, 500) + num(x, y + 36, val, c, 36, an)
    else:
        out += fit((296, 296), aw, ah, 12, 30) + art + "</g>"
    return f'<svg viewBox="0 0 320 338" xmlns="http://www.w3.org/2000/svg" font-family="{FONT}" style="display:block;width:100%;height:100%;background:#000">{out}</svg>'
