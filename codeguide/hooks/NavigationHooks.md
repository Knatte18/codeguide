# Navigation Enforcement Hooks

Documents the hook system that enforces correct `_codeguide/` routing and catches navigation failures for guide improvement.

---

## Two Rules Being Enforced

### Rule 1 — Route first

Before opening any source file or running any search, read the relevant project's `_codeguide/Overview.md`. This identifies which files are relevant without requiring pattern matching across the codebase.

### Rule 2 — Source files are the final step

`_codeguide/` docs route to the right files. They do not replace reading those files. For any factual question about behavior, logic, contracts, or values, the answer must come from the source — not from the doc. Docs may be incomplete or imprecise.

---

## Hook Inventory

Hooks are split into two groups: **always-on** (provide core value) and **enforcement** (validate that the guide is working). The `tracking` flag in `_codeguide/config.yaml` controls which set is active. Toggle with `/codeguide-tracking`.

### Always-on hooks

These run regardless of the tracking flag.

| Hook | Event | What it does |
|---|---|---|
| `check_docs_on_prompt.py` | SubagentStart | Injects `_codeguide/Overview.md` into every subagent so it can route without searching |
| `update_docs_after_edit.py` | PostToolUse (Edit/Write) | Reminds Claude to verify docs when source files or `_codeguide/` module docs are modified |

### Enforcement hooks (tracking only)

These run only when `tracking: true`. They create session state, enforce the "read Overview first" rule, and log violations for review.

| Hook | Event | What it does |
|---|---|---|
| `nav_init_session.py` | UserPromptSubmit | Creates a turn-scoped session state file capturing the user prompt |
| `nav_track_read.py` | PreToolUse (Read) | Sets `overview_read` flag when any `_codeguide/` file is accessed |
| `nav_track_search.py` | PreToolUse (Grep/Glob/Bash) | Counts search calls; blocks after threshold if Overview not yet read; logs violations |
| `nav_track_task.py` | PreToolUse (Agent) | Counts subagent spawns for parity checking |
| `nav_track_subagent_inject.py` | SubagentStart | Counts subagent injections for parity checking |
| `nav_stop.py` | Stop | Logs parity issues (spawned vs injected) and deletes the session state file |

---

## How Enforcement Works

A turn-scoped session state file tracks whether `_codeguide/` has been read and how many search calls have been made. If the search count exceeds the threshold without `_codeguide/` having been read, the search tool is blocked until the guide is read.

Subagents receive the repo-level Overview injected verbatim, since they cannot inherit hook context.

Violations are logged to `_codeguide/runtime/navigation-issues.md` with the user's prompt, for later review via `/review-navigation`.

---

## Language Configuration

`_codeguide/config.yaml` defines which file extensions are recognized as source files. Hooks read this at runtime — to support a new language, add its extension to the list.

---

## Runtime Directory

```
_codeguide/
└── runtime/                        ← not version-controlled
    ├── sessions/
    │   └── {session_id}-state.json ← turn-scoped, deleted on Stop
    └── navigation-issues.md        ← accumulated violation log
```

---

## Adjusting the Threshold

The search threshold is set in `nav_track_search.py`. Start conservative and raise if legitimate work is being blocked.
