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

This writes `enabledPlugins` into `.claude/settings.json` (project-scoped). Repeat for each repo where you want codeguide.

**Subfolder workspaces:** If you open Claude Code from a subfolder (e.g. a project within a monorepo), run the install from that subfolder too. The plugin activates per working directory — a parent's `.claude/settings.json` is not inherited.

### 3. Restart Claude Code

Close and reopen Claude Code in the target repo so it picks up the plugin.

### 4. Set up the documentation skeleton

```
/codeguide-init --extensions .cs .py
```

This creates the `_codeguide/` directory with config, templates, and runtime folders.

### 5. Add routing memories

The plugin's hooks rely on Claude Code reading `_codeguide/Overview.md` before navigating the codebase. Without explicit memory entries, Claude tends to skip the routing system and search files directly. Add two feedback memories to the target repo's `.claude/` memory directory:

**Routing-first lookup** — Always read `_codeguide/Overview.md` before using Grep/Glob/Bash to find files or symbols. Even targeted symbol lookups must go through routing first. Without this, Claude bypasses the routing system with direct searches and misses the documentation layer.

**Source-of-truth verification** — After routing via `_codeguide/`, always read the actual source files before answering factual questions. Never answer from doc content alone. Docs can contain stale or incomplete information (e.g. a missing term in a formula), so the source code is the authority.

---

## Updating

After editing skills, hooks, or templates in the `codeguide/` source:

1. Re-run `claude plugin install codeguide@codeguide --scope project` from each target repo.
2. Run `/codeguide-init` in each target repo to update plugin-owned files (DocumentationGuide.md, NavigationHooks.md).
