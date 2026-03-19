---
name: codeguide-check
description: "Check _codeguide/ pointer consistency and local-rules validity. Does not check doc-to-code accuracy."
argument-hint: "[project]"
---

Check structural consistency of `_codeguide/` documentation. Assumes doc content is accurate relative to its code file — only checks pointers and linking rules. Does **not** commit.

## Before starting

Read `_codeguide/modules/DocumentationGuide.md` first. It defines the linking rules, naming conventions, and file structure that this check enforces. Do not rely on assumptions about how docs are organized — the guide is authoritative.

## Scope

`$ARGUMENTS` controls what gets checked:

- No argument → all documented projects + repo-level docs
- `MyProject` → only that project's `_codeguide/`

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

### 5. Missing docs

Read `_codeguide/config.yaml` to get the list of recognized source extensions. For each source file or source folder in the project that matches those extensions, check if a corresponding doc exists using the naming rules from the guide:

- `parser.py` → `_codeguide/modules/Parser.md`
- `utils/` (folder) → `_codeguide/modules/Utils.md`
- If not found by file name, check by parent folder name (the two-step lookup from the guide).

Report each source file that has no corresponding doc. Do not create docs — just list what's missing. The user can then run `/codeguide-generate` to fill the gaps.

Exclude build output directories (`obj/`, `bin/`, `__pycache__/`, `.venv/`).

### 6. Local-rules validation

If `_codeguide/local-rules.md` exists, read it and check each rule that makes a verifiable claim against the codebase. Verifiable claims include: dependency direction between modules, named patterns or conventions, structural invariants (e.g., "all controllers inherit from BaseController"), layer ordering.

For each verifiable rule:
- Spot-check the claim against the code (e.g., verify the dependency direction, check that the referenced pattern still exists).
- If the rule matches the code: pass silently.
- If there is a mismatch: **stop and present both sides to the user**:
  - What the rule says (quote the relevant line from local-rules.md)
  - What the code shows (file, line, or search result that contradicts)
  - Ask: *"Is the rule outdated (update it), or is the code non-conforming (flag it)?"*

**Do not auto-fix rules. Do not silently skip mismatches.** A mismatch can mean the rule drifted (convention changed, rule wasn't updated) or the code drifted (someone broke the convention). Only the user can decide which.

Skip rules that are purely stylistic guidance with no verifiable assertion (e.g., "keep docs concise").

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
- [ ] MISSING DOC: `src/Validators/InputValidator.cs` has no corresponding doc
- [ ] MISSING DOC: `src/Middleware/` folder has no corresponding doc

### Repo-level
- [x] Project table complete

### Local rules
- [x] "Services depend on Repositories, never the reverse" — verified
- [ ] MISMATCH: Rule says "all endpoints return ApiResponse<T>", but `UserController.cs:47` returns `IActionResult` — rule outdated or code non-conforming?
```

If everything passes, say so briefly.

## Rules

- Read-only — do not modify any files.
- Do not check whether doc content matches source code. That is `/codeguide-sync`'s job.
- Do not create or delete docs.
