"""Round 13: the original OP-1's screens (Operator's Manual v1, reference pages 41-45 and chapters 5-9).
Keeps the round 5 drawings, which already follow the original manual, and redraws the screens Ryan flagged
(punch, nitro, phone, spring, CWO, finger, master effect) in the original's neon line style.
The radio input screen is removed."""
import math, os, sys, re
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import screens as base
from screens import t, num, ln, circ, dot, rect, poly, B, G, W, O, P, PK, CY, GR, DIM

def art(i, a, ro=None, title=None):
    sc = next(s for s in base.S if s["id"] == i)
    sc["art"] = a
    if ro is not None: sc["ro"] = ro
    if title: sc["title"] = title
    sc["wide_ro"] = True

# ---- Punch: a neon boxer, pink gloves, purple pointers from FREQ and PUNCH (manual p.45) ----
boxer = (ln("M74 20 Q74 8 86 8 Q98 8 98 20 L97 32 Q94 40 86 40 Q78 40 75 32 Z", G, 1.4)           # head
         + ln("M78 20 L84 22 M90 22 L96 20 M80 27 H84 M90 27 H94 M82 34 Q86 36 90 34 M86 24 V30", G, 1)   # face
         + ln("M66 48 Q86 40 104 48 M66 48 Q54 54 50 70 Q48 80 58 84 M104 48 Q116 54 116 66", G, 1.4)  # shoulders, arms
         + ln("M64 60 Q78 66 92 58 M70 70 Q80 74 90 70 M60 84 L64 96", G, 1.2)                          # chest
         + ln("M66 96 L60 112 M80 96 L88 112 M60 112 H66 M86 112 H94", B, 1.4))                          # legs
gloves = (ln("M58 84 Q46 86 48 98 Q52 110 66 106 Q78 102 76 90 Q72 80 58 84 Z M54 88 Q50 84 56 80", PK, 1.6)
          + ln("M112 64 Q104 58 104 70 Q104 84 116 84 Q128 84 128 72 Q128 60 116 60 Q112 60 112 64 Z M118 60 Q122 54 126 60", PK, 1.6)
          + ln("M114 70 l4 4 m0 -4 l-4 4", W, 1.2))
a = boxer + gloves + ln("M0 26 L76 40", P, 1.2) + dot(76, 40, 2.5, P) + ln("M0 104 H30 L62 94", P, 1.2) + dot(62, 94, 2.5, P)
a += ln("M66 0 L70 6 M84 -6 V2 M102 0 L98 6", P, 1.2) + "".join(ln(f"M136 {10 + k*7} H148", G, 1.2) for k in range(9))
a += rect(134, 100, 22, 13, P, sw=1.2) + t(145, 110, "FX", P, 10, "middle")
PUNCH = (156, 120, a)
art("fx_punch", PUNCH, [("FREQ", "45", P), ("PUNCH", "45", G), ("ROUNDS", "45", G), ("POWER", "45", PK)])
art("mx_fx", PUNCH, [("FREQ", "45", P), ("PUNCH", "45", G), ("ROUNDS", "45", G), ("POWER", "45", PK)])

# ---- Nitro: the driver's view, windshield, skyline, the road, gear stick R and the dash (manual p.44) ----
a = ln("M0 6 Q150 18 300 6", B, 2)
a += "".join(ln(f"M{118 + k*6} 30 V{30 - h}", B, 1.4) for k, h in enumerate([4, 8, 6, 14, 10, 18, 12, 7, 16, 9, 5, 11]))
a += ln("M120 30 H192", B, 1)
for k in range(10):
    y = 38 + k * 5.5; hw = 30 + k * 13
    a += ln(f"M{150 - hw} {y:.1f} H{150 + hw}", G, 1.2, 'stroke-dasharray="5 3"')
a += circ(150, 70, 9, W, "#0A0A0A", 1.6) + t(150, 74.5, "R", W, 11, "middle", 600) + ln("M150 79 V96 M140 106 Q150 92 160 106 Z", W, 1.4)
a += ln("M0 96 H96 Q104 96 108 104 M192 104 Q196 96 204 96 H300 L296 110", B, 1.4)
a += ln("M14 84 H34 M24 76 V92", G, 1.2) + t(40, 108, "4  5  6  7", W, 8) + "".join(ln(f"M{6 + k*8} 104 H{11 + k*8}", [PK, G, W, B, W, PK][k % 6], 2) for k in range(7))
a += ln("M224 104 H244 M228 100 H240 M228 108 H240", W, 1) + circ(276, 104, 4, B) + dot(276, 104, 1.4, B)
art("fx_nitro", (300, 112, a), [("FREQ", "45", B), ("FF", "45", G), ("RES", "45", W), ("FREQ", "45", PK)])

# ---- Phone: a telephone taken apart, its parts joined by purple guides (manual p.44) ----
a = poly("60,54 120,30 170,52 110,78", W, "none", 1.4) + poly("60,54 60,62 110,86 110,78", W, "none", 1.2) + poly("110,86 170,60 170,52 110,78", W, "none", 1.2)
a += poly("96,40 112,34 130,42 114,48", W, "none", 1.1) + ln("M100 48 L110 52 L120 48", W, 1)
a += poly("128,58 146,50 156,56 138,64", G, "none", 1.1) + "".join(dot(134 + k*4, 58 - k*1.6, 1.1, G) for k in range(5))
a += ln("M36 10 L60 24 Q66 28 62 34 L58 38 Q54 40 50 36 L28 20 Z", W, 1.3) + ln("M42 14 L36 22", W, 1)          # handset tube
a += ln("M10 34 V44 M6 44 H14 V52 H6 Z", B, 1.2) + ln("M14 48 H40", P, 1)                                    # mouthpiece
a += "".join(f'<ellipse cx="{24 + k*5}" cy="72" rx="3" ry="6" fill="none" stroke="{W}" stroke-width="1"/>' for k in range(6))   # coil spring
a += circ(78, 98, 12, G, "none", 1.4) + circ(78, 98, 7, G) + "".join(dot(78 + 9*math.cos(k), 98 + 9*math.sin(k), 1.3, G) for k in range(0, 6))
a += circ(200, 26, 9, PK, "none", 1.4) + circ(200, 26, 4, PK) + "".join(dot(196 + k*3, 8 + (k % 2)*3, 1.2, B) for k in range(4))
a += poly("174,74 192,66 202,72 184,80", W, "none", 1.1) + rect(186, 88, 10, 8, W, sw=1) + ln("M60 54 L40 40 M110 86 L84 98 M170 52 L192 34 M150 62 L182 70 M140 80 L188 90", P, 0.9)
a += circ(100, 102, 4, W) + circ(120, 104, 3, W) + ln("M100 106 V112 M120 107 V112", W, 1)
art("fx_phone", (214, 114, a), [("TONE", "45", B), ("PHONIC", "45", G), ("BAUD", "45", W), ("TELEMATIC", "45", PK)])

# ---- Spring: T, then an even coil, TURNS above, DAMP below, the dotted send bar (manual p.45) ----
coil = "M0 60 H18"
for k in range(14): coil += " c-4 -26 14 -26 10 0"
coil += " H186"
a = t(0, 70, "T", B, 40, "start", 200) + f'<g transform="translate(40 0)">{ln(coil, W, 1.4)}</g>' + t(140, 14, "TURNS", G, 16, "middle", 400) + t(140, 98, "DAMP", W, 16, "middle", 400)
a += ln("M262 36 V84", PK, 1.6, 'stroke-dasharray="2 4"') + dot(262, 36, 3, PK) + dot(262, 84, 3, PK)
art("fx_spring", (266, 104, a), [])

# ---- CWO: a neon cow with its workings showing; frequency, delay, feedback, sideband ----
cow = ("M50 34 Q46 24 38 26 L30 20 L32 28 Q20 32 16 42 L12 50 Q10 58 18 60 L26 58 Q32 54 36 50 L48 54 "
       "Q58 32 92 30 L172 26 Q200 24 208 40 Q216 34 220 44 L216 76 Q216 92 208 100 L204 128 L194 128 L194 102 "
       "Q162 108 122 104 L112 128 L102 128 L100 102 Q76 98 68 84 L64 128 L54 128 L54 80 Q50 66 50 54 Z")
a = ln(cow, CY, 1.5) + ln("M28 34 Q34 30 40 32", W, 1.2) + dot(26, 40, 1.8, W) + ln("M216 44 Q228 50 226 66", CY, 1.2)
a += ln("M58 50 Q74 46 90 54 L104 60", B, 1.2, 'stroke-dasharray="3 2"') + ln("M100 56 L106 60 L100 64", B, 1.2)
a += circ(118, 56, 9, G, "none", 1.4) + ln("M113 56 H123", W, 1.6) + circ(120, 82, 9, B, "none", 1.4) + dot(116, 80, 2, G) + dot(124, 80, 2, PK) + dot(120, 86, 2, W)
a += circ(152, 68, 20, P, "none", 1.4) + "".join(ln(f"M{142 + k*5} {60 + (k % 2)*4} V{76 - (k % 3)*3}", [W, G, PK][k % 3], 1.4) for k in range(5))
a += circ(190, 70, 9, O, "none", 1.2) + "".join(ln(f"M183 {66 + k*3} H197", O, 0.9) for k in range(3))
a += ln("M172 52 H180 V42 H186 V52 H192 V42 H198 V52 H204 V42 H210", PK, 1.6)
a += "".join(ln(f"M{4 + k*11} 134 V{130 - (k*7) % 6}", G, 1) for k in range(21))
art("fx_cwo", (230, 136, a), [("FREQ", "45", B), ("DELAY", "45", G), ("FEEDBACK", "45", W), ("SIDEBAND", "45", PK)], "CWO")

# ---- Finger: two players with headphones, JOIN, the pattern rows and the step keys (manual p.17) ----
def player(x, c):
    s = ln(f"M{x-14} 30 Q{x-14} 14 {x} 14 Q{x+14} 14 {x+14} 30 Q{x+14} 44 {x} 44 Q{x-14} 44 {x-14} 30 Z", PK, 1.4)
    s += ln(f"M{x-17} 30 Q{x-17} 8 {x} 8 Q{x+17} 8 {x+17} 30", B, 1.6) + rect(x - 20, 24, 6, 12, B, sw=1.4) + rect(x + 14, 24, 6, 12, B, sw=1.4)
    s += ln(f"M{x-8} 28 L{x-3} 30 M{x+3} 30 L{x+8} 28 M{x-4} 37 Q{x} 40 {x+4} 37", PK, 1.2)
    s += ln(f"M{x-22} 74 Q{x-18} 52 {x} 50 Q{x+18} 52 {x+22} 74 Z", c, 1.4) + ln(f"M{x-10} 58 V74 M{x+10} 58 V74", c, 1)
    s += ln(f"M{x-30} 56 L{x-36} 44 M{x-40} 46 L{x-34} 40 M{x+30} 56 L{x+36} 44 M{x+40} 46 L{x+34} 40", PK, 1.4)
    return s
a = player(34, PK) + player(246, PK)
a += "".join((ln(f"M{102 + (k % 9)*9} {4 + (k // 9)*8} l5 5 m0 -5 l-5 5", W, 1) if k in (1, 4, 10, 15, 21, 24) else dot(104.5 + (k % 9)*9, 6.5 + (k // 9)*8, 1.6, B)) for k in range(27))
a += ln("M130 32 H150 V42 H160 V60 H150 V70 H130 V60 H120 V42 H130 Z", PK, 1.6) + t(140, 55, "JOIN", W, 9, "middle", 600)
a += rect(110, 80, 60, 22, W, sw=1.1) + "".join(rect(114 + k*7.6, 84, 5.5, 14, W, "#C9C5BE" if k > 3 else "none", 0.7) for k in range(7))
a += t(112, 78, "-1", PK, 8) + t(160, 78, "+1", G, 8) + t(140, 114, "0000000", W, 12, "middle", 200)
a += rect(10, 92, 50, 12, B, sw=1.2) + t(35, 101, "A", B, 9, "middle") + rect(220, 92, 50, 12, B, sw=1.2) + t(245, 101, "B", B, 9, "middle")
a += rect(232, 0, 32, 12, None, PK) + t(248, 9, "HOLD", "#fff", 8, "middle", 600)
art("seq_finger", (280, 116, a), [("CURSOR", "07", B), ("SWING", "50%", G), ("LENGTH", "16", W), ("HOLD", "ON", PK)])

# the radio input screen goes; the effect-off screen shows the effect faded behind FX OFF (manual p.12)
base.S[:] = [s for s in base.S if s["id"] != "ut_input"]
off = next(s for s in base.S if s["id"] == "pg_fxoff")
off["art"] = (300, 110, f'<g opacity="0.22">{next(s for s in base.S if s["id"] == "fx_phone")["art"][2]}</g>'
              + rect(98, 46, 40, 24, B, sw=1.6) + t(118, 64, "FX", B, 17, "middle") + num(146, 70, "OFF", W, 38))
off["art"] = (214, 114, f'<g opacity="0.22">{next(s for s in base.S if s["id"] == "fx_phone")["art"][2]}</g>'
              + rect(52, 44, 40, 24, B, "#000", 1.6) + t(72, 62, "FX", B, 17, "middle") + num(100, 70, "OFF", W, 38))
off["ro"] = [("TONE", "45", "#3a5aa0"), ("PHONIC", "45", "#2a6a4a"), ("BAUD", "45", "#555"), ("TELEMATIC", "45", "#6a2a35")]; off["wide_ro"] = True

if __name__ == "__main__":
    dst = sys.argv[1]
    for sub in ("phone", "ipad"):
        os.makedirs(os.path.join(dst, sub), exist_ok=True)
        for f in os.listdir(os.path.join(dst, sub)):
            if f.endswith(".svg"): os.remove(os.path.join(dst, sub, f))
    for sc in base.S:
        name = re.sub(r"[^a-z0-9]+", "-", (sc["group"] + " " + sc["title"].split(" (")[0]).lower()).strip("-")
        for sub, fn, w, h in (("phone", base.tall, 320, 338), ("ipad", base.wide, 320, 160)):
            svg = fn(sc).replace(' style="display:block;width:100%;height:100%;background:#000"', f' width="{w*2}" height="{h*2}"')
            svg = svg.replace('>', f'><rect width="{w}" height="{h}" fill="#000"/>', 1)
            open(os.path.join(dst, sub, name + ".svg"), "w").write(svg)
    print(len(base.S), "screens")
