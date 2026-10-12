// Cloud saving for Tombola: Firebase Auth (Google sign-in) and Firebase SQL Connect.
// Songs, tombola patterns and tape tracks (MIDI note lists) are stored as rows; there is no audio,
// so Cloud Storage isn't needed. The operations are defined in dataconnect/connector/*.gql and
// called here by name. On localhost the page talks to the Auth and SQL Connect emulators.
const SDK = 'https://www.gstatic.com/firebasejs/12.6.0/';
const LOCAL = ['localhost', '127.0.0.1'].includes(location.hostname);
const CONNECTOR = {connector: 'tombola', service: 'tombola', location: 'us-central1'};
const $ = s => document.querySelector(s);
const T = () => window.Tombola;

const acct = $('#acct'), list = $('#songList'), saveBtn = $('#saveSong'), state = $('#saveState');
let auth, A, D, dc, user = null, songId = null, busy = false;

function remember(id) { try { id ? localStorage.setItem('tombola.song', id) : localStorage.removeItem('tombola.song'); } catch (e) {} }
function recalled() { try { return localStorage.getItem('tombola.song'); } catch (e) { return null; } }
const say = msg => { state.textContent = msg; };

async function config() {
  if (LOCAL) return {apiKey: 'demo-key', authDomain: 'demo-tombola.firebaseapp.com', projectId: 'demo-tombola', appId: 'demo-app'};
  const r = await fetch('/__/firebase/init.json');   // served by Firebase Hosting for this project's web app
  if (!r.ok) throw new Error('This site has no Firebase web app yet.');
  return r.json();
}
const q = (name, vars) => D.executeQuery(D.queryRef(dc, name, vars)).then(r => r.data);
const m = (name, vars) => D.executeMutation(D.mutationRef(dc, name, vars)).then(r => r.data);

function renderAcct() {
  acct.innerHTML = '';
  if (!user) {
    const b = document.createElement('button'); b.className = 'sbtn pri'; b.textContent = 'sign in with Google';
    b.onclick = signIn; acct.append(b);
    const n = document.createElement('span'); n.className = 'muted'; n.textContent = 'to save songs to your account';
    acct.append(n);
  } else {
    const n = document.createElement('span'); n.textContent = user.displayName || user.email || 'signed in';
    const b = document.createElement('button'); b.className = 'sbtn'; b.textContent = 'sign out';
    b.onclick = () => A.signOut(auth);
    acct.append(n, b);
  }
  saveBtn.disabled = !user;
}
async function signIn() {
  const p = new A.GoogleAuthProvider();
  try { await A.signInWithPopup(auth, p); }
  catch (e) {
    if (e.code === 'auth/popup-blocked' || e.code === 'auth/operation-not-supported-in-this-environment') return A.signInWithRedirect(auth, p);
    if (e.code !== 'auth/popup-closed-by-user' && e.code !== 'auth/cancelled-popup-request') say(e.message);
  }
}

async function refresh() {
  list.innerHTML = '';
  if (!user) return;
  const {songs} = await q('MySongs');
  for (const s of songs) {
    const li = document.createElement('li');
    const open = document.createElement('button'); open.className = 'open';
    const when = new Date(s.updatedAt).toLocaleDateString(undefined, {month: 'short', day: 'numeric'});
    open.innerHTML = `<span></span><span class="muted">${s.tempo} bpm · ${when}</span>`;
    open.firstChild.textContent = s.title + (s.id === songId ? '  ·  open' : '');
    open.onclick = () => load(s.id);
    const del = document.createElement('button'); del.className = 'del'; del.textContent = 'delete';
    del.setAttribute('aria-label', 'Delete ' + s.title);
    del.onclick = async () => {
      if (!confirm(`Delete “${s.title}”? Its tape tracks and pattern go with it.`)) return;
      await m('DeleteSong', {id: s.id});
      if (s.id === songId) { songId = null; remember(null); }
      refresh();
    };
    li.append(open, del); list.append(li);
  }
  if (!songs.length) list.innerHTML = '<li><span class="muted" style="padding:12px 2px">No saved songs yet.</span></li>';
}

async function save() {
  if (!user || busy) return;
  busy = true; saveBtn.disabled = true; say('saving…');
  try {
    const s = T().songState();
    const vars = {title: s.title, tempo: s.tempo, settings: s.settings};
    if (songId) {
      const r = await m('UpdateSong', Object.assign({id: songId}, vars));
      if (!r.song_update) songId = null;   // deleted elsewhere: save it as a new song
    }
    if (!songId) songId = (await m('CreateSong', vars)).song_insert.id;
    remember(songId);
    for (const p of s.patterns) await m('SavePattern', {songId, kind: p.kind, data: p.data});
    for (const r of s.recordings) {
      if (r.events.length && r.instrument) {
        await m('SaveRecording', {songId, track: r.track, instrument: r.instrument, ppq: r.ppq, lengthTicks: r.lengthTicks, events: r.events});
      } else await m('DeleteRecording', {songId, track: r.track});
    }
    T().saved(); say('saved'); refresh();
  } catch (e) { say('could not save: ' + (e.message || e)); }
  busy = false; saveBtn.disabled = !user;
}

async function load(id) {
  if (T().dirty && !confirm('Open this song? Unsaved changes to the current one will be lost.')) return;
  say('opening…');
  try {
    const {song} = await q('GetSong', {id});
    if (!song) { say('that song is gone'); remember(null); return refresh(); }
    T().loadSong(song); songId = song.id; remember(songId);
    $('#songTitle').value = song.title; say(''); refresh();
  } catch (e) { say('could not open: ' + (e.message || e)); }
}

saveBtn.onclick = save;
$('#newSong').onclick = () => {
  if (T().dirty && !confirm('Start a new song? Unsaved changes will be lost.')) return;
  T().newSong(); songId = null; remember(null); $('#songTitle').value = 'untitled'; say(''); refresh();
};
window.addEventListener('tombola:sheet', () => { if (user) refresh(); });

(async () => {
  try {
    const cfg = await config();
    const [fa, fauth, fdc] = await Promise.all([import(SDK + 'firebase-app.js'), import(SDK + 'firebase-auth.js'), import(SDK + 'firebase-data-connect.js')]);
    A = fauth; D = fdc;
    const app = fa.initializeApp(cfg);
    auth = A.getAuth(app);
    dc = D.getDataConnect(app, CONNECTOR);
    if (LOCAL) {
      A.connectAuthEmulator(auth, 'http://127.0.0.1:9099', {disableWarnings: true});
      D.connectDataConnectEmulator(dc, '127.0.0.1', 9399);
    }
    renderAcct();
    A.onAuthStateChanged(auth, async u => {
      user = u; renderAcct();
      if (!u) { songId = null; list.innerHTML = ''; return; }
      try {
        await m('UpsertMe', {displayName: u.displayName || null});
        const last = recalled();
        if (last && !T().dirty) await load(last); else await refresh();
      } catch (e) { say(e.message || String(e)); }
    });
  } catch (e) {
    acct.innerHTML = '<span class="muted"></span>';
    acct.firstChild.textContent = 'Cloud saving is unavailable: ' + (e.message || e);
  }
})();
