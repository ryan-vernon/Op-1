# OP-1 Tombola

A web instrument after the teenage engineering OP-1, built around its Tombola sequencer. It runs in the browser on phones and iPads, and plays from a MIDI keyboard.

The page itself is one file, `tombola.html`. Cloud saving lives in `src/cloud.js`, and the database is defined in `dataconnect/`.

## Layout

Everything sits on a grid of white tiles. One unit is the width of a white key.

- **Phone (portrait):** the screen, then T1–T4, then the transport row (record, play, stop, sequencer, octave down and up, shift), then one octave of keys, then the four mode keys.
- **iPad (landscape, 900px and wider):** an 18 × 12 grid.
  - A 2:1 display sits on top, flanked by the OP-1's keys and four encoders.
  - A full-width keyboard runs 2½ octaves, C3 to F5.

## Modes

- **Synth:**
  - **T1 engine:** five engines: digital, fm, string, pulse, cluster. Press T1 again for the next engine.
  - **T2 envelope:** attack, decay, sustain, release.
  - **T3 spring reverb:** press T3 again to turn it on or off.
  - **T4 LFO:** speed, pitch, volume and wave.
- **Sequencer (SEQ):** the spinning Tombola. Tap inside to drop notes and drag to spin. Its corners set speed, gravity, shape and mass. With SHIFT, T1–T4 lay five notes, clear, change key and change scale.
- **Drum:** a synthesized kit with one sound per semitone. T1 sets pitch, decay, tone and level.
- **Tape:**
  - Four tracks. T1–T4 pick the track; SHIFT plus a T key clears it.
  - REC records notes from the keys, MIDI and the Tombola onto the selected track. The tape loops over the bars you set.
  - The tape records MIDI notes, not audio.
- **Mixer:** T1 sets the four track levels. T2 sets master, live, effect send and the metronome click.

Each page shows its four parameters in the screen's corners, in the encoder colors: blue, green, white and orange.
- To change a value, drag a corner up or down.
- On iPad, you can turn the encoders instead.
- With a MIDI controller, the first four knobs you move become the four encoders.

You can also play from a computer keyboard: `a w s e d f t g y h u j k` play C to C, and `z` / `x` change the octave.

## Saving songs (Firebase)

Tap the song name at the top of the screen (or the album key on iPad) to open the song sheet.

- You sign in with Google through **Firebase Auth**.
- Songs are stored in **Firebase SQL Connect**, a managed Postgres database.
- `dataconnect/schema/schema.gql` defines four tables:
  - users
  - songs: title, tempo, and every sound setting as JSON
  - patterns: the Tombola's notes
  - recordings: one row per tape track, as `[tick, note, velocity, durationTicks]` events
- Recordings are small JSON, so nothing goes to Cloud Storage.
- Every query and mutation in `dataconnect/connector/` is limited to the signed-in user's own rows.

## Running locally

Start the Auth and SQL Connect emulators. The page talks to them whenever it's served from `localhost`.

```bash
firebase emulators:start --only auth,dataconnect --project demo-tombola
```

Build the page and serve it:

```bash
bash build.sh && python3 -m http.server 8765
```

Then open http://localhost:8765/public/index.html.

## Hosting and deploying

The app runs on **Firebase App Hosting** in its own project, `op-1-57510` (set in `.firebaserc`), separate from the original Tombola site:

- **Live at:** https://op-1--op-1-57510.us-central1.hosted.app
- **Backend:** `op-1`, in us-central1.
- **How it runs:** App Hosting runs `npm run build` (which calls `build.sh`) and then `npm start`. `server.js` is a tiny dependency-free static server for `public/`.
- **Scaling:** `apphosting.yaml` lets it scale to zero, up to 2 instances.
- **Deploy:**
  ```bash
  firebase deploy --only apphosting
  ```
  The upload skips anything in `.gitignore`.
- **Web app config:** `src/webapp-config.json` holds the Firebase web app config, which is public by design. App Hosting reserves `/__/` paths, so `/__/firebase/init.json` isn't available there.
- **SQL Connect:** service `tombola` on the Cloud SQL instance `tombola-fdc`, under the SQL Connect no-cost trial. Deploy it with:
  ```bash
  firebase deploy --only dataconnect
  ```

To move to plain Firebase Hosting later and save money, run:

```bash
firebase deploy --only hosting
```

The `hosting` block in `firebase.json` is ready, and the page works on either host. Then delete the App Hosting backend:

```bash
firebase apphosting:backends:delete op-1
```

Google sign-in needs two console settings:

1. Enable the Google provider under Authentication → Sign-in method.
2. Add `op-1--op-1-57510.us-central1.hosted.app` under Authentication → Settings → Authorized domains.

## Agent skills

The Firebase agent skills (github.com/firebase/agent-skills) are installed in `.claude/skills/` for Claude Code.
