// Offline renderer: headless Chromium draws each frame, POSTs raw RGBA to this server, piped into ffmpeg.
import { createRequire } from 'node:module';
const { chromium } = createRequire(import.meta.url)('playwright');
import http from 'node:http';
import fs from 'node:fs';
import path from 'node:path';
import { spawn } from 'node:child_process';

const [,, W = 3840, H = 2160, FPS = 60, SECONDS = 15, OUT = 'out', START = 0, COUNT] = process.argv;
const N = FPS * SECONDS, first = +START, last = COUNT ? Math.min(N, first + +COUNT) : N;
const html = fs.readFileSync(path.resolve('visual.html'));
fs.mkdirSync(OUT, { recursive: true });

const ff = spawn('ffmpeg', ['-y', '-hide_banner', '-loglevel', 'error',
  '-f', 'rawvideo', '-pix_fmt', 'rgba', '-s', `${W}x${H}`, '-r', `${FPS}`, '-i', '-',
  '-vf', 'vflip', '-c:v', 'ffv1', '-level', '3', '-pix_fmt', 'bgr0', '-slices', '16', '-g', '1', '-threads', '2',
  process.env.OUTFILE || path.join(OUT, `master_${String(first).padStart(4, '0')}.mkv`)], { stdio: ['pipe', 'inherit', 'inherit'] });

let pending = null;
const server = http.createServer((req, res) => {
  if (req.method === 'GET') { res.writeHead(200, { 'content-type': 'text/html' }); return res.end(html); }
  const chunks = [];
  req.on('data', c => chunks.push(c));
  req.on('end', () => {
    const buf = Buffer.concat(chunks);
    if (!ff.stdin.write(buf)) ff.stdin.once('drain', () => res.end('ok')); else res.end('ok');
  });
}).listen(0);
const port = server.address().port;

const browser = await chromium.launch({ args: ['--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--ignore-gpu-blocklist'] });
const page = await browser.newPage();
page.on('console', m => console.log('[page]', m.text()));
page.on('pageerror', e => console.error('[pageerror]', e.message));
await page.goto(`http://127.0.0.1:${port}/?offline&w=${W}&h=${H}`);
await page.evaluate(() => window.renderReady);
const t0 = Date.now();
const list = process.env.FRAMES ? process.env.FRAMES.split(',').map(Number) : Array.from({ length: last - first }, (_, k) => first + k);
for (const i of list) {
  await page.evaluate(([p, u]) => window.renderFrame(p, u), [i / N, `http://127.0.0.1:${port}/f`]);
  const done = list.indexOf(i) + 1, el = (Date.now() - t0) / 1000;
  if (done % 10 === 0 || done === 1) console.log(`frame ${i} (${done}/${list.length}) ${(el / done).toFixed(2)}s/f eta ${((list.length - done) * el / done / 60).toFixed(1)}min`);
}
await browser.close(); server.close();
ff.stdin.end();
await new Promise(r => ff.on('close', r));
console.log('done', first, last);
