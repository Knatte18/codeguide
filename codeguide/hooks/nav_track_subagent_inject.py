"""
SubagentStart hook: increments subagents_injected in session state.

Runs alongside the Overview injection hook (check_docs_on_prompt.py).
Together they form a parity check: subagents_spawned (from nav_track_task.py)
vs subagents_injected detects whether the injection hook ran for every subagent.
"""

import json
import os
import pathlib
import sys

data = json.load(sys.stdin)
session_id = data.get("session_id") or os.environ.get("CLAUDE_SESSION_ID", "unknown")

sessions_dir = pathlib.Path(os.getcwd()) / "_codeguide" / "runtime" / "sessions"
state_path = sessions_dir / f"{session_id}-state.json"

if state_path.exists():
    state = json.loads(state_path.read_text(encoding="utf-8"))
    state["subagents_injected"] = state.get("subagents_injected", 0) + 1
    state_path.write_text(json.dumps(state, indent=2), encoding="utf-8")

sys.exit(0)
