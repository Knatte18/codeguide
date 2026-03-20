"""
SubagentStart hook: injects the local _codeguide/Overview.md into every
subagent so it has the project routing table in context.

Overview.md is resolved from cwd (routing context). Metadata references
(local-rules.md) walk up to the nearest ancestor that contains them.

Not used for UserPromptSubmit — routing is enforced via memory + violation hooks.
"""

import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _resolve import routing_root

overview_path = routing_root() / "Overview.md"

try:
    overview = overview_path.read_text(encoding="utf-8")
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
