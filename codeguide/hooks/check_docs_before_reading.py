"""
PreToolUse hook: reminds Claude to check _codeguide/ before scanning source files.
Currently DISABLED by default — the navigation violation hooks cover this with
less noise. Enable in settings.json if you want per-read reminders.

If the target is a recognized source file (per _codeguide/config.yaml), outputs
a JSON reminder. Otherwise no-op.
"""

import sys
import json
import os

# Load source extensions from config
repo_root = os.getcwd()
config_path = os.path.join(repo_root, "_codeguide", "config.yaml")

source_extensions = []
try:
    with open(config_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line.startswith("- ."):
                source_extensions.append(line[2:].strip())
except FileNotFoundError:
    pass

if not source_extensions:
    sys.exit(0)

data = json.load(sys.stdin)
tool_input = data.get("tool_input", {})

target = (
    tool_input.get("file_path", "")
    or tool_input.get("path", "")
    or tool_input.get("pattern", "")
    or ""
)

if any(target.lower().endswith(ext) for ext in source_extensions):
    print(json.dumps({
        "hookSpecificOutput": {
            "hookEventName": "PreToolUse",
            "additionalContext": (
                "REMINDER: Before scanning source files, check the relevant "
                "project's _codeguide/Overview.md first to identify which files matter."
            ),
        }
    }))
