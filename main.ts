// news-image-20261120 entry program (Node 22, standard library only).
//
// The entry image is entry.png beside this file: a one-day world news
// poster for Friday 20 November 2026, drawn at build time by
// draw_image.py. At run time there is no network, so this program only
// validates the image bytes and copies them to the output directory.
// Outside the grader's container, MAKEFUN_OUTPUT_DIR stands in for /output:
//   mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts

import { mkdirSync, readFileSync, writeFileSync } from 'node:fs';
import { join } from 'node:path';
import { fileURLToPath } from 'node:url';

const MAX_BYTES = 1048576; // 1 MiB gate limit
const MAX_DIM = 1024; // 1024 by 1024 gate limit

function pngSize(bytes) {
  // PNG signature, then IHDR width/height as big-endian uint32 at 16/20.
  const sig = [0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a];
  if (bytes.length < 24 || !sig.every((b, i) => bytes[i] === b)) return null;
  return { width: bytes.readUInt32BE(16), height: bytes.readUInt32BE(20) };
}

const here = fileURLToPath(new URL('.', import.meta.url));
const bytes = readFileSync(join(here, 'entry.png'));

if (bytes.length > MAX_BYTES) {
  throw new Error(`entry.png is ${bytes.length} bytes, over the 1 MiB gate limit`);
}
const size = pngSize(bytes);
if (size === null) {
  throw new Error('entry.png is not a PNG (bad signature)');
}
if (size.width > MAX_DIM || size.height > MAX_DIM) {
  throw new Error(`entry.png is ${size.width}x${size.height}, over ${MAX_DIM}x${MAX_DIM}`);
}

const outDir = process.env.MAKEFUN_OUTPUT_DIR || '/output';
mkdirSync(outDir, { recursive: true });
writeFileSync(join(outDir, 'entry.png'), bytes);
console.log(`entry.png ${size.width}x${size.height} ${bytes.length} bytes -> ${outDir}/entry.png`);
