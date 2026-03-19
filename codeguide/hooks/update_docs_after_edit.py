"""
PostToolUse hook: reminds Claude to verify docs when source files or
_codeguide module docs are created or modified.

Fires on Edit and Write. Covers both new file creation and modification.
Source file extensions are read from _codeguide/config.yaml.
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

BUBBLE_UP = (
    "OVERVIEW BUBBLE-UP: After updating the module doc, walk upward through "
    "each parent Overview.md in _codeguide/. For each level, update the "
    "corresponding table row (description and 'Touch this when...' hint) if "
    "the module doc change affects it. Stop when a level needs no update or "
    "you reach the project-root _codeguide/Overview.md."
)

data = json.load(sys.stdin)
tool_input = data.get("tool_input", {})

file_path = tool_input.get("file_path", "") or ""
file_lower = file_path.lower().replace("\\", "/")

if source_extensions and any(file_lower.endswith(ext) for ext in source_extensions):
    basename = os.path.splitext(os.path.basename(file_path))[0]

    print(json.dumps({
        "hookSpecificOutput": {
            "hookEventName": "PostToolUse",
            "additionalContext": (
                f"DOC MAINTENANCE: You modified or created {os.path.basename(file_path)}. "
                f"Verify that a corresponding doc ({basename}.md) exists in the project's "
                "_codeguide/modules/ folder and is current. Find it via the project's _codeguide/Overview.md. "
                "Update the doc if any of these changed: public interface, observable behavior, "
                "contracts, relationships to other modules. "
                "Skip if: internal refactor or bug fix with identical external behavior. "
                "If the file was renamed, rename the corresponding doc file, update "
                "the project's _codeguide/Overview.md module table, and fix any cross-references "
                "in other doc files that link to the old name. "
                "When creating a new doc, first read _codeguide/modules/DocumentationGuide.md "
                "and _codeguide/local-rules.md (if it exists), and follow their structure. "
                + BUBBLE_UP
            ),
        }
    }))

elif (
    "_codeguide/" in file_lower
    and file_lower.endswith(".md")
    and os.path.basename(file_lower) not in ("overview.md", "documentationguide.md", "local-rules.md")
):
    print(json.dumps({
        "hookSpecificOutput": {
            "hookEventName": "PostToolUse",
            "additionalContext": (
                f"DOC MAINTENANCE: You modified {os.path.basename(file_path)} "
                f"(a _codeguide module doc). " + BUBBLE_UP
            ),
        }
    }))
