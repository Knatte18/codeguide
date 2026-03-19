---
name: codeguide-tracking
description: "Toggle navigation enforcement and violation tracking on or off."
argument-hint: "[on|off]"
---

Toggle the `tracking` flag in `_codeguide/config.yaml` and install the matching hooks configuration.

## Behavior

- If `$ARGUMENTS` is `on` or `off`, set `tracking` to that value.
- If no argument, toggle: `true` → `false`, `false` → `true`.
- After updating the flag, copy the correct hooks file into place:
  - `tracking: true` → copy `${CLAUDE_PLUGIN_ROOT}/hooks/hooks-full.json` to `${CLAUDE_PLUGIN_ROOT}/hooks/hooks.json`
  - `tracking: false` → copy `${CLAUDE_PLUGIN_ROOT}/hooks/hooks-minimal.json` to `${CLAUDE_PLUGIN_ROOT}/hooks/hooks.json`

## Steps

1. **Read** `_codeguide/config.yaml`. If it doesn't exist, stop with: "Run /codeguide-init first."

2. **Determine new value:**
   - Argument `on` → new value is `true`
   - Argument `off` → new value is `false`
   - No argument → flip the current value

3. **Update config.yaml:** Replace the `tracking:` line with the new value. Do not change anything else in the file.

4. **Install hooks:** The plugin ships two hooks files:
   - `${CLAUDE_PLUGIN_ROOT}/hooks/hooks-full.json` — all hooks (enforcement + tracking)
   - `${CLAUDE_PLUGIN_ROOT}/hooks/hooks-minimal.json` — only Overview injection and doc-update reminders

   Read the source file matching the new value. Write its content to `${CLAUDE_PLUGIN_ROOT}/hooks/hooks.json`.

5. **Report:** State what changed and remind the user that this takes effect on the next turn (hooks are loaded per-turn).

## What each mode includes

**Tracking on** (all hooks):
| Hook | Event | Purpose |
|---|---|---|
| nav_init_session.py | UserPromptSubmit | Creates turn-scoped session state |
| check_docs_on_prompt.py | SubagentStart | Injects Overview into subagents |
| nav_track_subagent_inject.py | SubagentStart | Counts injected subagents (parity check) |
| nav_track_read.py | PreToolUse (Read) | Sets overview_read flag when _codeguide/ files are accessed |
| nav_track_search.py | PreToolUse (Grep/Glob/Bash) | Counts searches, blocks violations, logs to navigation-issues.md |
| nav_track_task.py | PreToolUse (Agent) | Counts spawned subagents (parity check) |
| update_docs_after_edit.py | PostToolUse (Edit/Write) | Reminds to verify docs when source is modified |
| nav_stop.py | Stop | Logs parity issues, deletes session state |

**Tracking off** (minimal hooks):
| Hook | Event | Purpose |
|---|---|---|
| check_docs_on_prompt.py | SubagentStart | Injects Overview into subagents |
| update_docs_after_edit.py | PostToolUse (Edit/Write) | Reminds to verify docs when source is modified |

## Rules

- Do not modify any file other than `_codeguide/config.yaml` and `${CLAUDE_PLUGIN_ROOT}/hooks/hooks.json`.
- Do not commit.
