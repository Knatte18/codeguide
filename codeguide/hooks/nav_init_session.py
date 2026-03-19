"""
UserPromptSubmit hook: creates a fresh turn-scoped session state file.

Runs on every user message. Always overwrites — state is turn-scoped only.
Captures the user prompt so violations can be logged with context.
"""

import json
import os
import pathlib
import sys

data = json.load(sys.stdin)
session_id = data.get("session_id") or os.environ.get("CLAUDE_SESSION_ID", "unknown")
prompt_text = data.get("prompt", "")[:500]  # cap at 500 chars

repo_root = pathlib.Path(os.getcwd())
sessions_dir = repo_root / "_codeguide" / "runtime" / "sessions"
sessions_dir.mkdir(parents=True, exist_ok=True)

state = {
    "session_id": session_id,
    "prompt": prompt_text,
    "overview_read": False,
    "search_count": 0,
    "subagents_spawned": 0,
    "subagents_injected": 0,
}

state_path = sessions_dir / f"{session_id}-state.json"
state_path.write_text(json.dumps(state, indent=2), encoding="utf-8")
