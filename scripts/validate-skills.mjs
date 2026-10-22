// Lints every skill: frontmatter, sections, size, references, cross-skill coupling, engine profiles.
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const skillsDir = path.join(root, "skills");
const templates = path.join(skillsDir, "blender-setup", "templates");
const REQUIRED = ["## Requires", "## Inputs", "## Steps", "## Hard rules", "## Done when", "## On fail", "## Next"];
const ENGINE_REQUIRED = ["## Import", "## Coordinates and scale", "## Limits", "## Mesh rules", "## Naming", "## Rig", "## Animation", "## Materials", "## VFX", "## Camera", "## Export call", "## Import test"];
const RUNTIME_ONLY = new Set(["engine.md", "style.md"]);
const MAX_LINES = 140, MAX_DESC = 420;

const errors = [], warnings = [];
const err = (m) => errors.push(m);
const warn = (m) => warnings.push(m);

function frontmatter(text) {
  const m = text.match(/^---\n([\s\S]*?)\n---\n/);
  if (!m) return null;
  const o = {};
  for (const line of m[1].split("\n")) {
    const i = line.indexOf(":");
    if (i > 0) o[line.slice(0, i).trim()] = line.slice(i + 1).trim();
  }
  return o;
}
const exists = (p) => fs.existsSync(p);

const skillNames = fs.readdirSync(skillsDir).filter((d) => fs.statSync(path.join(skillsDir, d)).isDirectory());
for (const name of skillNames) {
  const dir = path.join(skillsDir, name);
  const file = path.join(dir, "SKILL.md");
  if (!exists(file)) { err(`${name}: SKILL.md missing`); continue; }
  const text = fs.readFileSync(file, "utf8");
  const fm = frontmatter(text);
  if (!fm) { err(`${name}: frontmatter missing`); continue; }
  if (fm.name !== name) err(`${name}: frontmatter name "${fm.name}" != folder`);
  if (!fm.description) err(`${name}: description missing`);
  else {
    if (!/^use (when|for)/i.test(fm.description)) err(`${name}: description must start with "Use when" or "Use for"`);
    if (fm.description.length > MAX_DESC) err(`${name}: description ${fm.description.length} chars > ${MAX_DESC}`);
  }
  const lines = text.split("\n").length;
  if (lines > MAX_LINES) err(`${name}: ${lines} lines > ${MAX_LINES}`);
  for (const h of REQUIRED) if (!text.includes("\n" + h)) err(`${name}: missing section "${h}"`);
  if (text.includes("../")) err(`${name}: contains "../" (skills must be self-contained)`);

  // references inside the skill folder
  const refRe = /\b(references|variants)\/[A-Za-z0-9_./-]+\.md/g;
  for (const m of text.matchAll(refRe)) if (!exists(path.join(dir, m[0]))) err(`${name}: missing file ${m[0]}`);
  // project-level paths
  const docRe = /docs\/blender\/([A-Za-z0-9_./-]+?)(?=[\s`'")\],;:]|$)/g;
  for (const m of text.matchAll(docRe)) {
    let rel = m[1].replace(/[.]+$/, "");
    if (!rel || rel.endsWith("/")) continue;
    if (RUNTIME_ONLY.has(rel)) continue;
    if (rel.startsWith("templates/")) rel = rel.slice("templates/".length);
    if (!exists(path.join(templates, rel))) err(`${name}: docs/blender/${m[1]} has no template at blender-setup/templates/${rel}`);
  }
}

// cross-skill coupling in every md file under skills/
for (const f of fs.readdirSync(skillsDir)) {}
function walkAll(d, out = []) { for (const f of fs.readdirSync(d)) { const p = path.join(d, f); fs.statSync(p).isDirectory() ? walkAll(p, out) : out.push(p); } return out; }
for (const f of walkAll(skillsDir).filter((p) => p.endsWith(".md"))) {
  const t = fs.readFileSync(f, "utf8");
  const m = t.match(/blender-[a-z0-9-]+\/(references|variants|templates)\//);
  if (m && !f.includes(path.join("blender-setup", "templates"))) err(`${path.relative(root, f)}: cross-skill file path "${m[0]}" (use docs/blender/... instead)`);
}
// markdown image links must exist relative to the file
for (const f of walkAll(skillsDir).filter((p) => p.endsWith(".md"))) {
  const t = fs.readFileSync(f, "utf8");
  for (const m of t.matchAll(/!\[[^\]]*\]\(([^)]+)\)/g)) if (!/^https?:/.test(m[1]) && !exists(path.join(path.dirname(f), m[1]))) err(`${path.relative(root, f)}: missing image ${m[1]}`);
}
// reference files: contents for long files
function walk(d, out = []) { for (const f of fs.readdirSync(d)) { const p = path.join(d, f); fs.statSync(p).isDirectory() ? walk(p, out) : out.push(p); } return out; }
for (const f of walk(skillsDir).filter((p) => p.endsWith(".md") && !p.endsWith("SKILL.md"))) {
  const t = fs.readFileSync(f, "utf8");
  if (!f.includes(path.join("templates", "engines")) && t.split("\n").length > 100 && !/contents/i.test(t.slice(0, 600))) warn(`${path.relative(root, f)}: long file without a Contents line`);
}

// engine profiles
const engDir = path.join(templates, "engines");
for (const f of fs.readdirSync(engDir)) {
  const t = fs.readFileSync(path.join(engDir, f), "utf8");
  for (const h of ENGINE_REQUIRED) if (!t.includes(h)) err(`engines/${f}: missing "${h}"`);
  if (f !== "_template.md" && /status:\s*VERIFIED/.test(t) && /UNVERIFIED/.test(t)) err(`engines/${f}: VERIFIED but still has UNVERIFIED rows`);
}

// intents map to existing skills
const intents = fs.readFileSync(path.join(skillsDir, "blender", "references", "intents.md"), "utf8");
for (const m of intents.matchAll(/\bblender-[a-z0-9-]+\b/g)) if (!skillNames.includes(m[0])) err(`intents.md references unknown skill ${m[0]}`);
const routes = fs.readFileSync(path.join(skillsDir, "blender", "references", "routes.md"), "utf8");
for (const m of routes.matchAll(/\bblender-[a-z0-9-]+\b/g)) if (!skillNames.includes(m[0])) err(`routes.md references unknown skill ${m[0]}`);

console.log(`skills: ${skillNames.length}`);
for (const w of warnings) console.log("WARN  " + w);
for (const e of errors) console.log("ERROR " + e);
console.log(errors.length ? `FAILED (${errors.length} errors)` : "OK");
process.exit(errors.length ? 1 : 0);
