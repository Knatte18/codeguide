# Install

How to install the codeguide plugin for Claude Code.

---

## Prerequisites

- [Claude Code](https://claude.com/claude-code) CLI installed and on your PATH.
- Python 3 installed and on your PATH.
- This repository cloned locally (e.g. `c:\Code\codeguide`).

---

## Steps

### 1. Add the marketplace (first time only)

Register this repo as a local plugin marketplace:

```
claude plugin marketplace add c:/Code/codeguide
```

This tells Claude Code where to find `.claude-plugin/marketplace.json`.

### 2. Install the plugin into a target repo

From the target repo's directory:

```
cd /path/to/your/repo
claude plugin install codeguide@codeguide --scope project
```

This installs hooks and skills into `.claude/settings.json` (project-scoped). Repeat for each repo where you want codeguide.

### 3. Restart Claude Code

Close and reopen Claude Code in the target repo so it picks up the plugin.

### 4. Set up the documentation skeleton

```
/codeguide-setup --extensions .cs .py
```

This creates the `_codeguide/` directory with config, templates, and runtime folders.

---

## Updating

After editing skills, hooks, or templates in the `codeguide/` source:

1. Re-run `claude plugin install codeguide@codeguide --scope project` from each target repo.
2. Run `/codeguide-setup` in each target repo to update plugin-owned files (DocumentationGuide.md, NavigationHooks.md).
