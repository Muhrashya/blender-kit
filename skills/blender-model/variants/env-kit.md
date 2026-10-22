# Variant: environment kit (modular pieces)

| Topic | Rule |
|---|---|
| Grid | choose ONE kit unit (for example 1 m) and write it in config.md Project overrides; every piece dimension is a multiple |
| Pivot | corner or bottom center, same convention for all pieces |
| Snap | boundary vertices land exactly on the grid; neighbors share identical edge vertex positions (no gaps) |
| Hidden faces | delete faces that touch another piece; keep the visible side only |
| Trim | repeated details use a shared trim texture, not unique geometry |
| Variants | give each piece 2 or 3 variants only if the brief asks |
| Pitfalls | pieces off-grid by 0.001, mixed pivot conventions, unique textures per piece |
| Budget | role env-module from config.md per piece |
