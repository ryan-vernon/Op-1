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
