# Asset index + log

One row per asset. The router reads this to find the ACTIVE asset (Status = IN-PROGRESS or BLOCKED).
Per-asset detail lives in blender-out/<asset>/state.md. blender-qa writes the verdict. Never edit a verdict by hand.

| Asset | Mode | Role | Stage | Status (IN-PROGRESS / BLOCKED / SHIP / NO-SHIP) | Tris / Budget | Engine | Date | State file |
|---|---|---|---|---|---|---|---|---|
