# Navigation Enforcement Hooks

Documents the hook system that enforces correct `_codeguide/` routing and catches navigation failures for guide improvement.

For the full explanation, see the [codeguide repository](https://github.com/hanf/codeguide).

---

## Two Rules Being Enforced

### Rule 1 — Route first

Before opening any source file or running any search, read the relevant project's `_codeguide/Overview.md`. This identifies which files are relevant without requiring pattern matching across the codebase.

### Rule 2 — Source files are the final step

`_codeguide/` docs route to the right files. They do not replace reading those files. For any factual question about behavior, logic, contracts, or values, the answer must come from the source — not from the doc. Docs may be incomplete or imprecise.

---

## How It Works

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
