"""One-stroke numerals (a 8 x 14 box), so every number is drawn with the same line weight as the illustrations."""
import re, json
GLY = {
 '0':("M1 4Q1 0 4 0Q7 0 7 4V10Q7 14 4 14Q1 14 1 10Z", 11),
 '1':("M1.5 3L4.5 0V14", 8),
 '2':("M1 3.5Q1 0 4 0Q7 0 7 3.5Q7 6 4 8.5L1 14H7.5", 11),
 '3':("M1 1.2Q4 -0.6 6.4 1.4Q7.4 4.2 4 6.6Q8 8.2 7 11Q5.6 14.6 1 13", 11),
 '4':("M5.5 14V0L0.5 10H8", 11),
 '5':("M7 0H1.8L1.2 6.4Q6 4.4 7.3 8.6Q8 13 3.6 14Q1.6 14 1 12.6", 11),
 '6':("M6.4 1Q1 -1 1 7V10Q1 14 4 14Q7 14 7 10Q7 7 4 7Q1 7 1 9", 11),
 '7':("M0.5 0H7.5L3 14", 11),
 '8':("M4 7Q1 6 1 3.5Q1 0 4 0Q7 0 7 3.5Q7 6 4 7Q0.7 8 0.8 10.5Q1 14 4 14Q7 14 7.2 10.5Q7.3 8 4 7", 11),
 '9':("M1.6 13Q7 15 7 7V4Q7 0 4 0Q1 0 1 4Q1 7 4 7Q7 7 7 5", 11),
 '.':("M1 13.2V13.6", 4), ':':("M1 3.2V3.6M1 10.4V10.8", 4), '%':("M2 0Q0.6 0 0.6 1.6T2 3.2T3.4 1.6T2 0ZM8 10.8Q6.6 10.8 6.6 12.4T8 14T9.4 12.4T8 10.8ZM9 0L1 14", 12),
 '-':("M0.5 8H6.5", 8), '+':("M0.5 8H7.5M4 4.5V11.5", 9), '/':("M5 0L0.5 14", 7), ' ':("", 5),
}
H = 14.0
def ok(s): return bool(s) and all(c in GLY for c in str(s))
def width(s): return sum(GLY[c][1] for c in s) - 3
def paths(s):
    """list of (translate_x, path) for a string"""
    x = 0; out = []
    for c in s:
        d, adv = GLY[c]
        if d: out.append((x, d))
        x += adv
    return out
def svg(x, y, s, col, sz, anchor, lw=1.4):
    k = sz * 0.7 / H; w = width(s) * k
    x0 = x - (w if anchor == 'end' else w / 2 if anchor == 'middle' else 0)
    g = ''.join(f'<path transform="translate({x0 + tx * k:.2f} {y - sz * 0.7:.2f}) scale({k:.4f})" d="{d}" fill="none" stroke="{col}" stroke-width="{lw / k:.3f}" stroke-linecap="round" stroke-linejoin="round"/>' for tx, d in paths(s))
    return g
if __name__ == '__main__': print(json.dumps({c:[d,a] for c,(d,a) in GLY.items()}, separators=(',',':')))
