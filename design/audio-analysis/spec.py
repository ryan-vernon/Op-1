import numpy as np, scipy.io.wavfile as w, scipy.signal as sg, scipy.ndimage as nd, matplotlib
matplotlib.use('Agg'); import matplotlib.pyplot as plt
def load(path):
    sr, x = w.read(path); x = x.astype(np.float32)/32768
    return sr, (x.mean(axis=1) if x.ndim > 1 else x)
def stft(x, sr, n=4096, hop=1024):
    f, t, Z = sg.stft(x, sr, nperseg=n, noverlap=n-hop, window='hann'); return f, t, Z
def steady(S, secs, hop_s, harm_secs=0.0):
    """keep the steady part of a magnitude spectrogram: median over time (kills speech syllables, keeps held tones)"""
    k = max(3, int(secs/hop_s)) | 1
    return nd.median_filter(S, size=(1, k))
def plot(S, f, t, fmax, path, title, lo=-90, size=(24, 6)):
    db = 20*np.log10(S + 1e-7); m = f <= fmax
    fig, ax = plt.subplots(figsize=size, dpi=100)
    ax.imshow(db[m][::-1], aspect='auto', extent=[t[0], t[-1], 0, fmax], cmap='magma', vmin=lo, vmax=lo+70)
    ax.set_title(title); ax.set_xlabel('s'); ax.set_ylabel('Hz'); fig.tight_layout(); fig.savefig(path); plt.close(fig)
