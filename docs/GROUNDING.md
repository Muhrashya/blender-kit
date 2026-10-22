# Grounding (summary)

The full rules are in `skills/blender-setup/templates/ground-rules.md` (copied to `docs/blender/ground-rules.md` in your project).
In one table:
| Never | Instead |
|---|---|
| invent engine limits | read engine.md; unknown = UNVERIFIED |
| guess an operator argument | introspect `get_rna_type().properties` |
| estimate a triangle count | run audit_mesh.py |
| claim "done" | show the audit JSON numbers |
| trust a remembered MCP tool name | read the tool list |
| lose the plan in a long chat | read/write state.md every turn |
