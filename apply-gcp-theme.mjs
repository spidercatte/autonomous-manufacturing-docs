// Run after Archify deliver to keep the interactive diagram self-contained.
import { readFileSync, writeFileSync } from 'node:fs';
import { fileURLToPath } from 'node:url';
import { dirname, join } from 'node:path';

const directory = dirname(fileURLToPath(import.meta.url));
const css = readFileSync(join(directory, 'gcp-color-theme.css'), 'utf8').trim();
const style = `<style id="gcp-color-theme">\n${css}\n</style>`;
for (const [file, title] of [
  ['gcp-deployment.html', 'Target Google Cloud Architecture Diagram'],
  ['local-tech-stack.html', 'Local Proactive Tech Stack Diagram'],
]) {
  const htmlPath = join(directory, file);
  let html = readFileSync(htmlPath, 'utf8');
  if (!html.includes(`<title>${title}</title>`)) {
    throw new Error(`${file} was not generated from the expected Archify source.`);
  }
  if (html.includes('<style id="gcp-color-theme">')) {
    html = html.replace(/<style id="gcp-color-theme">[\s\S]*?<\/style>/, style);
  } else {
    html = html.replace('</head>', `${style}\n</head>`);
  }
  writeFileSync(htmlPath, html);
}
