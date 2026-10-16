# OP-School audio analysis (first pass)

Findings (video 02, synth mode):
- The audio is effectively mono (L/R correlation 0.9993), so a mid/side trick cannot remove the narrator.
- The narrator speaks almost continuously. Only 13 gaps of 2 s or more in 272 s; the longest is 222-240 s (the LFO section).
- Held notes under the narration show up as horizontal harmonic lines in a spectrogram (`spec.py`); `segs.py` lists them.
- The videos are overviews with short demonstrations, not systematic sweeps of one encoder per sound. They give a rough timbre reference, not measurable parameters for each engine and effect.

Usage: `bash download.sh ./opschool`, then `python3 segs.py opschool/stereo/02_*.wav opschool/stereo/02_*.en.vtt`.
