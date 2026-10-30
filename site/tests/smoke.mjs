// Browser smoke test for the built site (node site/tests/smoke.mjs [build/site] [shots-dir]).
// Serves the build locally and opens every page at desktop and phone width in light and dark.
// Fails on console errors, uncaught exceptions, any request that leaves this origin (the site is
// meant to be self-contained), horizontal page scroll, or a 3D scene that neither renders nor
// shows its still fallback.
import { createServer } from 'node:http';
import { readFile, readdir, mkdir } from 'node:fs/promises';
import { extname, join, relative, resolve } from 'node:path';
import { createRequire } from 'node:module';

// require() honours NODE_PATH, so CI can point at a throwaway Playwright install.
const { chromium } = createRequire(import.meta.url)('playwright');

const root = resolve(process.argv[2] ?? 'build/site');
const shots = resolve(process.argv[3] ?? 'build/site-shots');
const TYPES = { '.html': 'text/html', '.js': 'text/javascript', '.mjs': 'text/javascript', '.css': 'text/css',
  '.json': 'application/json', '.svg': 'image/svg+xml', '.png': 'image/png', '.webp': 'image/webp', '.jpg': 'image/jpeg',
  '.woff2': 'font/woff2', '.woff': 'font/woff', '.ttf': 'font/ttf', '.pdf': 'application/pdf', '.tex': 'text/plain',
  '.glb': 'model/gltf-binary' };
const VIEWS = [
  { name: 'desktop', viewport: { width: 1440, height: 900 } },
  { name: 'phone', viewport: { width: 390, height: 844 }, isMobile: true, hasTouch: true },
];

async function pages(dir) {
  const out = [];
  for (const entry of await readdir(dir, { withFileTypes: true })) {
    const path = join(dir, entry.name);
    if (entry.isDirectory()) out.push(...await pages(path));
    else if (entry.name.endsWith('.html')) out.push(relative(root, path));
  }
  return out.sort();
}

const server = createServer(async (req, res) => {
  const path = join(root, decodeURIComponent(new URL(req.url, 'http://x').pathname));
  try {
    const body = await readFile(path.endsWith('/') ? join(path, 'index.html') : path);
    res.writeHead(200, { 'content-type': TYPES[extname(path)] ?? 'application/octet-stream' }).end(body);
  } catch {
    res.writeHead(404).end();
  }
}).listen(0, '127.0.0.1');
await new Promise(r => server.once('listening', r));
const origin = `http://127.0.0.1:${server.address().port}`;

const browser = await chromium.launch({ args: ['--use-gl=swiftshader', '--enable-unsafe-swiftshader'] });
const problems = [];
await mkdir(shots, { recursive: true });
for (const page of (await pages(root)).filter(p => !p.startsWith('visualizations/'))) {
  for (const view of VIEWS) {
    for (const scheme of ['light', 'dark']) {
      const context = await browser.newContext({ ...view, colorScheme: scheme, reducedMotion: 'reduce' });
      const tab = await context.newPage();
      const tag = `${page} ${view.name} ${scheme}`;
      tab.on('console', m => { if (m.type() === 'error') problems.push(`${tag}: console error: ${m.text()}`); });
      tab.on('pageerror', e => problems.push(`${tag}: uncaught: ${e.message}`));
      tab.on('request', r => { if (!r.url().startsWith(origin) && !r.url().startsWith('data:') && !r.url().startsWith('blob:')) problems.push(`${tag}: external request ${r.url()}`); });
      tab.on('response', r => { if (r.status() >= 400) problems.push(`${tag}: ${r.status()} ${r.url().slice(origin.length)}`); });
      await tab.goto(`${origin}/${page}`, { waitUntil: 'networkidle' });
      await tab.waitForTimeout(800);
      const state = await tab.evaluate(() => ({
        overflow: document.documentElement.scrollWidth - window.innerWidth,
        scenes: [...document.querySelectorAll('[data-scene]')].map(el => ({
          id: el.dataset.scene,
          ok: el.dataset.state === 'running' || el.dataset.state === 'fallback',
          state: el.dataset.state ?? 'none',
        })),
      }));
      if (state.overflow > 1) problems.push(`${tag}: page scrolls sideways by ${state.overflow}px`);
      for (const s of state.scenes) if (!s.ok) problems.push(`${tag}: scene ${s.id} state ${s.state}`);
      await tab.screenshot({ path: join(shots, `${page.replace(/[/.]/g, '_')}-${view.name}-${scheme}.png`), fullPage: false });
      await context.close();
    }
  }
}
await browser.close();
server.close();
console.log(JSON.stringify({ pages: (await pages(root)).length, problems }, null, 2));
process.exit(problems.length ? 1 : 0);
