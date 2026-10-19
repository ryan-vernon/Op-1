# What the OP-School videos told us (first pass)

Source: the ten OP-School videos on YouTube (OP-1 overview, synth, drum, tape, mixer, and the Endless, Finger, Sketch, Pattern and Tombola sequencers).
Method: spectrograms of the audio, the captions for what the narrator says when, and video frames for which knob the hands turn.
Limits: the audio is mono and the narrator speaks nearly all the time, so only a few stretches are clean. This is measuring, not hearing.

## Measured
- **Tremolo LFO** (synth video, 227-239 s, held middle C, LFO turned up): loudness wobbles at about 5.3 Hz, 2-8 dB rms; pitch moves only 1-7 cents rms, with one spike (about 16 cents rms) when the pitch knob goes up. Our tremolo is tempo-synced; 5.3 Hz is a bit faster than 1/8 at 120 bpm (4 Hz).
- **Master out drive** (mixer video, a song playing): compared with the same song before the drive was touched, the loud-to-quiet spread narrows from about 23 dB to 15 dB, the median rises about 5 dB, peaks stay the same, and energy above 4 kHz goes from 3% to 4-6%. Implemented as a compressor with make-up gain plus mild saturation.
- **Held notes** show flat levels, a dense harmonic comb up to 4-6 kHz and abrupt stops in the clean engine-audition and effect sections. Pure harmonic series with no noise between them (the default engine), pitch exactly on the note.

## Told by the narrator
- Synth and drum effects are mono. The stereo reverb comes only from the **master effect** (mixer T3), which can be any effect, "modified for stereo".
- Mixer T1: blue/green/white/orange set the levels of tracks 1-4. SHIFT + encoder sets each track's pan. SHIFT + track key mutes it, and its level can still be adjusted while muted.
- Mixer T2: blue/green/white are low/mid/high; turning everything down kills the sound; orange is the overall EQ level.
- Mixer T4: blue and green are master left and right (SHIFT turns both), white is drive, orange is the release of the drive.
- Drum mode: blue pitch (SHIFT: direction), green in, white out (SHIFT: fine), orange play mode (SHIFT: volume). 24 keys per kit, settings per key. T2: blue attack level, green mid level, white release level, orange the region.
- Tombola: blue rotation speed and direction (SHIFT + blue: crank mode), green gravity, orange mass, white shape.
- Synth mode: SHIFT + 1-8 replaces a preset: blue chooses the engine, green the preset for that engine. SHIFT + T2 opens play mode (poly, mono, legato, unison) and portamento.

## Not measurable from these videos
Per-engine and per-effect knob sweeps. The narrator describes where to find things, and the demonstrations are short and spoken over.
Recordings of a real OP-1 playing one note while turning one encoder would give exact numbers.

## Round 21: digital engine and phone effect, from three more recordings

Sources (audio only, analysed as spectrograms; the narration is on top, so only steady passages were used):
- Ollie Loops, "OP-1: Synth Engines Demo" (https://www.youtube.com/watch?v=RzPKrDPWbMc), 0:07-0:31 digital pads and 0:54-1:04 digital plucks.
- The Unperson, "Exploring Teenage Engineering OP1 Synth Engines" (https://www.youtube.com/watch?v=RMZQ_xt--ps), 13:50-14:35 digital, 15:15-15:40 phone effect.
- Gregonater, "OP-1 Synthesizer Engines Walkthrough" (https://www.youtube.com/watch?v=DHeFyJLrUjQ), 4:42-6:25 digital.

Findings:
- **Digital:** 60-70% of the energy sits below 500 Hz, over 90% below 1 kHz, 2-4 kHz holds 2-4%, and nothing above 4 kHz. Ours was bright: 53% at 1-2 kHz and 6-8% above 4 kHz, from a hard wave fold (x7) and the sample-and-hold images. Now: fold x3.5 and two one-pole low-passes at max(1.5 kHz, 7 x pitch).
- **Phone:** in the loudest phone passage 88% of the energy is 300 Hz to 3.4 kHz, none below 300 Hz and under 10% above 3.4 kHz, with a faint grid of clicks (a coarse sampler). Ours only added noise to the dry sound. Now it replaces the dry sound: 220-740 Hz high-pass, 2.6-4.5 kHz low-pass, a sample-and-hold and bit reducer driven by the baud encoder (hold 2-28 samples, 10 to 3 bits), a shaper (phonic) and line noise (telematic).

## Round 34: compared with recordings of the original OP-1

References (line-out recordings on YouTube, audio only, analysed with spectrograms and level measurements):
Red Means Recording "Effects" (xrakJyT8blM), "Drum Engines" (J9F00exP4H8), "Synthesizer Engines" (3s285Il7dt0), "Modulators" (zdl3xsmDkCo), "Sequencers" (aZiploFCxq8);
MyReasonToPlay review (9OXMgnHxIik); SynthDawg Nitro/Crank/Bend (aJYHvBXZhb8) and New OS (5K2xAEfQesQ); Ollie Loops engines (RzPKrDPWbMc);
Mamotreco Pulse (mKX9eBtxvlI) and Digital (7d_AK2uOdOM); Jakob Haq String (mI_qNsOaj4M).

- Every effect section measures L/R correlation 1.000: voices and patch effects are mono. The live voice bus is now mono; width comes only from the tape tracks' pan and the master effect.
- Grid was a tempo gate. The recordings show fixed comb resonances and echoes that ring: it is now a feedback plate (a worklet): X tunes a short comb, Y sets the echo time (changed by crossfade, so the pitch never slides), Z feeds both with saturation.
- CWO was a ring modulator. The recordings show each echo shifted further in frequency (rising and falling ladders): it is now a single-sideband frequency shifter in a feedback delay; sideband goes down, both (ring) or up.
- Nitro: green is how far the input's loudness opens the low-pass (envelope follow), not drive; the resonance goes high enough to sing.
- Punch: a resonant low-pass in front of the compressor, and a bigger low end as power goes up (the recordings show a large sub boost).
- Phone: full range with rhythmic dropouts at the baud rate (the recordings show vertical "glitch" striping across the whole spectrum), not a narrow telephone band.
- Delay: speed now scales the time like tape speed; the old wobble moved the pitch by several percent, which the recordings do not show.
- DBox: hits are much shorter by default (the reference hits are short and snappy). Pulse: 7 dB louder, to match the reference level.
