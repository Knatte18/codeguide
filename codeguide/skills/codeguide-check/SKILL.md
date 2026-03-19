---
name: codeguide-check
description: "Check _codeguide/ pointer consistency: Overview tables vs actual doc files, sibling links, cross-area links. Does not check code accuracy."
argument-hint: "[project]"
---

Check structural consistency of `_codeguide/` documentation. Assumes doc content is accurate relative to its code file — only checks pointers and linking rules. Does **not** commit.

## Before starting

Read `_codeguide/modules/DocumentationGuide.md` first. It defines the linking rules, naming conventions, and file structure that this check enforces. Do not rely on assumptions about how docs are organized — the guide is authoritative.

## Scope

`$ARGUMENTS` controls what gets checked:

- No argument → all documented projects + repo-level docs
- `WellboreModel` → only that project's `_codeguide/`

## Checks

### 1. Overview module tables

For each `Overview.md` (project-level and subfolder-level):

a. **Dead links** — every `[link](path.md)` in the module table must resolve to an existing file.

b. **Missing entries** — every `.md` file in the corresponding `modules/` folder (or subfolder) must have a row in the Overview's module table. Ignore `Overview.md` itself.

c. **Orphan docs** — flag any doc file that exists but has no corresponding source file or folder. Do not delete — just report.

### 2. No sibling links

For each non-Overview doc, check that it contains no markdown links to other docs in the same folder. Links like `[Name](Name.md)` or `[Name](./Name.md)` are violations. Report the file and line.

### 3. Cross-area links target Overviews

For each non-Overview doc, check that any markdown link to a doc in a *different* folder points to an `Overview.md`, not a specific module doc. For example, `[Graph](../Graph/Overview.md)` is fine; `[GraphBuilder](../Graph/GraphBuilder.md)` is a violation.

### 4. Repo-level Overview

Check that the repo-level `_codeguide/Overview.md` project table:

a. Has a row for every project that contains a `_codeguide/Overview.md`.

b. Has no dead links (project Overview files that don't exist).

c. Projects without `_codeguide/` are marked as "*not yet documented*" or similar.

## Output

Report findings as a checklist:

```
## Results

### ProjectName
- [x] Overview table complete (N modules, N rows)
- [ ] MISSING from Overview: `modules/NewModule.md`
- [ ] DEAD LINK in Overview: `modules/DeletedModule.md`
- [ ] SIBLING LINK: `Foo.md:15` links to `[Bar](Bar.md)`
- [ ] CROSS-AREA LINK: `Foo.md:22` links to `[Baz](../Other/Baz.md)` — should target Overview.md
- [x] No orphan docs

### Repo-level
- [x] Project table complete
```

If everything passes, say so briefly.

## Rules

- Read-only — do not modify any files.
- Do not check whether doc content matches source code. That is `/codeguide-update`'s job.
- Do not create or delete docs.
