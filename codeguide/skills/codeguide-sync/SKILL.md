---
name: codeguide-sync
description: "Sync existing _codeguide/ docs with current source code, guide, and local rules. Fixes stale content and structural violations."
argument-hint: "[project] [module-path]"
---

Sync existing `_codeguide/` documentation with the current source code, Documentation Guide, and local rules. Fixes both content accuracy and structural compliance. Does **not** commit.

## When to use

- After code changes that affect module behavior, interfaces, or relationships
- After adding or changing a rule in `local-rules.md`
- After a plugin update brings a new `DocumentationGuide.md`

## Scope

`$ARGUMENTS` controls what gets synced:

- No argument → all docs in all documented projects
- `MyProject` → all docs in that project's `_codeguide/`
- `MyProject/Storage` → only the Storage subfolder docs
- `MyProject/Storage/BlobCache` → only that one doc file

## Steps

1. **Read the Documentation Guide:** Read `_codeguide/modules/DocumentationGuide.md` in full. This is the authoritative structure — it may have changed since the docs were last written.

2. **Read local rules:** Read `_codeguide/local-rules.md` if it exists. These are repo-specific additions to the guide.

3. **Determine scope:** Parse `$ARGUMENTS` to identify which project(s) and doc file(s) to sync. If no argument, find all projects that have `_codeguide/Overview.md`.

4. **For each doc in scope:**

   a. **Read the existing doc.**

   b. **Read the corresponding source file(s)** to check if behavior, interfaces, or relationships have changed.

   c. **Check the Source section:** Verify that the relative paths in the `## Source` section resolve to existing files. If a path is broken, search for the file by name and update the path. If the Source section is missing, add it using relative paths from the doc to the source file(s).

   d. **Check doc content against source code:**
      - Stale content (doc describes behavior that no longer matches the code)
      - Code-derived values that should not be in the doc (formulas, thresholds, constants)

   e. **Check doc structure against guide and local rules:**
      - Missing required sections (e.g., "When not to use", "Relationships", negative boundaries in Overviews)
      - Sections that don't match guide conventions (e.g., API signatures that should be capability summaries)
      - Formatting or structural issues
      - Violations of local rules

   f. **Update the doc** if any of the above apply. Preserve accurate existing content — only change what's wrong or missing.

   g. **Update the `synced:` timestamp** in the doc's YAML frontmatter to the current UTC time (`YYYY-MM-DD-HHMMSS`). If the frontmatter or `synced:` field doesn't exist, add it.

5. **Check Overview routing tables:** Verify that the project Overview's module table matches the actual doc files (no missing entries, no dead links, routing hints still accurate).

6. **Report changes:** Summarize what was updated and which rule or code change triggered each fix.

## Rules

- Read the Documentation Guide and local rules first — do not rely on memory of what they say.
- Do not create new docs for undocumented source files. That is `/codeguide-generate`'s job. However, flag undocumented source files to the user so they know what's missing. For large scopes, summarize (e.g., "none of the source files in ProjectX are documented") rather than listing every file.
- Do not delete docs. If a doc has no corresponding source, flag it to the user.
- Preserve accurate existing content. Only modify what is structurally wrong or factually stale.
- When updating structure to match the guide, keep the existing content's meaning intact.
