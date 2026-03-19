---
name: codeguide-generate
description: "Generate _codeguide/ documentation for source files that have no docs yet. Works for new and existing projects."
argument-hint: "[project] [module-path]"
---

Generate `_codeguide/` documentation for source files that don't have corresponding docs. Works both for projects with no docs at all and for existing projects with new source files. Does **not** commit.

## Scope

`$ARGUMENTS` controls what gets scanned:

- No argument → all projects in the repo
- `MyProject` → only that project
- `MyProject/Storage` → only that subfolder

## Steps

1. **Read the Documentation Guide:** Read `_codeguide/modules/DocumentationGuide.md` in full. All docs must follow its structure.

2. **Read local rules:** Read `_codeguide/local-rules.md` if it exists. These are repo-specific additions to the guide.

3. **Read source extensions:** Read `_codeguide/config.yaml` to get the list of recognized source extensions.

4. **Scan source structure:** List all folders and source files matching those extensions in scope (excluding build output directories like `obj/`, `bin/`, `__pycache__/`, `.venv/`).

5. **Identify undocumented source:** For each source file or source folder, check if a corresponding doc exists using the naming rules from the guide:
   - `parser.py` → `_codeguide/modules/Parser.md`
   - `utils/` (folder) → `_codeguide/modules/Utils.md`
   - If the doc exists and is current, skip it.

6. **Read undocumented source files:** Read only the source files that need new docs. Use parallel agent reads for large sets.

7. **Decide doc granularity:** Following the guide's rules:
   - One doc per source file or source folder
   - Large modules with subfolders get their own `_codeguide/modules/<Module>/Overview.md` + per-file docs
   - Small modules get a flat `_codeguide/modules/<Name>.md`

8. **Create docs for new project (if no Overview exists):**
   - Create `_codeguide/` and `_codeguide/modules/`
   - Write `_codeguide/Overview.md` with: scope, negative boundaries, dependencies, module table with routing hints, cross-cutting patterns
   - Update the repo-level `_codeguide/Overview.md` project table

9. **Write module docs:** For each undocumented module, create the doc following the guide structure:
   - What and why
   - Capability summaries (plain language, no signatures)
   - When not to use (negative space)
   - Relationships (depends on, consumed by)

10. **Update the project Overview:** Add rows to the module table for each new doc. Update routing hints if the new modules change the project's scope.

11. **Update IDE visibility (language-specific):** For .NET projects with a `.csproj`, ensure `<None Include="_codeguide\**\*.md" />` is in an ItemGroup. Skip for other languages.

12. **Report:** List what was created and what was skipped (already documented).

## Rules

- Follow the Documentation Guide exactly — read it first, not from memory.
- Apply local rules from `local-rules.md` on top of the guide.
- Do not include API signatures, line-by-line walkthroughs, or internal algorithm details.
- Do not include code-derived values: formulas, thresholds, constants, or expressions copied from source.
- Do not reference projects the code doesn't depend on.
- Do not modify existing docs. That is `/codeguide-sync`'s job.
- Capability summaries are the highest-value section — a reader should know if the module is relevant without reading source.
- Write docs as if they were written first and the code was written to satisfy them.
