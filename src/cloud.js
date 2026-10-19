// Cloud saving for Tombola: Firebase Auth (Google sign-in), Cloud Firestore for songs and sounds, and Cloud Storage for the big
// files (the tape tracks). Everything plays without an account; signing in is only needed to keep a sound, a sequence or a recording.
//
// Firestore (every path is under the signed-in person's own id; see firestore.rules):
//   users/{uid}                       display name
//   users/{uid}/presets/slots         { json: the eight synth sounds and eight drum kits, updatedAt }
//   users/{uid}/songs/{songId}        { title, tempo, json: settings + sequencers + tape track list, updatedAt, createdAt }
// Cloud Storage (storage.rules):
//   users/{uid}/songs/{songId}/track-{n}.json   the notes of one tape track
// (Firestore cannot hold arrays inside arrays, so the song state travels as one JSON string.)
// On localhost the page talks to the Auth, Firestore and Storage emulators.
const SDK = 'https://www.gstatic.com/firebasejs/12.6.0/';
const LOCAL = ['localhost', '127.0.0.1'].includes(location.hostname);
const $ = s => document.querySelector(s);
const T = () => window.Tombola;

const acct = $('#acct'), list = $('#songList'), saveBtn = $('#saveSong'), state = $('#saveState');
let auth, A, F, S, db, store, user = null, songId = null, busy = false, presetTimer = 0, pendingSave = false;

function remember(id) { try { id ? localStorage.setItem('tombola.song', id) : localStorage.removeItem('tombola.song'); } catch (e) {} }
function recalled() { try { return localStorage.getItem('tombola.song'); } catch (e) { return null; } }
const say = msg => { state.textContent = msg; };
const uidPath = (...p) => ['users', user.uid, ...p];

async function config() {
  if (LOCAL) return {apiKey: 'demo-key', authDomain: 'demo-tombola.firebaseapp.com', projectId: 'demo-tombola', appId: 'demo-app', storageBucket: 'demo-tombola.appspot.com'};
  // The web app config (public by design) is in src/webapp-config.json; Firebase Hosting also serves it
  // at /__/firebase/init.json, but App Hosting reserves /__/ paths.
  for (const url of ['src/webapp-config.json', '/__/firebase/init.json']) {
    try { const r = await fetch(url); if (r.ok) return await r.json(); } catch (e) {}
  }
  throw new Error('This site has no Firebase web app config.');
}

/* ---------- account ---------- */
function renderAcct() {
  acct.innerHTML = '';
  if (!user) {
    const b = document.createElement('button'); b.textContent = 'sign in';
    b.onclick = signIn; acct.append(b);
  } else {
    const n = document.createElement('span'); n.textContent = user.displayName || user.email || 'signed in';
    const b = document.createElement('button'); b.textContent = 'sign out';
    b.onclick = () => A.signOut(auth);
    acct.append(n, b);
  }
  saveBtn.textContent = 'save';
}
async function signIn() {
  if (!auth) { say('sign-in is not available right now'); return false; }
  const p = new A.GoogleAuthProvider();
  try { await A.signInWithPopup(auth, p); return true; }
  catch (e) {
    if (e.code === 'auth/popup-blocked' || e.code === 'auth/operation-not-supported-in-this-environment') { A.signInWithRedirect(auth, p); return false; }
    if (e.code !== 'auth/popup-closed-by-user' && e.code !== 'auth/cancelled-popup-request') say(e.message);
    return false;
  }
}

/* ---------- sounds: the eight synth sounds and eight drum kits follow the account ---------- */
const presetDoc = () => F.doc(db, ...uidPath('presets', 'slots'));
async function savePresets() {
  if (!user) return;
  try {
    const p = T().getPresets();
    await F.setDoc(presetDoc(), {json: JSON.stringify({synth: p.synth, drum: p.drum}), updatedAt: F.serverTimestamp()});
  } catch (e) { say('could not save your sounds: ' + (e.message || e)); }
}
async function syncPresets() {   // after signing in: your account's sounds, with any you saved here before signing in on top
  const mine = T().getPresets(), snap = await F.getDoc(presetDoc());
  if (snap.exists()) {
    try {
      const theirs = JSON.parse(snap.data().json);
      for (const pm of ['synth', 'drum']) mine.mods[pm].forEach(i => { if (Array.isArray(theirs[pm])) theirs[pm][i] = mine[pm][i]; });
      T().setPresets(theirs);
    } catch (e) {}
  }
  if (mine.mods.synth.length || mine.mods.drum.length || !snap.exists()) await savePresets();
}
window.addEventListener('tombola:preset', () => { if (!user) return; clearTimeout(presetTimer); presetTimer = setTimeout(savePresets, 800); });

/* ---------- songs ---------- */
async function refresh() {
  list.innerHTML = '';
  if (!user) return;
  const snap = await F.getDocs(F.query(F.collection(db, ...uidPath('songs')), F.orderBy('updatedAt', 'desc')));
  snap.forEach(d => {
    const s = d.data(), li = document.createElement('li');
    const open = document.createElement('button'); open.className = 'open';
    const when = s.updatedAt && s.updatedAt.toDate ? s.updatedAt.toDate().toLocaleDateString(undefined, {month: 'short', day: 'numeric'}) : '';
    open.textContent = s.title; if (d.id === songId) open.classList.add('cur');
    open.onclick = () => load(d.id);
    const del = document.createElement('button'); del.className = 'del'; del.textContent = '×';
    del.setAttribute('aria-label', 'Delete ' + s.title);
    del.onclick = async () => {
      if (!confirm(`Delete “${s.title}”? Its tape tracks and sequences go with it.`)) return;
      try { for (const r of JSON.parse(s.json).recordings || []) if (r.path) await S.deleteObject(S.ref(store, r.path)).catch(() => {}); } catch (e) {}
      await F.deleteDoc(d.ref);
      if (d.id === songId) { songId = null; remember(null); }
      refresh();
    };
    li.append(open, del); list.append(li);
  });
  if (snap.empty) list.innerHTML = '';
}

async function save() {
  if (busy) return;
  if (!user) { say('sign in with Google to save'); pendingSave = true; if (!(await signIn())) pendingSave = false; return; }   // once signed in, the auth listener saves
  busy = true; saveBtn.disabled = true; say('saving…');
  try {
    const s = T().songState(), col = F.collection(db, ...uidPath('songs'));
    const ref = songId ? F.doc(col, songId) : F.doc(col), id = ref.id;
    const recs = [];
    for (const r of s.recordings) {   // the notes of each tape track are a file in Cloud Storage; the song keeps where it is
      const path = `users/${user.uid}/songs/${id}/track-${r.track}.json`;
      if (r.events.length && r.instrument) {
        const body = JSON.stringify({instrument: r.instrument, events: r.events});
        try { await S.uploadString(S.ref(store, path), body, 'raw', {contentType: 'application/json'}); recs.push({track: r.track, ppq: r.ppq, lengthTicks: r.lengthTicks, count: r.events.length, path}); }
        catch (e) {
          if (body.length > 600000) throw e;   // too big to carry in the song itself
          recs.push({track: r.track, ppq: r.ppq, lengthTicks: r.lengthTicks, count: r.events.length, instrument: r.instrument, events: r.events});
        }
      } else if (songId) await S.deleteObject(S.ref(store, path)).catch(() => {});
    }
    const json = JSON.stringify({settings: s.settings, patterns: s.patterns, pattern: s.pattern, recordings: recs});
    if (json.length > 900000) throw new Error('this song is too large to save');
    const data = {title: s.title, tempo: s.tempo, json, updatedAt: F.serverTimestamp()};
    if (!songId) data.createdAt = F.serverTimestamp();
    await F.setDoc(ref, data, {merge: true});
    songId = id; remember(songId);
    T().saved(); say('saved'); refresh();
  } catch (e) { say('could not save: ' + (e.message || e)); }
  busy = false; saveBtn.disabled = false;
}

async function load(id) {
  if (T().dirty && !confirm('Open this song? Unsaved changes to the current one will be lost.')) return;
  say('opening…');
  try {
    const snap = await F.getDoc(F.doc(db, ...uidPath('songs', id)));
    if (!snap.exists()) { say('that song is gone'); remember(null); return refresh(); }
    const d = snap.data(), body = JSON.parse(d.json), recordings = [];
    for (const r of body.recordings || []) {
      let inst = r.instrument, events = r.events;
      if (r.path) { const f = JSON.parse(new TextDecoder().decode(await S.getBytes(S.ref(store, r.path)))); inst = f.instrument; events = f.events; }
      recordings.push({track: r.track, ppq: r.ppq, lengthTicks: r.lengthTicks, instrument: inst, events: events || []});
    }
    T().loadSong({title: d.title, tempo: d.tempo, settings: body.settings, patterns: body.patterns, pattern: body.pattern, recordings});
    songId = id; remember(songId);
    try { const p = await F.getDoc(presetDoc()); if (p.exists()) T().setPresets(JSON.parse(p.data().json)); } catch (e) {}   // your sounds stay yours, whichever song is open
    $('#songTitle').value = d.title; say(''); refresh();
  } catch (e) { say('could not open: ' + (e.message || e)); }
}

saveBtn.onclick = save;
$('#newSong').onclick = () => {
  if (T().dirty && !confirm('Start a new song? Unsaved changes will be lost.')) return;
  T().newSong(); songId = null; remember(null); $('#songTitle').value = 'untitled'; say(''); refresh();
};
window.addEventListener('tombola:sheet', () => { if (user) refresh(); });
window.TombolaCloud = {signedIn: () => !!user};

(async () => {
  try {
    const cfg = await config();
    const [fa, fauth, ffs, fst] = await Promise.all([import(SDK + 'firebase-app.js'), import(SDK + 'firebase-auth.js'), import(SDK + 'firebase-firestore.js'), import(SDK + 'firebase-storage.js')]);
    A = fauth; F = ffs; S = fst;
    const app = fa.initializeApp(cfg);
    auth = A.getAuth(app); db = F.getFirestore(app); store = S.getStorage(app);
    if (LOCAL) {
      A.connectAuthEmulator(auth, 'http://127.0.0.1:9099', {disableWarnings: true});
      F.connectFirestoreEmulator(db, '127.0.0.1', 8080);
      S.connectStorageEmulator(store, '127.0.0.1', 9199);
    }
    renderAcct();
    A.onAuthStateChanged(auth, async u => {
      user = u; renderAcct();
      if (!u) { songId = null; list.innerHTML = ''; return; }
      try {
        await F.setDoc(F.doc(db, ...uidPath()), {displayName: u.displayName || null, updatedAt: F.serverTimestamp()}, {merge: true});
        await syncPresets();
        const last = recalled();
        if (last && !T().dirty) await load(last); else await refresh();
        if (pendingSave) { pendingSave = false; await save(); }
        else if (/^sign in/i.test(state.textContent)) say('signed in');
      } catch (e) { say(e.message || String(e)); }
    });
  } catch (e) {
    acct.innerHTML = '<span class="muted"></span>';
    acct.firstChild.textContent = 'Cloud saving is unavailable: ' + (e.message || e);
  }
})();
