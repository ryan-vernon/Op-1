// Minimal static server for Firebase App Hosting (Cloud Run): serves the built page in public/.
// The Firebase web app config ships as public/src/webapp-config.json.
const http = require('http'), fs = require('fs'), path = require('path');
const ROOT = path.join(__dirname, 'public');
const TYPES = {'.html': 'text/html; charset=utf-8', '.js': 'text/javascript; charset=utf-8', '.json': 'application/json',
  '.css': 'text/css; charset=utf-8', '.png': 'image/png', '.svg': 'image/svg+xml', '.ico': 'image/x-icon', '.webmanifest': 'application/manifest+json'};

http.createServer((req, res) => {
  const url = new URL(req.url, 'http://x');
  let file = path.normalize(path.join(ROOT, decodeURIComponent(url.pathname)));
  if (file !== ROOT && !file.startsWith(ROOT + path.sep)) { res.writeHead(403); return res.end(); }
  if (url.pathname.endsWith('/')) file = path.join(file, 'index.html');
  fs.readFile(file, (err, body) => {
    if (err) { res.writeHead(404, {'Content-Type': 'text/plain'}); return res.end('not found'); }
    res.writeHead(200, {'Content-Type': TYPES[path.extname(file)] || 'application/octet-stream', 'Cache-Control': 'no-cache'});
    res.end(body);
  });
}).listen(process.env.PORT || 8080);
