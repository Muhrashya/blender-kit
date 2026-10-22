// Builds two files for ChatGPT (no skills folder, no slash): dist/chatgpt-instructions.md + dist/chatgpt-knowledge.md
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const skillsDir = path.join(root, "skills");
const dist = path.join(root, "dist");
const LIMIT = Number((process.argv.find((a) => a.startsWith("--limit=")) || "--limit=8000").split("=")[1]); // instructions limit is UNVERIFIED; adjust
fs.mkdirSync(dist, { recursive: true });

const strip = (t) => t.replace(/^---\n[\s\S]*?\n---\n/, "");
const read = (...p) => fs.readFileSync(path.join(skillsDir, ...p), "utf8");
function walk(d, out = []) { for (const f of fs.readdirSync(d).sort()) { const p = path.join(d, f); fs.statSync(p).isDirectory() ? walk(p, out) : out.push(p); } return out; }

const instructions = [
  "# Blender Kit (ChatGPT mode, SCRIPT MODE)",
  "You help build game-ready Blender assets. You cannot run Blender: for every stage write ONE self-contained Python script, tell the user to paste it into Blender > Scripting, and ask them to paste the printed output back. All rules below and in the Knowledge file apply.",
  "Rules: classify each message with the intent table, run one stage per turn, report in the fixed format, never invent engine limits (use labels [MEASURED] [DOC] [RECALLED] [START] [ASSUMED] [UNVERIFIED]), measure with the audit scripts in Knowledge, never skip a failed audit.",
  strip(read("blender", "SKILL.md")),
  "Full ground rules, rigor modes and waivers: see FILE: blender-setup/templates/ground-rules.md in the Knowledge file (read it first in every session).",
].join("\n\n");
fs.writeFileSync(path.join(dist, "chatgpt-instructions.md"), instructions);
if (instructions.length > LIMIT) console.warn(`WARN instructions are ${instructions.length} chars (> ${LIMIT}); move the ground rules into the Knowledge file or raise --limit`);

let knowledge = "# Blender Kit knowledge\n\n";
for (const f of walk(skillsDir).filter((p) => /\.(md|py)$/.test(p))) {
  const rel = path.relative(skillsDir, f);
  const body = f.endsWith(".md") ? strip(fs.readFileSync(f, "utf8")) : "```python\n" + fs.readFileSync(f, "utf8") + "\n```";
  knowledge += `\n\n<!-- FILE: ${rel} -->\n## FILE: ${rel}\n\n${body}\n`;
}
fs.writeFileSync(path.join(dist, "chatgpt-knowledge.md"), knowledge);
console.log(`instructions: ${instructions.length} chars | knowledge: ${knowledge.length} chars`);
