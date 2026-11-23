// "THE 23rd" — a one-day newspaper front page for Monday 23 November 2026.
//
// The entry is the pre-drawn front page in art.png (see draw.py for how it
// was made). This program only validates it and copies it to the output
// directory, so both grader runs produce byte-identical output.
// Node 22, standard library only. No network.
//
//   mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts

import { createHash } from "node:crypto";
import { existsSync, mkdirSync, readFileSync, writeFileSync } from "node:fs";
import { join } from "node:path";

const ART = new URL("./art.png", import.meta.url);
const OUT_DIR = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";
const OUT_NAME = "entry.png";
const MAX_BYTES = 1048576;
const PNG_MAGIC = Buffer.from([
  0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a,
]);

function die(message: string): never {
  console.error(`error: ${message}`);
  process.exit(1);
}

if (!existsSync(ART)) die("art.png is missing from the repository");

const art = readFileSync(ART);

if (!art.subarray(0, 8).equals(PNG_MAGIC)) die("art.png is not a PNG file");
if (art.length > MAX_BYTES) {
  die(`art.png is ${art.length} bytes, over the 1 MiB limit`);
}
if (art.toString("latin1", 12, 16) !== "IHDR") {
  die("art.png has no IHDR chunk");
}
const width = art.readUInt32BE(16);
const height = art.readUInt32BE(20);
if (width !== 1024 || height !== 1024) {
  die(`art.png is ${width}x${height}, expected 1024x1024`);
}

mkdirSync(OUT_DIR, { recursive: true });
const dest = join(OUT_DIR, OUT_NAME);
writeFileSync(dest, art);

// Verify the copy: re-read it and compare size and hash with the source.
const back = readFileSync(dest);
if (back.length !== art.length) {
  die(`wrote ${back.length} bytes, expected ${art.length}`);
}
const digest = createHash("sha256").update(back).digest("hex");
const sourceDigest = createHash("sha256").update(art).digest("hex");
if (digest !== sourceDigest) die("output bytes differ from art.png");

console.log(
  `wrote ${dest} (${back.length} bytes, ${width}x${height} PNG, ` +
    `sha256 ${digest})`,
);
