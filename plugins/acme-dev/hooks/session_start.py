"""SessionStart hook: print the acme-dev index so every session starts with it.

Claude Code and Codex add whatever this prints to the session context. The
text is the body of skills/acme-dev/SKILL.md, found relative to this file so the
hook does not depend on CLAUDE_PLUGIN_ROOT being expanded by the shell.

Called with `python`, not `python3`: on a Windows machine `python3` is often
the Microsoft Store alias, which prints an install hint and exits.
"""

from __future__ import annotations

import sys
from pathlib import Path

INDEX = Path(__file__).resolve().parent.parent / "skills" / "acme-dev" / "SKILL.md"


def body(text: str) -> str:
    """Strip the YAML frontmatter; the agent needs the index, not its metadata."""
    if text.startswith("---"):
        end = text.find("\n---", 3)
        if end != -1:
            text = text[end + 4 :]
    return text.strip()


def main() -> int:
    try:
        text = INDEX.read_text(encoding="utf-8")
    except OSError as exc:
        print(f"acme-dev: index not readable ({exc}); invoke the acme-dev skill by hand.")
        return 0
    # A Windows console pipe defaults to cp1252, which cannot encode every
    # character the index may contain.
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    print(body(text))
    return 0


if __name__ == "__main__":
    sys.exit(main())
