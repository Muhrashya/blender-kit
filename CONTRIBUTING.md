# Contributing

## Add a skill
1. Create `skills/<name>/SKILL.md` with frontmatter `name` (equal to the folder), `description` starting with "Use when" (max 420 chars, include trigger words in English and Indonesian when relevant).
2. Use the 7 sections: Requires, Inputs, Steps, Hard rules, Done when, On fail, Next. Keep the file under 140 lines; move detail to `references/`.
3. Reference files with relative paths inside the skill (`references/x.md`); project-level files as `docs/blender/...` (they must exist in `skills/blender-setup/templates/` or be `engine.md` / `style.md`).
4. Add the intent row to `skills/blender/references/intents.md` and routes to `routes.md`.
5. Run `npm run check`.

## Add an engine profile
Copy `skills/blender-setup/templates/engines/_template.md`; fill with [DOC]/[RECALLED]/UNVERIFIED labels; keep `status: SEED` until every Limits row is [DOC]. Run `/blender-setup engine <name>` to research from official docs.

## Add a style
Copy a file in `templates/styles/`; keep the same table layout.

## Rules for content
No invented numbers. Every number is computed, quoted from a source, or labeled [START]/[RECALLED]. No third-party images or copyrighted text.
