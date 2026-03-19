---
name: codeguide-update
description: "Update existing _codeguide/ documentation to match current guide and code. Use after code changes or guide revisions."
argument-hint: "[project] [module-path]"
---

Update existing `_codeguide/` documentation to match the current Documentation Guide and source code. Does **not** commit.

## Scope

`$ARGUMENTS` controls what gets updated:

- No argument → all docs in all documented projects
- `WellboreModel` → all docs in that project's `_codeguide/`
- `WellboreModel/Solvers` → only the Solvers subfolder docs
- `WellboreModel/Solvers/Wemod` → only that one doc file

## Steps

1. **Read the Documentation Guide:** Read `_codeguide/modules/DocumentationGuide.md` in full. This is the authoritative structure — it may have changed since the docs were last written.

2. **Read local rules:** Read `_codeguide/local-rules.md` if it exists. These are repo-specific additions to the guide.

3. **Determine scope:** Parse `$ARGUMENTS` to identify which project(s) and doc file(s) to update. If no argument, find all projects that have `_codeguide/Overview.md`.

4. **For each doc in scope:**

   a. **Read the existing doc.**

   b. **Read the corresponding source file(s)** to check if behavior, interfaces, or relationships have changed.

   c. **Compare doc structure against the guide and local rules.** Check for:
      - Missing sections (e.g., "When not to use", "Relationships", negative boundaries in Overviews)
      - Sections that don't match guide conventions (e.g., API signatures that should be capability summaries)
      - Stale content (doc describes behavior that no longer matches the code)
      - Code-derived values that should not be in the doc (formulas, thresholds, constants)

   d. **Update the doc** if any of the above apply. Preserve accurate existing content — only change what's wrong or missing.

5. **Check Overview routing tables:** Verify that the project Overview's module table matches the actual doc files (no missing entries, no dead links, routing hints still accurate).

6. **Report changes:** Summarize what was updated and why.

## Rules

- Read the Documentation Guide and local rules first — do not rely on memory of what they say.
- Do not create new docs for undocumented source files. That is `/codeguide-init`'s job.
- Do not delete docs. If a doc has no corresponding source, flag it to the user.
- Preserve accurate existing content. Only modify what is structurally wrong or factually stale.
- When updating structure to match the guide, keep the existing content's meaning intact.
