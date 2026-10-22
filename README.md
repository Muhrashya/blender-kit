# blender-kit

Agent skills for Blender 3D game asset pipelines: clean topology, triangle budget enforcement, rig-ready meshes, retopology, UV unwrapping, PBR materials, rigging, animation, cinematic cameras, and game visual effects (realistic, stylized, low-poly, voxel). Engine-agnostic via swappable profile configurations.

Contains 21 specialized skills coordinated through a single router command: `/blender`.

Supported engines: generic-gltf, roblox, unity, unreal, godot, web-three.
Supported art styles: voxel, lowpoly, stylized, realistic.

---

## Installation

A complete installation consists of four steps: system prerequisites, skill installation, BlenderMCP addon configuration, and agent registration.

### 1. Prerequisites

- Blender 4.x installed and accessible.
- Node.js (v18+) for running `npx`.
- Python tool runner `uv`:
  - macOS/Linux: `curl -LsSf https://astral.sh/uv/install.sh | sh`
  - Windows (PowerShell): `powershell -c "irm https://astral.sh/uv/install.ps1 | iex"`

### 2. Install Skills

Install the skill package into your coding agent:

| Environment | Command |
|---|---|
| Project directory (default) | `npx skills@latest add Muhrashya/blender-kit` |
| Global install | `npx skills@latest add Muhrashya/blender-kit -g` |
| Specific agent only | `npx skills@latest add Muhrashya/blender-kit -a claude-code` (or `cursor`, `codex`, `antigravity`) |
| Select skills only | `npx skills@latest add Muhrashya/blender-kit --skill blender --skill blender-setup --skill blender-topology` |
| Local repository copy | `npx skills add ./blender-kit` |
| Claude Code plugin | `/plugin marketplace add Muhrashya/blender-kit` |
| ChatGPT / Web LLM | Run `npm run bundle:chatgpt`, then use `dist/chatgpt-instructions.md` and `dist/chatgpt-knowledge.md` |

### 3. BlenderMCP Addon Setup

BlenderMCP acts as the execution bridge between your AI agent and the live Blender session:

1. Locate `addon.py` from the BlenderMCP project.
2. In Blender: go to **Edit > Preferences > Add-ons > Install**, select `addon.py`, and enable the addon.
3. In the 3D Viewport sidebar (press `N`), select the **BlenderMCP** tab and click **Connect** to start the local bridge server.

### 4. Register MCP Server in Your Agent

Add the `blender-mcp` tool runner to your agent's configuration:

- **Claude Code**:
  ```bash
  claude mcp add blender -- uvx blender-mcp
  ```

- **Cursor** (`.cursor/mcp.json`):
  ```json
  {
    "mcpServers": {
      "blender": {
        "command": "uvx",
        "args": ["blender-mcp"]
      }
    }
  }
  ```

- **Claude Desktop** (`claude_desktop_config.json`):
  ```json
  {
    "mcpServers": {
      "blender": {
        "command": "uvx",
        "args": ["blender-mcp"]
      }
    }
  }
  ```

- **Codex** (`~/.codex/config.toml`):
  ```toml
  [mcp_servers.blender]
  command = "uvx"
  args = ["blender-mcp"]
  ```

- **Antigravity**:
  Configure an MCP server with command `uvx` and arguments `blender-mcp`.

> Note for Windows users: If `uvx` is not directly resolved by your agent shell, set the command to `cmd` with arguments `["/c", "uvx", "blender-mcp"]`. If BlenderMCP is unavailable, skills operate in headless script-generating mode.

---

## How to Use

The kit uses an automated multi-stage pipeline where `/blender` classifies user input, loads the required skill, enforces gate audits, and tracks asset progress.

### Standard Workflow

1. **Initialize Project (`/blender-setup`)**:
   Run this once when starting a new project. It creates `docs/blender/`, configures target engine profile (`generic-gltf`, `roblox`, `unity`, `unreal`, `godot`, `web-three`), art style, and validates the BlenderMCP connection.

2. **Generate or Edit Assets (`/blender <mode>`)**:
   Invoke `/blender` with the desired asset mode and parameters. The router sets up `blender-out/<asset>/state.md` and proceeds through the pipeline stages (reference, modeling, topology, UV/bake, materials, rigging, animation).

3. **Handle Interruptions and Technical Queries**:
   You can ask technical questions or request repairs at any point (such as `/blender fix`). The router pauses the active stage, runs the requested action or diagnosis, and seamlessly resumes previous work.

4. **Verify and Export (`/blender qa` and `/blender export`)**:
   Run quality assurance to verify mesh topology, non-manifold geometry, texel density, and bone count against engine limits. Once approved, the asset is exported to game-ready FBX or glTF formats.

### Common Commands

| Target / Task | Example Command |
|---|---|
| Initialize project | `/blender-setup` |
| Low-poly prop from image | `/blender prop "WoodCrate" ref=crate.png role=prop-small style=lowpoly` |
| Animated character | `/blender char "Knight" role=char-npc rig anim=idle,walk` |
| Character hands / gloves | `/blender hands "KnightHand" style=stylized` |
| Repair topology / ngons | `/blender fix` |
| Convert sculpt to game mesh | `/blender retopo "HeroSculpt" tris=5000` |
| Mesh-based visual effect | `/blender fx "SlashArc" fx=lowpoly` |
| Cinematic shot sequence | `/blender cam "HeroReveal" shots=3` |
| Quality audit | `/blender qa` |
| Game engine export | `/blender export` |

---

## Skills Reference

The 21 skills are organized into 7 functional architectural layers:

### 1. Intelligence
| Skill | Trigger / Command | Description |
|---|---|---|
| `blender` | `/blender` | Master router and state manager; classifies intent, coordinates skill chains, and tracks asset state. |
| `blender-setup` | `/blender-setup` | Initializes workspace configuration, engine limits, art style rules, and verifies MCP connection. |
| `blender-diagnose` | `/blender diagnose` | Diagnoses shading artifacts, normal orientation, mesh errors, and answers 3D technical questions. |

### 2. Geometry
| Skill | Trigger / Command | Description |
|---|---|---|
| `blender-ref` | `/blender ref` | Analyzes reference images, extracting measured proportions and silhouette bounds prior to modeling. |
| `blender-model` | `/blender model` | Constructs base blockouts, modular environment pieces, and characters with clean transform origins. |
| `blender-topology` | `/blender topology` | Enforces quad flow, loop continuity, deformation zones, and triangle budgets. |
| `blender-topology-fix` | `/blender fix` | Detects and resolves ngons, non-planar quads, joint poles, and asymmetrical density. |
| `blender-retopo` | `/blender retopo` | Converts high-poly sculpts, scans, or dense meshes into clean low-poly game-ready models. |
| `blender-hands` | `/blender hands` | Builds and refines anatomical hands, fingers, and claws with deformation-ready joint loops. |

### 3. Surface
| Skill | Trigger / Command | Description |
|---|---|---|
| `blender-uv-bake` | `/blender uv` | Performs UV unwrapping, island packing, texel density equalization, and normal/AO map baking. |
| `blender-material` | `/blender material` | Authors export-compliant Principled BSDF materials, palette textures, emission, and transparency settings. |

### 4. Motion
| Skill | Trigger / Command | Description |
|---|---|---|
| `blender-rig` | `/blender rig` | Generates armatures, bone hierarchies, skin weight distributions, and deform-only export skeletons. |
| `blender-animate` | `/blender anim` | Authors clean keyframed clips (idle, locomotion, combat actions) with loop points and NLA management. |

### 5. Effects
| Skill | Trigger / Command | Description |
|---|---|---|
| `blender-vfx` | `/blender fx` | Master VFX orchestrator; generates multi-layer effect specifications for games across styles. |
| `blender-vfx-mesh` | `vfx-mesh` | Generates mesh-based effects (slashes, cones, shockwaves, shields) with scrolling UV layouts. |
| `blender-vfx-flipbook` | `vfx-flipbook` | Renders simulation sequences and particle bursts into power-of-two transparent sprite sheets. |
| `blender-vfx-texture` | `vfx-texture` | Bakes channel-packed mask textures, noise fields, gradient ramps, and dissolve patterns. |
| `blender-vfx-sim` | `vfx-sim` | Simulates smoke, fire, fluids, and rigid body fractures, baking output to engine-compatible assets. |

### 6. Cinematics
| Skill | Trigger / Command | Description |
|---|---|---|
| `blender-camera` | `/blender cam` | Creates shot compositions, turntables, cinematic reveals, and animated camera movements. |

### 7. Delivery
| Skill | Trigger / Command | Description |
|---|---|---|
| `blender-qa` | `/blender qa` | Executes automated compliance audits against target engine limits to grant SHIP or NO-SHIP status. |
| `blender-export` | `/blender export` | Packages verified models into FBX or glTF files with applied modifiers, transforms, and textures. |

---

## Configuration and Rigor

Pipeline behavior is configured via `docs/blender/config.md`:

- **Rigor Levels**:
  - `strict`: Executes one pipeline stage per interaction turn, requiring approval before proceeding.
  - `balanced`: Automatically chains sequential low-risk stages that pass gate audits.
  - `flex`: Chains execution continuously until an audit check fails.
- **Waivers**: Non-critical warnings can be explicitly waived (recorded in `state.md`). Mandatory safety checks (saving `.blend` files, file existence validation, honest reporting) cannot be bypassed.
- **Visual Build Guide**: `docs/blender/reference/build-guide.md` details asset cards and pipeline diagrams. Diagrams can be regenerated using `npm run figures`.

---

## Project Architecture and Documentation

Detailed technical documentation is available in `docs/`:

- `docs/ARCHITECTURE.md`: Pipeline dependency graph, stage contracts, invalidation rules, and failure routes.
- `docs/EXAMPLES.md`: End-to-end walkthroughs covering prop, character, and VFX creation.
- `docs/GROUNDING.md`: Anti-hallucination protocols, script verification requirements, and evidence labels (`[MEASURED]`, `[DOC]`, `[RECALLED]`).

---

## Limitations and Compatibility

- **Blender Version**: Designed and tested for Blender 4.x. Scripts dynamically inspect version properties rather than hardcoding internal names.
- **Audit Scripts**: Audits run via Python within Blender. Mocked test cases are documented in `evals/cases.md`.
- **Engine Profiles**: Profiles in `engines/*.md` provide starter baseline budgets. Unverified constraints are flagged for verification against official engine documentation.
- **Camera Taxonomy**: Follows standard cinematic terminology with kit-calibrated speed and timing presets.

---

## Development

Run development tasks via npm:

```bash
npm run validate         # Lint all skill definition files
npm run check            # Lint skills and compile Python helper scripts
npm run bundle:chatgpt   # Build bundled documentation files for ChatGPT
npm run figures          # Regenerate architectural and visual guide figures
```

## License

MIT
