---
name: codeguide-init
description: "Create _codeguide/ documentation for a project from scratch. Use when a project has source code but no docs yet."
argument-hint: "<project-name>"
---

Create `_codeguide/` documentation for the specified project. Does **not** commit.

## Steps

1. **Read the Documentation Guide:** Read `_codeguide/modules/DocumentationGuide.md` in full. All docs must follow its structure.

2. **Read local rules:** Read `_codeguide/local-rules.md` if it exists. These are repo-specific additions to the guide.

3. **Identify the project:** Use `$ARGUMENTS` as the project folder name. If no argument, ask the user which project to document.

4. **Check for existing docs:** If `<project>/_codeguide/Overview.md` already exists, stop and suggest `/codeguide-update` instead.

5. **Read source extensions:** Read `_codeguide/config.yaml` to get the list of recognized source extensions.

6. **Scan source structure:** List all folders and source files matching those extensions in the project (excluding build output directories like `obj/`, `bin/`, `__pycache__/`, `.venv/`). Identify major areas by folder structure.

7. **Read source files:** Read all source files (per config extensions) to understand module responsibilities. Use parallel agent reads for large projects.

8. **Decide doc granularity:** Following the guide's rules:
   - One doc per source file or source folder
   - Large modules with subfolders get their own `_codeguide/modules/<Module>/Overview.md` + per-file docs
   - Small modules get a flat `_codeguide/modules/<Name>.md`

9. **Create directory structure:** Create `_codeguide/` and `_codeguide/modules/` (and any subfolders for split modules).

10. **Write the project Overview:** Create `_codeguide/Overview.md` with:
   - What this project is responsible for (sharp boundary)
   - What this project does NOT own (negative boundaries with redirects)
   - Dependencies with direction (consumes X, consumed by Y)
   - Module table with routing hints ("Touch this when...")
   - Cross-cutting patterns

11. **Write module docs:** For each module, create the doc following the guide structure:
   - What and why
   - Capability summaries (plain language, no signatures)
   - When not to use (negative space)
   - Relationships (depends on, consumed by)

12. **Update IDE visibility (language-specific):** For .NET projects with a `.csproj`, add `<None Include="_codeguide\**\*.md" />` to an ItemGroup. Skip for other languages.

13. **Update repo Overview:** In `_codeguide/Overview.md` at repo root, update the project row to link to the new Overview.

## Rules

- Follow the Documentation Guide exactly — read it first, not from memory.
- Apply local rules from `local-rules.md` on top of the guide.
- Do not include API signatures, line-by-line walkthroughs, or internal algorithm details.
- Do not include code-derived values: formulas, thresholds, constants, or expressions copied from source.
- Do not reference projects the code doesn't depend on.
- Capability summaries are the highest-value section — a reader should know if the module is relevant without reading source.
- Write docs as if they were written first and the code was written to satisfy them.
