# Handoff: match the sounds to the real OP-1

This note is for a fresh Claude session. The goal is to make the app's synth engines, effects, LFOs and drums sound like the original OP-1. Use teenage engineering's OP-School videos (about 5 or 6 on YouTube) as the reference.

The visual design work is paused. Ryan wants the audio done first, and Figma comes after.

## Where things are

- **App:** `tombola.html`, a single file with all the JS inline.
  - `bash build.sh` builds `public/`.
  - Serve locally with `python3 -m http.server 8765`, then open http://localhost:8765/public/index.html.
- **Live site:** https://op-1--op-1-57510.us-central1.hosted.app. It runs on Firebase App Hosting, project `op-1-57510`, backend `op-1`.
- **Deploying:**
  1. Commit first. App Hosting builds the last commit.
  2. Run `git push origin op1-modes-firebase:main`.
  3. Run `firebase deploy --only apphosting --project op-1-57510 --non-interactive`.
- **Repo:** https://github.com/ryan-vernon/Op-1. Work on branch `op1-modes-firebase` and push it to `main`.

## Sound code in `tombola.html`

| What | Where to look |
|---|---|
| Synth engines | `ENGINES` (labels, defaults) and `playNote()`. Each engine is a `case` reading `sv(0..3)`, the four encoders as 0–1. `digiGen` / `digiBuffer` and `ksBuffer` hold the Digital and String synthesis. |
| Effects | `FX_TYPES` (labels) and `makeFx(type)`. `T`, `R`, `D` and `W` are the blue, green, white and orange encoders, in the `P.taper`, `P.turns`, `P.damp` and `P.width` slots. The spring reverb impulse is `springIR()`. |
| LFOs | `lfoTargets()`, `updateLfo()`, `lfoEnvKick()` and `lfoHz()`. Tremolo speed is tempo-synced through `LFO_DIVS`. |
| Drums | `synthHit()` renders a 12-second kit offline. `playDrum()` plays one part per key, with in/out points, pitch, direction, play mode, level and the T2 dynamic envelope (`P.dyatk`, `P.dymid`, `P.dyrel`, `P.dyreg`). |
| Master chain | `ensureAudio()`. The chain is master → drive → 3-band EQ → low shelf → compressor → output. `updateGains()` sets the levels. |

## Correct encoder names

These come from the original OP-1 Operator's Manual, reference pages 41–45. A new session won't have the copy from this one; the PDF is linked from teenage.engineering. The OP-1 field guide at teenage.engineering/guides/op-1 adds a few. Encoder order is blue, green, white, orange.

**Synth engines**

| Engine | Blue | Green | White | Orange |
|---|---|---|---|---|
| Cluster | number of waves | wave envelope | spread | unitor |
| Digital | wave shaper | octave | detune / ring mod | digitalness |
| String | tension | impulse decay | detune | impulse type |
| Pulse | filter | amplitude | second pulse | modulation |
| FM | topology | freq | FM amount | detune |

The app's FM order differs from the manual: it is FM amount, frequency, topology, detune. Check this against the video.

**Effects**

| Effect | Blue | Green | White | Orange |
|---|---|---|---|---|
| Delay | size | speed | feedback | mix |
| Grid | X size | Y size | Z feedback | mix |
| Nitro | frequency | filter frequency follow | resonance | frequency |
| Phone | tone | phonic | baud | telematic |
| Punch | frequency | punch | rounds | power |
| Spring | tone | turns | damping | send |

The app's labels differ slightly. Its Nitro reads "freq, ff, res, freq", which is already close.

**Tremolo LFO** (field guide): blue speed, green pitch amount, white volume, orange envelope. With Shift, blue is fine speed and orange picks the shape: sine, saw, exp, square or blip.

## The plan

1. **Ask Ryan before downloading anything.** He has asked to analyse the OP-School videos. Confirm the list of video URLs with him first.
2. **Install the tools.** Neither Homebrew nor ffmpeg is on this Mac. Run `python3 -m pip install --user yt-dlp numpy scipy matplotlib imageio-ffmpeg`. `imageio-ffmpeg` provides an ffmpeg binary; get its path with `python3 -c "import imageio_ffmpeg; print(imageio_ffmpeg.get_ffmpeg_exe())"`.
3. **Download the audio only.** Use `yt-dlp -x --audio-format wav --ffmpeg-location <path>`, plus a few low-resolution keyframes so you can see which screen and encoder is shown at each timestamp.
4. **Make spectrograms and measure.** For each segment where one engine or effect is played and one encoder is turned, make a spectrogram with matplotlib and look at the PNG. Measure from it:
   - delay and echo spacing and how fast the echoes decay
   - filter cutoff sweeps
   - LFO rates and depths
   - which harmonics and inharmonic partials are present, and noise
   - envelope times
   - how each of these changes as the encoder turns
5. **Change the matching code and measure again.** Change the code in `playNote` / `makeFx` / `updateLfo` / `playDrum`. Then render the app's own sound for the same settings with an `OfflineAudioContext` in the browser, or record it, and compare spectrograms.
6. **Report honestly.** This is measuring, not listening. Tell Ryan what matched and what is still a guess.

## Notes

- Ryan is on a budget. Avoid subagents and keep tool output small (crop and downscale images).
- Commit messages end with `Co-Authored-By: Claude <noreply@anthropic.com>` in the attribution format the session gives you.
- **Screen drawings (on hold):**
  - Scripts: `design/screens/` (`screens.py` and `screens_r13.py`).
  - Export: `python3 design/screens/screens_r13.py "design/op-1 emulator"`.
  - Output: the SVGs in `design/op-1 emulator/` are the copies Ryan drags into Figma.
  - Ryan finds the drawings rough.
