---
name: codeguide-tracking
description: "Toggle navigation enforcement and/or violation logging."
argument-hint: "[enforcement|logging] [on|off]"
---

Toggle `enforcement` and `violation_logging` flags in `_codeguide/config.yaml` and rebuild hooks.json from composable base files.

## Flags

| Flag | What it controls |
|---|---|
| `enforcement` | Blocks search tools until `_codeguide/Overview.md` has been read. |
| `violation_logging` | Logs navigation violations to `runtime/navigation-issues.md` for `/review-navigation`. |

## Behavior

- `/codeguide-tracking enforcement on` → set `enforcement: true`
- `/codeguide-tracking enforcement off` → set `enforcement: false`
- `/codeguide-tracking logging on` → set `violation_logging: true`
- `/codeguide-tracking logging off` → set `violation_logging: false`
- `/codeguide-tracking` (no args) → show current values of both flags

## Steps

1. **Read** `_codeguide/config.yaml`. If it doesn't exist, stop with: "Run /codeguide-init first."

2. **Parse arguments:**
   - First arg is the flag name: `enforcement` or `logging` (maps to `violation_logging`)
   - Second arg is `on` or `off`
   - No arguments → read and display both flags, then stop

3. **Update config.yaml:** Replace the relevant flag line with the new value. Do not change anything else.

4. **Rebuild hooks.json:** Run the merge script to compose hooks.json from base files:

   ```
   python ${CLAUDE_PLUGIN_ROOT}/hooks/_merge_hooks.py ${CLAUDE_PLUGIN_ROOT}/hooks/hooks.json <inputs...>
   ```

   Always include `hooks-base.json`. Add `hooks-enforcement.json` if `enforcement: true`. Add `hooks-violation-logging.json` if `violation_logging: true`. Read both flags from config.yaml to determine which inputs to include.

   The composable hook files in `${CLAUDE_PLUGIN_ROOT}/hooks/`:
   - `hooks-base.json` — always included (routing instructions + doc-update reminders)
   - `hooks-enforcement.json` — session tracking, search blocking, cleanup
   - `hooks-violation-logging.json` — subagent parity tracking for review

5. **Report:** State what changed and remind the user that this takes effect on the next turn (hooks are loaded per-turn).

## What each layer includes

**Base** (always active):
| Hook | Event | Purpose |
|---|---|---|
| base_inject_routing.py | UserPromptSubmit, SubagentStart | Injects routing instructions |
| base_remind_docs.py | PostToolUse (Edit/Write) | Reminds to verify docs when source is modified |

**Enforcement** (`enforcement: true`):
| Hook | Event | Purpose |
|---|---|---|
| enforce_init_session.py | UserPromptSubmit | Creates turn-scoped session state |
| enforce_track_read.py | PreToolUse (Read) | Sets overview_read flag when _codeguide/ files are accessed |
| enforce_track_search.py | PreToolUse (Grep/Glob/Bash) | Blocks searches if Overview not read |
| enforce_stop.py | Stop | Cleans up session state; logs parity issues if `violation_logging: true` |

**Audit** (`violation_logging: true`):
| Hook | Event | Purpose |
|---|---|---|
| audit_track_task.py | PreToolUse (Agent) | Counts spawned subagents (parity check) |
| audit_track_subagent.py | SubagentStart | Counts injected subagents (parity check) |

## Rules

- Do not modify any file other than `_codeguide/config.yaml` and `${CLAUDE_PLUGIN_ROOT}/hooks/hooks.json`.
- Do not commit.
