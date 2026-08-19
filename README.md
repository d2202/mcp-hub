# mcp-hub

A TUI package manager for MCP servers. It detects which AI coding agents are
installed on your machine (Claude Code, Codex, Antigravity), shows what MCP
servers each one already has connected, and lets you add or remove a server
across every detected agent from one wizard — instead of hand-editing three
different config files in three different formats.

## Install & run

```bash
git clone git@github.com:d2202/mcp-hub.git
cd mcp-hub
./run.sh
```

`run.sh` creates a `.venv` on first run, installs the package, and launches
the TUI. Requires Python 3.11+.

## Screens

- **Dashboard** — one row per agent: detected or not, how many servers,
  where its config file lives. Select a row to open it.
- **Server List** — the MCP servers configured for that agent. Invalid
  entries show why parsing failed instead of crashing.
- **Add Wizard** — pick a server from the bundled catalog or enter one by
  hand, choose which detected agents to write it to, confirm.

## Keys

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

Every add or remove writes a `.bak` copy of the config file first. Language
and theme are remembered between runs (`~/.config/mcp-hub/settings.json`).

## Supported agents

| Agent | Config file |
|---|---|
| Claude Code | `~/.claude.json` (`mcpServers`) |
| Codex CLI | `~/.codex/config.toml` (`[mcp_servers.<name>]`) |
| Antigravity | `~/.gemini/config/mcp_config.json` (`mcpServers`) |

Adding another agent is one new adapter file (see `mcp_hub/adapters/`); the
rest of the app doesn't need to change.

## Development

```bash
python3.11 -m venv .venv
.venv/bin/pip install -e ".[dev]"
.venv/bin/pytest
```

## License

MIT — see [LICENSE](LICENSE).
