---
name: codeguide-stale
description: "Detect _codeguide/ module docs that are stale relative to their source files using git commit timestamps."
argument-hint: "[source-file-or-folder ...]"
---

Detect module docs whose source files have been committed more recently than the doc. Uses git commit timestamps — does not check content accuracy (that is `/codeguide-sync`'s job).

## Steps

1. **Find `_codeguide/`:** Run `python ${CLAUDE_PLUGIN_ROOT}/scripts/_resolve.py` to locate the nearest `_codeguide/` containing config.yaml. Use the returned path as the base for all `_codeguide/` references below. If it exits with an error, stop — run `/codeguide-init` first.

2. **Determine scope:** Parse `$ARGUMENTS` to get source file or folder paths. If no argument, find all source files in the current project using extensions from `_codeguide/config.yaml`.

2. **For each source file:**

   a. Walk up directories from the source file to find the nearest `_codeguide/` (stop at git root).

   b. Scan `## Source` sections in `_codeguide/modules/*.md` to find docs that reference the source file.

   c. Compare git commit dates: if the source file was committed more recently than the doc, the doc is stale.

   d. If a doc is stale, also flag its parent `Overview.md` (it may need a routing hint update).

3. **Report results:** List stale doc paths, one per line. If none are stale, say so.

## Rules

- Read-only — do not modify any files.
- A doc with no git history (untracked) is always considered stale.
- If a source file has no corresponding doc, skip it silently. That is `/codeguide-check`'s job to report.
