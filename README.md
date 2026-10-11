# Tombola

A web version of the Tombola spinning sequencer from the teenage engineering OP-1, built for a portrait phone screen. Notes bounce around inside a spinning hexagon and play a sound each time they hit a wall.

Everything lives in one self-contained file, `tombola.html`. Open it in a browser and tap once to turn on the sound.

## Controls

- **Tap inside the hexagon** to drop a note. Higher taps play higher notes on a two-octave pentatonic scale. Each note's pattern (blank, filled, stripes, dots, grid) shows its scale degree.
- **Drag or flick** the screen to spin the hexagon. It slows back down to the set speed.
- **Corner icons** are the four OP-1 encoders. Tap one to show its encoder ring, then drag the ring or the icon up and down to turn it.
  - **S** (blue): speed and direction of rotation
  - **G** (green): gravity
  - **M** (orange): mass, or bounciness. Harder hits play louder.
  - **Hexagon** (white): shape. Opens the sides and lets the notes out.
- **Synth icon** (below the tombola) opens the synth screen. It has five engines (digital, fm, string, pulse, cluster), each with four color-coded parameters, plus key, scale, tilt, "lay 5" and clear.
- **Spring icon** opens the spring reverb: taper, turns, damp and width.
- **Tilt** (on phones): gravity follows the device, and rolling it sideways opens the hexagon. Motion sensors need the page served over HTTPS from its own address. They're blocked inside embedded viewers.

## Running locally

```bash
python3 -m http.server 8765
```

Then open http://localhost:8765/tombola.html.
