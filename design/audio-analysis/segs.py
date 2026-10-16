import sys; sys.path.insert(0, '.')
from spec import *
import captions
def segments(path, minlen=1.0):
    sr, x = load(path)
    f, t, Z = stft(x, sr, 4096, 1024); S = np.abs(Z); hop = t[1]-t[0]
    m = (f > 60) & (f < 6000); A = S[m]
    A = np.log1p(A*200)
    # frame-to-frame similarity of the spectrum, and level
    num = (A[:, 1:]*A[:, :-1]).sum(0); den = np.sqrt((A[:, 1:]**2).sum(0)*(A[:, :-1]**2).sum(0)) + 1e-9
    sim = np.r_[1, num/den]; lvl = 20*np.log10(np.sqrt((x[:len(t)*1024]**2).reshape(-1, 1024).mean(1))+1e-9)[:len(t)] if False else None
    rms = np.array([np.sqrt(np.mean(x[int(i*hop*sr):int(i*hop*sr)+4096]**2)) for i in range(len(t))])
    ok = (nd.uniform_filter1d(sim, int(0.25/hop)) > 0.93) & (rms > 0.01)
    segs, i = [], 0
    while i < len(ok):
        if ok[i]:
            j = i
            while j < len(ok) and ok[j]: j += 1
            if (j-i)*hop >= minlen: segs.append((t[i], t[j-1]))
            i = j
        else: i += 1
    return sr, x, segs
def describe(x, sr, a, b):
    seg = x[int(a*sr):int(b*sr)]; core = seg[len(seg)//5: len(seg)-len(seg)//5]
    n = 1 << 16; win = core[:n] if len(core) >= n else np.pad(core, (0, n-len(core)))
    sp = np.abs(np.fft.rfft(win*np.hanning(len(win)))); fr = np.fft.rfftfreq(len(win), 1/sr)
    band = (fr > 50) & (fr < 1200); k = np.argmax(sp[band]); f0 = fr[band][k]
    # refine: the lowest strong partial that is a subharmonic of the peak
    for d in (4, 3, 2):
        c = f0/d
        if c > 55:
            j = np.argmin(abs(fr-c)); lo, hi = max(0, j-3), j+4
            if sp[lo:hi].max() > 0.35*sp[band].max(): f0 = fr[lo:hi][np.argmax(sp[lo:hi])]; break
    harm = []
    for h in range(1, 13):
        j = np.argmin(abs(fr-f0*h)); lo, hi = max(0, j-4), j+5
        harm.append(sp[lo:hi].max())
    harm = np.array(harm); harm = harm/(harm.max()+1e-9)
    cen = (fr*sp).sum()/sp.sum()
    # noisiness: energy not at harmonics
    mask = np.zeros_like(sp, bool)
    for h in range(1, 60):
        j = np.argmin(abs(fr-f0*h)); mask[max(0, j-4):j+5] = True
    noise = sp[~mask].sum()/sp.sum()
    rms = np.sqrt(np.mean(core**2))
    return dict(f0=round(float(f0), 1), harm=[round(float(v), 2) for v in harm], centroid=int(cen), noise=round(float(noise), 2), rms=round(float(rms), 3))
if __name__ == '__main__':
    path, vtt = sys.argv[1], sys.argv[2]
    sr, x, segs = segments(path)
    w = captions.words(vtt)
    print(len(segs), 'steady segments')
    for a, b in segs:
        d = describe(x, sr, a, b)
        near = ' '.join(wd for tt, wd in w if a-4 <= tt <= b+1)[:90]
        print(f'{a:6.1f}-{b:6.1f} f0={d["f0"]:6.1f} cen={d["centroid"]:5d} noise={d["noise"]:.2f} rms={d["rms"]:.3f} | {near}')
