"""
SubagentStart hook: injects the repo-level _codeguide/Overview.md into every
subagent so it has the project routing table in context.

Not used for UserPromptSubmit — routing is enforced via memory + violation hooks.
"""

import json
import os

repo_root = os.getcwd()
overview_path = os.path.join(repo_root, "_codeguide", "Overview.md")

try:
    with open(overview_path, "r", encoding="utf-8") as f:
        overview = f.read()
except FileNotFoundError:
    overview = "(ERROR: _codeguide/Overview.md not found)"

context = (
    "MANDATORY: Read the relevant project _codeguide/Overview.md before touching any source files.\n"
    "NEVER use grep, glob, or find for file discovery. Use _codeguide routing only.\n"
    "NEVER spawn a subagent without including the relevant project Overview in the agent prompt.\n"
    "ALWAYS load required skills before starting any task.\n"
    "When writing or updating _codeguide/ docs, read _codeguide/local-rules.md first (if it exists) for repo-specific rules.\n"
    "_codeguide/ is a routing guide, NOT a source of truth. "
    "After using _codeguide/ to identify the relevant module, you MUST open and read the actual source files before answering. "
    "Do not answer factual questions about behavior, logic, contracts, or values from _codeguide/ content alone — the docs may be incomplete or imprecise.\n"
    "\n"
    f"{overview}"
)

print(json.dumps({
    "hookSpecificOutput": {
        "hookEventName": "SubagentStart",
        "additionalContext": context,
    }
}))
