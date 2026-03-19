---
name: codeguide-reload
description: "Update plugin-owned files in _codeguide/ from the plugin source. Safe to run anytime."
---

Refresh plugin-owned files in the current repo's `_codeguide/` from the plugin source. Does **not** touch repo-specific files. Does **not** commit.

## Plugin-owned files

These are overwritten on reload:

- `${CLAUDE_PLUGIN_ROOT}/templates/DocumentationGuide.md` → `_codeguide/modules/DocumentationGuide.md`
- `${CLAUDE_PLUGIN_ROOT}/hooks/NavigationHooks.md` → `_codeguide/NavigationHooks.md`

## Steps

1. **Check prerequisites:** Verify `_codeguide/` exists in the working directory. If not, stop with an error — run `/codeguide-init` first.

2. **Read plugin source files** from `${CLAUDE_PLUGIN_ROOT}`:
   - `templates/DocumentationGuide.md`
   - `hooks/NavigationHooks.md`

3. **Overwrite local copies:**
   - `_codeguide/modules/DocumentationGuide.md`
   - `_codeguide/NavigationHooks.md`

4. **Report** what was updated. If a file was identical to the source, say so.

## Rules

- Do not modify repo-specific files (config.yaml, local-rules.md, Overview.md, module docs).
- Do not commit. The user decides when to commit.
