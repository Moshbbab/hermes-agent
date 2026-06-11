# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

> **`AGENTS.md` in the repo root is the authoritative, deep-dive developer guide.** Read it before non-trivial work — it covers the contribution rubric, the Footprint Ladder, plugins, skills authoring standards, profiles, delegation, cron, kanban, curator, and known pitfalls in full detail. This file is the condensed quick-reference.

## What Hermes Is

A personal AI agent running the same core (`AIAgent` in `run_agent.py`) across a CLI, a TUI, a messaging gateway (~20 platforms), and an Electron desktop app. Two principles govern every change:

1. **Prompt caching is sacred.** Never mutate past context, swap toolsets, or rebuild the system prompt mid-conversation (sole exception: context compression). Commands that mutate system-prompt state must default to deferred invalidation with an opt-in `--now` flag.
2. **Narrow waist, capable edges.** Every core model tool ships on every API call. New capability should arrive as (in order of preference): extension of existing code → CLI command + skill → service-gated tool (`check_fn`) → plugin → MCP catalog server → new core tool (last resort).

## Commands

```bash
source .venv/bin/activate   # or venv/ — always activate before Python work
hermes                      # interactive CLI
hermes --tui                # Ink/React TUI
hermes gateway start        # messaging gateway
hermes doctor               # diagnose config/env issues
```

### Testing — always use the wrapper, never bare `pytest`

```bash
scripts/run_tests.sh                                   # full suite, CI-parity
scripts/run_tests.sh tests/gateway/                    # one directory
scripts/run_tests.sh tests/agent/test_foo.py           # one file
scripts/run_tests.sh tests/agent/test_foo.py -- -k test_x   # one test (-k filter)
scripts/run_tests.sh -j 4                              # cap parallelism
scripts/run_tests.sh -- -v --tb=long                   # pytest args go after '--'
```

The wrapper runs in a hermetic `env -i` environment (credentials can't leak, `TZ=UTC`, `LANG=C.UTF-8`, `PYTHONHASHSEED=0`) and delegates to `scripts/run_tests_parallel.py`: **per-file** isolation — each test file gets its own freshly-spawned `python -m pytest <file>` subprocess (no xdist, no shared workers). Node-ID selectors (`file.py::test_x`) are not accepted as positionals — use `-- -k`. Per-test 30s timeout comes from `--timeout=30` in pyproject `addopts`. `tests/conftest.py` redirects `HERMES_HOME` to a temp dir for any pytest invocation. Run the full suite before pushing.

### TUI development

```bash
cd ui-tui
npm run dev        # watch mode
npm run typecheck  # tsc --noEmit
npm run lint && npm run fmt
npm test           # vitest
```

Desktop-app tests (`apps/desktop/`) run via the repo-root `vitest` (deps resolve from the root workspace install).

## Architecture

### Tool registration dependency chain

```
tools/registry.py   (no deps)
    ↑
tools/*.py          (each calls registry.register() at import time — auto-discovered)
    ↑
model_tools.py      (triggers discovery; handle_function_call() dispatches)
    ↑
run_agent.py / cli.py / batch_runner.py
```

Auto-discovery imports any `tools/*.py` with a top-level `registry.register()`, but a tool is only **exposed** if its name appears in a toolset in `toolsets.py` (`_HERMES_CORE_TOOLS` is the default bundle). All handlers must return a JSON string.

### Core entry points

| File | Role |
|---|---|
| `run_agent.py` | `AIAgent` — synchronous agent loop in `run_conversation()`; OpenAI message format; ~60 init params |
| `cli.py` | `HermesCLI` — prompt_toolkit interactive CLI |
| `hermes_cli/main.py` | All `hermes` subcommands; `_apply_profile_override()` sets `HERMES_HOME` before imports |
| `hermes_cli/commands.py` | `COMMAND_REGISTRY` of `CommandDef`s — single source for CLI/gateway/Telegram/Slack/autocomplete/help |
| `gateway/run.py` | Messaging gateway main loop; `gateway/platforms/` has one adapter per platform |
| `tui_gateway/server.py` | JSON-RPC backend for the TUI (newline-delimited JSON-RPC over stdio; Node/Ink owns the screen, Python owns state) |
| `hermes_constants.py` | `get_hermes_home()` / `display_hermes_home()` — profile-aware paths |

### Chat surfaces — don't duplicate them

- The dashboard (`hermes dashboard` → `/chat`) embeds the **real** `hermes --tui` over a PTY WebSocket (`hermes_cli/pty_bridge.py`). Never re-implement the transcript/composer in React — extend Ink instead.
- The Electron desktop app (`apps/desktop/`) is a separate renderer talking JSON-RPC to `tui_gateway`; its slash palette curation lives in `apps/desktop/src/lib/desktop-slash-commands.ts` (hide noisy built-ins, never hide skill/quick-command extensions).

### Plugins (three discovery systems)

- **General** (`hermes_cli/plugins.py`): `register(ctx)` provides lifecycle hooks, `ctx.register_tool()`, `ctx.register_cli_command()`. Discovery runs as a side effect of importing `model_tools.py` — call `discover_plugins()` explicitly otherwise.
- **Memory providers** (`plugins/memory/`): implement the `MemoryProvider` ABC. The in-tree set is **closed** — new backends ship as standalone plugin repos.
- **Model providers** (`plugins/model-providers/`): each calls `register_provider(ProviderProfile(...))`; lazily scanned by `providers/__init__.py`, NOT by PluginManager. User plugins override bundled ones by name.

**Plugins must never modify core files** (`run_agent.py`, `cli.py`, `gateway/run.py`, `hermes_cli/main.py`). Widen the generic plugin surface instead.

### Skills vs tools

Almost all new capability should be a **skill**, not a tool. Bundled skills in `skills/`, heavy/niche ones in `optional-skills/`. Skill authoring standards are HARDLINE (see AGENTS.md): description ≤ 60 chars, reference native Hermes tools by name (`terminal`, `read_file`, `patch`, `search_files` — not `grep`/`cat`/`sed`), audit `platforms:` gating against actual script imports, tests at `tests/skills/test_<skill>_skill.py` (stdlib + pytest + mock only).

## Hard Rules

- **Profile-safe paths:** use `get_hermes_home()` for state, `display_hermes_home()` for user-facing strings. Never hardcode `~/.hermes` (broke 5 things in PR #3575). Tests mocking `Path.home()` must also set `HERMES_HOME`.
- **`.env` is for secrets only.** All behavioral settings (timeouts, flags, display prefs) go in `config.yaml` (`DEFAULT_CONFIG` in `hermes_cli/config.py`). Only bump `_config_version` when actively migrating/renaming keys — new keys deep-merge automatically.
- **Three config loaders:** `load_cli_config()` (cli.py), `load_config()` (hermes_cli/config.py), raw YAML (gateway). If CLI sees a key but gateway doesn't, you're on the wrong loader.
- **Dependency pinning:** every dependency needs an upper bound (`>=floor,<next_major`); git URLs pinned to commit SHA; GitHub Actions pinned to SHA. Run `uv lock` after changes.
- **Strict message-role alternation:** never two same-role messages in a row, never inject a synthetic user message mid-loop.
- **No change-detector tests:** don't assert catalog snapshots, config version literals, or enumeration counts. Assert relationships/invariants instead.
- **No cross-tool references in schema descriptions** — referenced tools may be unavailable; add dynamically in `get_tool_definitions()` if needed.
- **No new `simple_term_menu` usage** (rendering bugs in tmux/iTerm2) — use `hermes_cli/curses_ui.py`. **No `\033[K`** in spinner/display code — use space-padding.
- **Gateway has two message guards** (base adapter queue + runner intercept); commands that must reach the runner while an agent runs must bypass both inline.
- **`delegate_task` is synchronous and not durable** — long-running work that must outlive the turn uses `cronjob` or `terminal(background=True, notify_on_complete=True)`.

## TypeScript Style (desktop, TUI, website)

Small nanostores over prop-drilling; feature-owned atoms (`useStore` to render, `$atom.get()` for non-rendering reads); thin route roots; no monolithic hooks; interfaces over `type` for public props; table-driven mappings over condition ladders. `src/app` = routes/pages, `src/store` = shared atoms, `src/lib` = pure helpers.
