---
name: codeguide-reload
description: "Update plugin-owned files in _codeguide/ from the plugin source. Safe to run anytime."
---

Refresh plugin-owned files in the current repo's `_codeguide/` from the plugin source. Also updates the config schema if new keys have been added. Does **not** commit.

## Plugin-owned files

These are overwritten on reload:

- `${CLAUDE_PLUGIN_ROOT}/templates/DocumentationGuide.md` → `_codeguide/modules/DocumentationGuide.md`
- `${CLAUDE_PLUGIN_ROOT}/hooks/NavigationHooks.md` → `_codeguide/NavigationHooks.md`

## Config schema merge

The repo's `_codeguide/config.yaml` is user-owned — reload never overwrites it. But when the plugin template adds new keys, reload merges them in:

1. Read the template `${CLAUDE_PLUGIN_ROOT}/templates/config.yaml` and the repo's `_codeguide/config.yaml`.
2. For each key in the template that is missing from the repo config, add it with its default value and comment.
3. Do not change existing values or remove keys the user added.
4. Report which keys were added.

## Steps

1. **Find the target `_codeguide/`:** Run `python ${CLAUDE_PLUGIN_ROOT}/scripts/_resolve.py`. It prints the path to the nearest `_codeguide/` containing config.yaml (walks up from cwd). If it exits with an error, stop — run `/codeguide-init` first.

2. **Read plugin source files** from `${CLAUDE_PLUGIN_ROOT}`:
   - `templates/DocumentationGuide.md`
   - `hooks/NavigationHooks.md`
   - `templates/config.yaml`

3. **Overwrite local copies** at the target found in step 1:
   - `_codeguide/modules/DocumentationGuide.md`
   - `_codeguide/NavigationHooks.md`

4. **Merge config schema:** Compare `templates/config.yaml` with the target's `_codeguide/config.yaml`. Add missing keys with defaults (see Config schema merge above).

5. **Report** what was updated. If a file was identical to the source, say so. List any config keys that were added.

## Rules

- Do not overwrite repo-specific content in config.yaml — only add missing keys.
- Do not modify local-rules.md, Overview.md, or module docs.
- Do not commit. The user decides when to commit.
