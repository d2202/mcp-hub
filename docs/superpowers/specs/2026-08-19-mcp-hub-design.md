# mcp-hub — design spec

Date: 2026-08-19

## Problem

MCP (Model Context Protocol) lets AI coding agents connect to external tool
servers. Each agent app tracks its own list of connected MCP servers in its
own config file, own format, own location:

| Agent | Config path | Format | Key |
|---|---|---|---|
| Claude Code | `~/.claude.json` (user scope) or `.mcp.json` (project scope) | JSON | `mcpServers` |
| Codex CLI | `~/.codex/config.toml` (or project `.codex/config.toml`) | TOML | `[mcp_servers.<name>]` tables |
| Antigravity | `~/.gemini/config/mcp_config.json` (or workspace `.agents/mcp_config.json`) | JSON | `mcpServers` |

Adding one MCP server to all installed agents today means hand-editing three
files in three syntaxes, risking breakage.

## Goal

A local CLI/TUI tool, `mcp-hub`, that:

1. Detects which of the above agents are installed on the machine (config
   file present).
2. Shows a single dashboard of connected MCP servers per agent.
3. Lets the user add a server once (via catalog pick or manual entry) and
   writes it into every selected agent's config, in that agent's native
   format, safely.
4. Lets the user remove a server the same way.

Out of scope for v1: running/health-checking MCP servers themselves, editing
existing server configs (only add/remove), auto-discovering new agent types
beyond the three above (adapter interface allows adding more later).

## Architecture

### Adapter interface

Core code never special-cases an agent by name; it talks to an
`AgentAdapter` protocol:

```python
class AgentAdapter(Protocol):
    name: str                     # "claude-code" / "codex" / "antigravity"
    config_path: Path

    def detect(self) -> bool: ...
    def list_servers(self) -> list[ServerEntry]: ...
    def add_server(self, spec: ServerSpec) -> None: ...
    def remove_server(self, name: str) -> None: ...
```

Three concrete adapters ship in v1:

- `ClaudeCodeAdapter` — reads/writes `mcpServers` object in JSON, user scope
  (`~/.claude.json`) with project-scope `.mcp.json` as a secondary
  detection target if run inside a project dir.
- `CodexAdapter` — reads/writes `[mcp_servers.<name>]` TOML tables via
  `tomlkit` (preserves comments/formatting on the rest of the file).
- `AntigravityAdapter` — same shape as Claude Code but at the Antigravity
  path.

Adding a 4th agent later = one new adapter file + registration; no core
changes.

### Safe writes

Every `add_server` / `remove_server`:

1. Read + parse the existing file (or treat as empty skeleton if missing
   but agent otherwise detected via install markers — v1 only acts on
   existing files).
2. Copy original to `<path>.bak` before writing.
3. Apply the change on the parsed structure (not text patching), so
   existing entries/formatting/comments (TOML) survive.
4. Write back. On any parse/write error, abort with no partial write and
   report which agent failed; other agents in the batch still proceed
   independently.

### Catalog

`catalog.yaml`, bundled with the tool, lists known popular MCP servers:
name, description, command, args, required/optional env vars. The add
wizard can prefill from catalog or start blank ("custom").

### ServerSpec / ServerEntry

Shared internal shape both adapters and catalog produce/consume:

```python
@dataclass
class ServerSpec:
    name: str
    command: str
    args: list[str]
    env: dict[str, str]
```

## TUI (Textual)

Screens:

- **Dashboard** — table: agent name | detected (yes/no) | server count |
  config path. Selecting a row opens Server List.
- **Server List** — servers configured for that agent; flags entries that
  failed to parse (malformed config) instead of crashing.
- **Add Wizard** — step 1: pick from catalog or "custom"; step 2: fill
  name/command/args/env (prefilled if from catalog); step 3: pick target
  agents (defaults to all detected); step 4: preview diff per agent;
  confirm writes with backups.
- **Remove** — pick agent → pick server → confirm → removed with backup.

## Stack

- Python + Textual (TUI framework)
- `tomlkit` for TOML (Codex) — preserves formatting, unlike stdlib `tomllib`
  (read-only) or naive `toml` (drops comments)
- stdlib `json` for Claude Code / Antigravity
- PyYAML for catalog
- Packaging: single `pyproject.toml`, entry point `mcp-hub`

## Testing

- Adapter unit tests: given a sample config fixture, add/remove produces
  expected output, original untouched entries preserved, backup created.
- Malformed-config fixture: adapter reports error, doesn't crash, doesn't
  corrupt file further.
- No live TUI test suite in v1 (manual smoke test via `run` skill); core
  adapter + catalog logic is unit tested.

## Project layout

```
mcp-hub/
  pyproject.toml
  mcp_hub/
    __init__.py
    adapters/
      __init__.py      # AgentAdapter protocol + registry
      claude_code.py
      codex.py
      antigravity.py
    catalog.py          # loads catalog.yaml
    catalog.yaml
    models.py            # ServerSpec, ServerEntry
    tui/
      app.py
      dashboard.py
      server_list.py
      add_wizard.py
  tests/
    test_claude_code_adapter.py
    test_codex_adapter.py
    test_antigravity_adapter.py
    test_catalog.py
    fixtures/
```
