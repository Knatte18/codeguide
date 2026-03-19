---
name: codeguide-setup
description: "Set up _codeguide/ in the current repo. Creates skeleton files, config, and .gitignore entry. Run once per repo."
argument-hint: "[--extensions .cs .py .ts]"
---

Set up `_codeguide/` in the current repository. Run this once after installing the codeguide plugin. Does **not** commit.

## What this creates

```
_codeguide/
├── config.yaml                    ← source file extensions (you own this)
├── local-rules.md                 ← repo-specific doc rules (you own this)
├── Overview.md                    ← repo routing table (you own this)
├── modules/
│   ├── DocumentationGuide.md      ← how to write docs (plugin-owned)
│   └── NavigationHooks.md         ← how hooks work (plugin-owned)
└── runtime/
    └── sessions/                  ← turn-scoped state (not version-controlled)
```

## Steps

1. **Check prerequisites:** Verify the working directory is a git repo (`.git/` exists). If not, stop with an error.

2. **Find plugin templates:** The templates are at `${CLAUDE_PLUGIN_ROOT}/templates/` (the codeguide plugin's install location). Read the template files from there:
   - `DocumentationGuide.md`
   - `NavigationHooks.md`
   - `config.yaml`
   - `local-rules.md`

3. **Create directories:** Create `_codeguide/modules/` and `_codeguide/runtime/sessions/`.

4. **Copy plugin-owned files** (always overwritten on re-run):
   - `templates/DocumentationGuide.md` → `_codeguide/modules/DocumentationGuide.md`
   - `templates/NavigationHooks.md` → `_codeguide/modules/NavigationHooks.md`

5. **Create repo-specific files** (only if they don't exist):
   - `_codeguide/config.yaml` — if `$ARGUMENTS` contains `--extensions`, write a config with those extensions. Otherwise copy the template (with commented-out examples).
   - `_codeguide/local-rules.md` — copy from template.
   - `_codeguide/Overview.md` — create with starter content:
     ```markdown
     # Repo Overview

     TODO: Add a project map table and dependency graph.

     ## Documentation system

     See [DocumentationGuide.md](modules/DocumentationGuide.md) for how docs are written and organized.

     See [NavigationHooks.md](modules/NavigationHooks.md) for routing enforcement.
     ```

6. **Update .gitignore:** Add `**/_codeguide/runtime/` if not already present.

7. **Report** what was created vs skipped.

## On re-run

Safe to re-run. Plugin-owned files (DocumentationGuide.md, NavigationHooks.md) are overwritten. Repo-specific files (config.yaml, local-rules.md, Overview.md, module docs) are never touched.

## Rules

- Do not modify existing repo-specific files.
- Do not commit. The user decides when to commit.
- If `_codeguide/` already exists with all files, report "already set up" and list what would be overwritten on a plugin update.
