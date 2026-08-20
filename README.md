# mcp-hub

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python 3.11+](https://img.shields.io/badge/python-3.11%2B-blue.svg)](pyproject.toml)

A TUI package manager for [MCP](https://modelcontextprotocol.io) servers.
It detects which AI coding agents are installed on your machine (Claude
Code, Codex, Antigravity), shows what MCP servers each one already has
connected, and lets you add or remove a server across every detected agent
from one wizard — instead of hand-editing three different config files in
three different formats.

## Table of Contents

- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Supported Agents](#supported-agents)
- [Configuration](#configuration)
- [Development](#development)
- [Contributing](#contributing)
- [License](#license)

## Features

- **Auto-detect** — scans for Claude Code, Codex, and Antigravity config
  files on startup; no setup needed.
- **One dashboard** — see every agent's MCP servers, and whether its config
  file even parses, in one table.
- **Add wizard** — pick a server from the bundled catalog or enter one by
  hand, choose which detected agents to write it to, confirm.
- **Safe writes** — every add or remove backs up the config file (`.bak`)
  before touching it, and never crashes on a malformed or empty config.
- **Confirm before delete** — removing a server asks first.
- **i18n** — full English/Russian UI, toggle at runtime with `l`.
- **Themeable** — built-in Textual command palette (`ctrl+p`); your choice
  of theme and language persists between runs.

## Installation

```bash
pip install mcp-hub-tui
mcp-hub
```

Requires Python 3.11+. Published on PyPI as `mcp-hub-tui` (the `mcp-hub`
name was taken); the command is still `mcp-hub`.

### From source

```bash
git clone git@github.com:d2202/mcp-hub.git
cd mcp-hub
./run.sh
```

`run.sh` creates a `.venv` on first run, installs the package, and launches
the TUI.

## Usage

Launch with `./run.sh`, then:

1. **Dashboard** — one row per agent: detected or not, how many servers,
   where its config file lives. Select a row to open it.
2. **Server List** — the MCP servers configured for that agent. Invalid
   entries show why parsing failed instead of crashing.
3. **Add Wizard** (`a`) — pick a server from the bundled catalog or enter
   one by hand, choose target agents, confirm.

### Keybindings

| Key | Action |
|---|---|
| `enter` | open the selected row |
| `a` | add server (from a server list) |
| `r` | remove server, asks to confirm (from a server list) |
| `l` | toggle language (English / Russian) |
| `?` | help screen |
| `ctrl+p` | command palette (change theme, and more) |
| `escape` | go back |
| `q` | quit |

## Supported Agents

| Agent | Config file | Format |
|---|---|---|
| [Claude Code](https://code.claude.com) | `~/.claude.json` | JSON, `mcpServers` |
| [Codex CLI](https://github.com/openai/codex) | `~/.codex/config.toml` | TOML, `[mcp_servers.<name>]` |
| [Antigravity](https://antigravity.google) | `~/.gemini/config/mcp_config.json` | JSON, `mcpServers` |

Adding another agent is one new adapter file under `mcp_hub/adapters/`; the
rest of the app doesn't need to change.

## Configuration

mcp-hub's own settings (language, theme) live in
`~/.config/mcp-hub/settings.json` and are written automatically — nothing to
configure by hand. The bundled MCP server catalog is
[`mcp_hub/catalog.yaml`](mcp_hub/catalog.yaml).

## Development

```bash
python3.11 -m venv .venv
.venv/bin/pip install -e ".[dev]"
.venv/bin/pytest
```

## Contributing

Issues and PRs welcome. Keep changes covered by tests (`pytest`) and follow
the existing adapter/screen structure — see `mcp_hub/adapters/` for the
pattern a new agent adapter should follow.

## License

MIT — see [LICENSE](LICENSE).
