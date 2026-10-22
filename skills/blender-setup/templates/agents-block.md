<!-- blender-kit:start -->
## Blender Kit

This project uses blender-kit (Agent Skills for Blender). Entry point: `/blender`. First-time setup: `/blender-setup`.

Always, for any Blender task:
1. Read `docs/blender/config.md` (budgets, naming, active engine and style) and `docs/blender/ground-rules.md`.
2. Active engine profile: `docs/blender/engine.md`. Active style: `docs/blender/style.md`. Never invent engine limits; unknown values are labeled UNVERIFIED.
3. Drive Blender through the Blender MCP (run Python + viewport screenshot). If it is not connected, use script mode (ground-rules.md section 7).
4. One stage per turn. Run the stage audit from `docs/blender/scripts/`. Never continue past a failed audit. Never export without a SHIP verdict from blender-qa.
5. Outputs go to `blender-out/<asset>/`. Log verdicts in `docs/blender/assets.md`.
<!-- blender-kit:end -->
