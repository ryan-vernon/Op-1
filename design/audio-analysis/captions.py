import re, sys, json
def ts(s):
    h, m, r = s.split(':'); return int(h)*3600 + int(m)*60 + float(r)
def words(path):
    out = []
    for block in open(path).read().split('\n\n'):
        lines = block.strip().split('\n')
        if len(lines) < 3 or '-->' not in lines[0]: continue
        a, b = lines[0].split(' --> '); a = ts(a); b = ts(b.split()[0])
        for ln in lines[1:]:
            if '<c>' not in ln and '<00:' not in ln: continue
            toks = re.split(r'<(\d\d:\d\d:\d\d\.\d+)>', ln)   # text, time, text, time, text ...
            cur = a; 
            for i in range(0, len(toks), 2):
                txt = re.sub(r'</?c>', '', toks[i]).strip()
                if i > 0: cur = ts(toks[i-1])
                if txt: out.append([cur, txt])
    # drop duplicates produced by overlapping cues
    seen, res = set(), []
    for t, w in out:
        k = (round(t, 2), w)
        if k in seen: continue
        seen.add(k); res.append([t, w])
    res.sort()
    return res
def timeline(path, dur, mingap=2.0):
    w = words(path)
    ends = [min(w[i+1][0], w[i][0] + 0.6) if i+1 < len(w) else w[i][0] + 0.5 for i in range(len(w))]
    gaps, prev = [], 0.0
    for (t, x), e in zip(w, ends):
        if t - prev >= mingap: gaps.append((prev, t))
        prev = max(prev, e)
    if dur - prev >= mingap: gaps.append((prev, dur))
    return w, gaps
if __name__ == '__main__':
    w, gaps = timeline(sys.argv[1], float(sys.argv[2]), float(sys.argv[3]) if len(sys.argv) > 3 else 2.0)
    print(len(w), 'words;', len(gaps), 'gaps')
    for a, b in gaps:
        before = ' '.join(x for t, x in w if a - 6 < t <= a)[-70:]
        after = ' '.join(x for t, x in w if b <= t < b + 5)[:60]
        print(f'{a:6.1f}-{b:6.1f} ({b-a:4.1f}s) ...{before} || {after}')
