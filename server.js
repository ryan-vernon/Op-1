// Minimal static server for Firebase App Hosting (Cloud Run). It serves the built page in public/
// and answers /__/firebase/init.json the way Firebase Hosting does, from the web app config that
// App Hosting injects (FIREBASE_WEBAPP_CONFIG), so src/cloud.js works the same on either host.
const http = require('http'), fs = require('fs'), path = require('path');
const ROOT = path.join(__dirname, 'public');
const TYPES = {'.html': 'text/html; charset=utf-8', '.js': 'text/javascript; charset=utf-8', '.json': 'application/json',
  '.css': 'text/css; charset=utf-8', '.png': 'image/png', '.svg': 'image/svg+xml', '.ico': 'image/x-icon'};
const config = process.env.FIREBASE_WEBAPP_CONFIG || '';

http.createServer((req, res) => {
  const url = new URL(req.url, 'http://x');
  if (url.pathname === '/__/firebase/init.json') {
    if (!config) { res.writeHead(404); return res.end('no web app config'); }
    res.writeHead(200, {'Content-Type': 'application/json', 'Cache-Control': 'no-cache'});
    return res.end(config);
  }
  let file = path.normalize(path.join(ROOT, decodeURIComponent(url.pathname)));
  if (file !== ROOT && !file.startsWith(ROOT + path.sep)) { res.writeHead(403); return res.end(); }
  if (url.pathname.endsWith('/')) file = path.join(file, 'index.html');
  fs.readFile(file, (err, body) => {
    if (err) { res.writeHead(404, {'Content-Type': 'text/plain'}); return res.end('not found'); }
    res.writeHead(200, {'Content-Type': TYPES[path.extname(file)] || 'application/octet-stream', 'Cache-Control': 'no-cache'});
    res.end(body);
  });
}).listen(process.env.PORT || 8080);
