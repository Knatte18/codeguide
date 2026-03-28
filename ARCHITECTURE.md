# Codeguide Architecture

## Prerequisites

Add to `.claude/settings.json` in any folder where codeguide should be active:

```json
{
  "enabledPlugins": {
    "codeguide@codeguide": true
  }
}
```

This is done via `claude plugin install codeguide@codeguide --scope project`.

---

## Skills

### Initialization

| Skill | Purpose |
|---|---|
| `/codeguide-init` | First-time repo setup. Creates `_codeguide/` skeleton with plugin-owned files (DocumentationGuide.md, NavigationHooks.md, cgignore.md) and user-owned files (config.yaml, local-rules.md, cgexclude.md, Overview.md). Does NOT create module docs. |
| `/codeguide-setup` | Root: refreshes plugin-owned files, merges new config keys. Subfolder: creates `_codeguide/root.txt` (cached path to repo-level `_codeguide/`) and `cgexclude.md`. |

### Doc maintenance

| Skill | Weight | Scope | What it does |
|---|---|---|---|
| `/codeguide-generate` | Heavy | User-specified `[project] [module-path]` | Creates docs for undocumented source files. Full source scan. |
| `/codeguide-sync` | Heavy | User-specified `[project] [module-path]` | Fixes existing docs: content accuracy, structural violations, pointers, links, local-rules compliance. Full source + doc comparison. |
| `/codeguide-update` | Light | Git diff (default), `1h`, `3d`, `HEAD~3`, or explicit files | Combines generate + sync, but only for files in scope. Creates missing docs AND fixes stale docs. Safe for commit-time use (called by mill-commit). |

### Review

| Skill | Purpose |
|---|---|
| `/review-navigation` | Reviews violation logs in `_codeguide/runtime/navigation-issues.md`. Shows patterns of routing bypasses for guide improvement. |

---

## Hooks

| Hook | Event | Purpose |
|---|---|---|
| `base_inject_routing.py` | UserPromptSubmit, SubagentStart | Inject routing instructions — "read Overview.md first" |
| `enforce_init_session.py` | UserPromptSubmit | Create turn-scoped session state |
| `enforce_track_read.py` | PreToolUse (Read) | Track when Overview is read |
| `enforce_track_search.py` | PreToolUse (Grep/Glob/Bash) | Block searches until Overview read |
| `enforce_stop.py` | Stop | Clean up session state, log parity issues |
| `audit_track_task.py` | PreToolUse (Agent) | Count subagent spawns |
| `audit_track_subagent.py` | SubagentStart | Count subagent injections |

Enforcement hooks require `enforcement: true` in config.yaml. Audit hooks require `violation_logging: true`. Toggle by editing config.yaml directly.

---

## Shared scripts

| Script | Purpose |
|---|---|
| `scripts/_resolve.py` | Two-tier path resolution. Routing files resolve from cwd. Metadata files walk up to nearest ancestor (stops at `.git/`). Also callable as CLI: prints the metadata `_codeguide/` path. |
| `hooks/_merge_hooks.py` | Composes `hooks.json` from base files (`hooks-base.json`, `hooks-enforcement.json`, `hooks-violation-logging.json`). |

---

## File ownership

| File | Owner | Overwritten on reload? |
|---|---|---|
| `_codeguide/modules/DocumentationGuide.md` | Plugin | Yes |
| `_codeguide/NavigationHooks.md` | Plugin | Yes |
| `_codeguide/cgignore.md` | Plugin | Yes |
| `_codeguide/config.yaml` | User | No (new keys merged) |
| `_codeguide/local-rules.md` | User | No |
| `_codeguide/cgexclude.md` | User | No |
| `_codeguide/Overview.md` | User | No |
| `_codeguide/modules/*.md` | User | No |
| `_codeguide/root.txt` | Generated | Recreated by setup |

---

## Typical workflows

**First-time setup:**
1. `claude plugin install codeguide@codeguide --scope project`
2. `/codeguide-init .py`
3. `/codeguide-generate`

**Subfolder activation:**
1. `claude plugin install codeguide@codeguide --scope project` (from subfolder)
2. `/codeguide-setup`

**Plugin update:**
1. `claude plugin install codeguide@codeguide --scope project` (refreshes cache)
2. `/codeguide-setup` (refreshes plugin-owned files)

**Routine maintenance:**
1. `/codeguide-generate` — create missing docs
2. `/codeguide-sync` — fix stale/broken docs

**On commit (via mill-commit):**
1. `/codeguide-update` (auto-scoped to git diff)

**After working without mill-commit:**
1. `/codeguide-update 1h` (or `HEAD~3`, etc.)
