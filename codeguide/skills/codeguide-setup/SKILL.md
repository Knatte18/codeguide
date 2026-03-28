---
name: codeguide-setup
description: "Root: refresh plugin-owned files. Subfolder: create cached root pointer and cgexclude. Safe to run anytime."
---

Set up or refresh codeguide in the current working directory. Behavior depends on whether this is a repo root or a subfolder. Does **not** commit.

## Steps

1. **Detect context:** Run `python ${CLAUDE_PLUGIN_ROOT}/scripts/_resolve.py` to find the nearest `_codeguide/` with config.yaml.

2. **Determine mode:**
   - If config.yaml is in **cwd's own** `_codeguide/` → **root mode**
   - If config.yaml is in an **ancestor's** `_codeguide/` → **subfolder mode**
   - If not found at all → stop with error, run `/codeguide-init` first

### Root mode

Refresh plugin-owned files and merge config:

3. **Read plugin source files** from `${CLAUDE_PLUGIN_ROOT}`:
   - `templates/DocumentationGuide.md`
   - `templates/cgignore.md`
   - `hooks/NavigationHooks.md`
   - `templates/config.yaml`

4. **Overwrite plugin-owned files:**
   - `_codeguide/modules/DocumentationGuide.md`
   - `_codeguide/NavigationHooks.md`
   - `_codeguide/cgignore.md`

5. **Merge config schema:** For each key in the template that is missing from the repo's `_codeguide/config.yaml`, add it with its default value and comment. Do not change existing values.

6. **Create `_codeguide/cgexclude.md`** if it doesn't exist. Copy from `${CLAUDE_PLUGIN_ROOT}/templates/cgexclude.md`.

7. **Report** what was updated.

### Subfolder mode

Create a lightweight `_codeguide/` for this subfolder:

3. **Create `_codeguide/root.txt`:** Write the absolute path to the ancestor `_codeguide/` found in step 1. Hooks use this to skip the walk-up on every call.

4. **Create `_codeguide/cgexclude.md`** if it doesn't exist. Copy from `${CLAUDE_PLUGIN_ROOT}/templates/cgexclude.md` (empty template).

5. **Report** what was created.

## Rules

- Do not overwrite user-owned files: config.yaml values, local-rules.md, cgexclude.md, Overview.md, module docs.
- Do not commit. The user decides when to commit.
