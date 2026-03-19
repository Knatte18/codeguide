# codeguide

Navigation-first documentation system for AI-assisted codebases.

Provides routing guides (`_codeguide/`) that direct Claude Code to the right source files before reading them, with enforcement hooks that block blind searching and log violations for guide improvement.

Installed as a Claude Code plugin. Per-repo setup via `/codeguide-init`.

## Install

See [INSTALL.md](INSTALL.md).

## Usage

After install and setup:

1. Edit `_codeguide/config.yaml` — set your source file extensions
2. Run `/codeguide-generate <project>` to create docs for a project
3. Claude Code will now route through `_codeguide/` before searching

### Skills

| Skill | Purpose |
|---|---|
| `/codeguide-init` | Initialize `_codeguide/` in the current repo (run once) |
| `/codeguide-generate` | Create docs for undocumented source files |
| `/codeguide-sync` | Sync existing docs with code changes and rule updates |
| `/codeguide-check` | Check pointer consistency, missing docs, and local-rules validity |
| `/codeguide-tracking` | Toggle navigation enforcement on/off |
| `/review-navigation` | Analyze navigation violations and propose guide improvements |

### How enforcement works

1. Every prompt creates a fresh session state file
2. Reading any `_codeguide/` file sets `overview_read: true`
3. After 3 search tool calls without `overview_read`, the tool is blocked
4. Claude must read `_codeguide/Overview.md` to unblock
5. Violations are logged with the user's prompt for later review
6. Session state is deleted when the turn ends

### Local rules

`_codeguide/local-rules.md` holds repo-specific documentation rules. These are applied on top of the generic DocumentationGuide.md by the skills.

Periodically collect `local-rules.md` files from multiple repos to identify patterns worth promoting to the generic guide.

## File ownership

| File | Owner | On update |
|---|---|---|
| `_codeguide/modules/DocumentationGuide.md` | Plugin | Overwritten by `/codeguide-init` |
| `_codeguide/NavigationHooks.md` | Plugin | Overwritten by `/codeguide-init` |
| `_codeguide/config.yaml` | Repo | Preserved |
| `_codeguide/local-rules.md` | Repo | Preserved |
| `_codeguide/Overview.md` | Repo | Preserved |
| `_codeguide/modules/*.md` (except above) | Repo | Preserved |

## Updating

Re-install the plugin:

```
claude plugin install codeguide@codeguide
```

Then run `/codeguide-init` in each repo to update plugin-owned files.
