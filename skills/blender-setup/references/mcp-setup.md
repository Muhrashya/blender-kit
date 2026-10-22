# Blender MCP setup (the bridge that lets the agent run Python in Blender)

Source: the BlenderMCP project (addon + MCP server). Tool names differ by version: read the tool list your agent shows; only two capabilities are required: (1) run Python in Blender, (2) viewport screenshot.

| Step | Action |
|---|---|
| 1 | Install `uv` (Python tool runner) |
| 2 | In Blender: Edit > Preferences > Add-ons > Install, choose the BlenderMCP `addon.py`, enable it |
| 3 | Blender 3D view: press `N`, open the BlenderMCP tab, click Connect (start the server) |
| 4 | Register the MCP server in your agent (table below) |
| 5 | Restart the agent. Test: run `scene_info.py` |

| Agent | Register |
|---|---|
| Claude Code | `claude mcp add blender -- uvx blender-mcp` |
| Cursor | `.cursor/mcp.json`: `{"mcpServers":{"blender":{"command":"uvx","args":["blender-mcp"]}}}` |
| Claude Desktop | `claude_desktop_config.json`: same `mcpServers` block |
| Codex | `~/.codex/config.toml`: `[mcp_servers.blender]` with `command = "uvx"` and `args = ["blender-mcp"]` (check your Codex version) |
| Antigravity | its MCP settings: command `uvx`, args `blender-mcp` (check the app) |
| Windows | if `uvx` is not found, use command `cmd` with args `["/c","uvx","blender-mcp"]` |
| ChatGPT | cannot reach a local Blender without extra tunnelling: use SCRIPT MODE (ground-rules.md section 7) |

Security: the "run Python" tool executes any code the agent writes. Save the .blend first. Do not run on files you cannot lose.
