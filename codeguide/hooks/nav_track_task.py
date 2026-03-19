"""
PreToolUse hook for the Agent tool: increments subagents_spawned in session state.
"""

import json
import os
import pathlib
import sys

data = json.load(sys.stdin)
session_id = data.get("session_id") or os.environ.get("CLAUDE_SESSION_ID", "unknown")
tool_name = data.get("tool_name", "")

if tool_name != "Agent":
    sys.exit(0)

sessions_dir = pathlib.Path(os.getcwd()) / "_codeguide" / "runtime" / "sessions"
state_path = sessions_dir / f"{session_id}-state.json"

if state_path.exists():
    state = json.loads(state_path.read_text(encoding="utf-8"))
    state["subagents_spawned"] = state.get("subagents_spawned", 0) + 1
    state_path.write_text(json.dumps(state, indent=2), encoding="utf-8")

sys.exit(0)
