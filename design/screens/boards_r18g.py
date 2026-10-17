# Round 14: rebuild the five screen galleries from the original-style screens (screens_r13), and add two board states
# for the new mixer pages. Usage: boards_r14.py <project dir>
import os, sys, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import screens as SC
import screens_r18 as R
P = sys.argv[1]
HEAD = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>{title}</title>
<script src="./support.js"></script>
</head>
<body>
<x-dc>
<helmet>
<link href="https://fonts.googleapis.com/css2?family=Encode+Sans+Condensed:wght@200;300;400;500;600&amp;display=swap" rel="stylesheet">
<style>
{css}
</style>
</helmet>
"""
TAIL = """
</x-dc>
<script type="text/x-dc" data-dc-script data-props='{{"$preview":{{"width":{w},"height":{h}}}}}'>
class Component extends DCLogic {{
renderVals() {{
return {{}};
}}
}}
</script>
</body>
</html>
"""
GCSS = """body{margin:0}
.cell{display:flex;gap:16px;align-items:flex-start}
.cap{font:500 13px/1.4 'Encode Sans Condensed',sans-serif;color:#2A2A2A;letter-spacing:.04em}
.sub{font:400 12px/1.4 'Encode Sans Condensed',sans-serif;color:#6A6A6A}
.frame{border-radius:10px;overflow:hidden;background:#000;box-shadow:0 2px 6px rgba(0,0,0,.18)}"""
GAL = [("GalEngines", "OP-1 screens · Synth engines", ["Synth engines"]),
       ("GalPagesFx", "OP-1 screens · Envelope, play mode and effects", ["Synth pages", "Effects"]),
       ("GalLfo", "OP-1 screens · LFOs", ["LFOs"]),
       ("GalSeqDrum", "OP-1 screens · Sequencers and drum", ["Sequencers", "Drum"]),
       ("GalTapeMix", "OP-1 screens · Tape, mixer and utility", ["Tape", "Mixer", "Utility"])]
SIZE = 'style="display:block;width:100%;height:100%;background:#000"'
def fit(svg, w, h, title): return svg.replace(SIZE, f'width="{w}" height="{h}" role="img" aria-label="{title} screen" style="display:block;background:#000"')
sizes = {}
for fname, title, groups in GAL:
    items = [s for s in SC.S if s["group"] in groups]
    rows = (len(items) + 1) // 2; H = 120 + rows * 290
    cells = ""
    for s in items:
        cells += (f'<div class="cell"><div class="frame" style="width:200px;height:211px">{fit(R.tall(s), 200, 211, s["title"])}</div>'
                  f'<div style="display:flex;flex-direction:column;gap:8px"><div class="frame" style="width:420px;height:210px">{fit(R.wide(s), 420, 210, s["title"])}</div>'
                  f'<div class="cap">{s["title"].upper()}</div><div class="sub">Left: phone · Right: iPad / OP-1 2:1</div></div></div>')
    body = (f'<div style="width:1400px;height:{H}px;box-sizing:border-box;padding:40px;background:#F2F0EC;font-family:\'Encode Sans Condensed\',sans-serif">'
            f'<h1 style="margin:0 0 28px;font-size:30px;font-weight:300;color:#2A2A2A;letter-spacing:.02em">{title}</h1>'
            f'<div style="display:grid;grid-template-columns:repeat(2,minmax(0,1fr));column-gap:40px;row-gap:40px">{cells}</div></div>')
    open(f"{P}/{fname}.dc.html", "w").write(HEAD.format(title=title, css=GCSS) + body + TAIL.format(w=1400, h=H))
    sizes[fname] = (title, H)
c = json.load(open(f"{P}/canvas.json"))
for fname, (title, H) in sizes.items():
    b = c["boards"][fname + ".dc.html"]; b["h"] = H; b["title"] = title
json.dump(c, open(f"{P}/canvas.json", "w"), indent=1, ensure_ascii=False)
print("galleries:", {k: v[1] for k, v in sizes.items()}, "screens:", len(SC.S))
