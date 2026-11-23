// Front page for Monday 23 November 2026.
// The page is drawn ahead of time by tools/render_front_page.py; this program
// checks the finished PNG and places it where the grader looks for it.
import { mkdirSync, readFileSync, writeFileSync } from 'node:fs';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';

const here = dirname(fileURLToPath(import.meta.url));
const outDir = process.env.MAKEFUN_OUTPUT_DIR || '/output';
let page;
try {
  page = readFileSync(join(here, 'entry.png'));
} catch (problem) {
  // say plainly what is missing instead of dying with a raw stack trace
  console.error(`cannot read the drawn page next to main.ts: ${problem.message}`);
  process.exit(1);
}

// A PNG opens with eight fixed bytes, then the IHDR chunk carrying width and height.
const pngStart = [0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a];
const looksLikePng = pngStart.every((byte, i) => page[i] === byte);
const wide = page.readUInt32BE(16);
const tall = page.readUInt32BE(20);

if (!looksLikePng || wide > 1024 || tall > 1024 || page.length > 1048576) {
  console.error(`front page failed its own check: ${wide}x${tall}, ${page.length} bytes`);
  process.exitCode = 1;
} else {
  mkdirSync(outDir, { recursive: true });
  writeFileSync(join(outDir, 'entry.png'), page);
  console.log(`front page written: ${wide}x${tall}, ${page.length} bytes`);
}
