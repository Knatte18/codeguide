---
name: codeguide-apply-rules
description: "Check existing docs against DocumentationGuide.md and local-rules.md, fix violations. Does not read source files — fast."
argument-hint: "[project]"
---

Check existing `_codeguide/` docs against the Documentation Guide and local rules, and fix any violations. Does **not** read source files — this is a fast, format-only pass. Does **not** commit.

## When to use

- After adding or changing a rule in `local-rules.md`
- After a plugin update brings a new `DocumentationGuide.md`
- To enforce consistency without the overhead of a full `/codeguide-update`

## Steps

1. **Read the Documentation Guide:** Read `_codeguide/modules/DocumentationGuide.md` in full.

2. **Read local rules:** Read `_codeguide/local-rules.md` if it exists.

3. **Determine scope:** Parse `$ARGUMENTS`:
   - No argument → all docs in all documented projects
   - `WellboreModel` → only that project's `_codeguide/`

4. **For each doc in scope:**

   a. **Read the existing doc.**

   b. **Check against guide and local rules:**
      - Missing required sections
      - Sections that violate guide conventions (e.g., API signatures, code-derived values, sibling links)
      - Formatting or structural issues
      - Violations of local rules

   c. **Fix violations** in place. Preserve all accurate content — only change what violates the rules.

5. **Report changes:** Summarize what was fixed and which rule triggered each fix.

## What this does NOT do

- Does not read source files — cannot detect stale content. Use `/codeguide-update` for that.
- Does not create new docs for undocumented source. Use `/codeguide-init` for that.
- Does not check pointer consistency (dead links, missing entries). Use `/codeguide-check` for that.

## Rules

- Read both the Documentation Guide and local rules before starting.
- Only modify docs that violate a rule. Do not rewrite docs that are already compliant.
- When fixing, preserve the existing content's meaning. Only change structure and formatting.
