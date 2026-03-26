"""
Detect codeguide module docs that are stale relative to their source files.

Input: source file paths as arguments or one per line on stdin.
Output: stale doc paths, one per line. Exit 0 if none, exit 1 if any stale.

For each source file:
1. Walk up directories to find the nearest _codeguide/ (stop at git root).
2. Scan ## Source sections in _codeguide/modules/ to find docs referencing the file.
3. Compare the doc's synced: frontmatter timestamp against the source file's
   last commit date. If the source is newer, the doc is stale.
4. If a doc is stale, also flag its parent Overview.md.
"""

import os
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

from codeguide.utcnow import TIMESTAMP_FMT


def find_git_root(start: Path) -> Path | None:
    current = start.resolve()
    while True:
        if (current / ".git").exists():
            return current
        parent = current.parent
        if parent == current:
            return None
        current = parent


def find_codeguide_root(source_file: Path) -> Path | None:
    git_root = find_git_root(source_file)
    if git_root is None:
        return None
    current = source_file.parent.resolve()
    git_root = git_root.resolve()
    while True:
        candidate = current / "_codeguide"
        if candidate.is_dir() and (candidate / "Overview.md").exists():
            return candidate
        if current == git_root:
            return None
        parent = current.parent
        if parent == current:
            return None
        current = parent


def parse_synced_timestamp(doc_path: Path) -> datetime | None:
    try:
        with open(doc_path, "r", encoding="utf-8") as f:
            content = f.read()
    except (FileNotFoundError, OSError):
        return None

    # Look for synced: in YAML frontmatter
    fm_match = re.match(r"^---\s*\n(.*?)\n---", content, re.DOTALL)
    if not fm_match:
        return None

    for line in fm_match.group(1).splitlines():
        line = line.strip()
        if line.startswith("synced:"):
            value = line.split(":", 1)[1].strip()
            try:
                return datetime.strptime(value, TIMESTAMP_FMT).replace(
                    tzinfo=timezone.utc
                )
            except ValueError:
                return None
    return None


def get_source_commit_date(source_file: Path) -> datetime | None:
    try:
        result = subprocess.run(
            ["git", "log", "-1", "--format=%aI", "--", str(source_file)],
            capture_output=True,
            text=True,
            cwd=source_file.parent,
        )
        if result.returncode != 0 or not result.stdout.strip():
            return None
        return datetime.fromisoformat(result.stdout.strip())
    except (OSError, ValueError):
        return None


def find_docs_referencing(source_file: Path, codeguide_root: Path) -> list[Path]:
    modules_dir = codeguide_root / "modules"
    if not modules_dir.is_dir():
        return []

    source_name = source_file.name
    matching_docs = []

    for doc_path in modules_dir.rglob("*.md"):
        if doc_path.name == "DocumentationGuide.md":
            continue
        try:
            with open(doc_path, "r", encoding="utf-8") as f:
                content = f.read()
        except (FileNotFoundError, OSError):
            continue

        # Look for ## Source section
        source_match = re.search(r"^## Source\s*\n(.*?)(?=\n## |\Z)", content,
                                 re.MULTILINE | re.DOTALL)
        if not source_match:
            continue

        source_section = source_match.group(1)
        # Check if any link in the Source section points to this file
        for link_match in re.finditer(r"\[.*?\]\((.*?)\)", source_section):
            rel_path = link_match.group(1)
            resolved = (doc_path.parent / rel_path).resolve()
            if resolved == source_file.resolve():
                matching_docs.append(doc_path)
                break
        else:
            # Fallback: check if the filename appears in the section
            if source_name in source_section:
                matching_docs.append(doc_path)

    return matching_docs


def find_parent_overview(doc_path: Path, codeguide_root: Path) -> Path | None:
    # The parent Overview is at _codeguide/Overview.md for flat docs,
    # or _codeguide/modules/<Subfolder>/Overview.md for nested docs
    doc_dir = doc_path.parent
    modules_dir = codeguide_root / "modules"

    if doc_dir == modules_dir:
        # Flat doc — parent is _codeguide/Overview.md
        overview = codeguide_root / "Overview.md"
    else:
        # Nested doc — parent is the subfolder's Overview.md
        overview = doc_dir / "Overview.md"
        if not overview.exists() or overview == doc_path:
            overview = codeguide_root / "Overview.md"

    return overview if overview.exists() else None


def main():
    source_files: list[str] = []

    if len(sys.argv) > 1:
        source_files = sys.argv[1:]
    elif not sys.stdin.isatty():
        source_files = [line.strip() for line in sys.stdin if line.strip()]

    if not source_files:
        sys.exit(0)

    stale_docs: set[str] = set()

    for source_path_str in source_files:
        source_file = Path(source_path_str).resolve()
        if not source_file.is_file():
            continue

        codeguide_root = find_codeguide_root(source_file)
        if codeguide_root is None:
            continue

        docs = find_docs_referencing(source_file, codeguide_root)
        if not docs:
            continue

        source_date = get_source_commit_date(source_file)
        if source_date is None:
            continue

        for doc_path in docs:
            synced_date = parse_synced_timestamp(doc_path)
            if synced_date is None or source_date > synced_date:
                stale_docs.add(str(doc_path))
                overview = find_parent_overview(doc_path, codeguide_root)
                if overview:
                    stale_docs.add(str(overview))

    if stale_docs:
        for doc in sorted(stale_docs):
            print(doc)
        sys.exit(1)
    else:
        sys.exit(0)


if __name__ == "__main__":
    main()
