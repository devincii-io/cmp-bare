#!/usr/bin/env python3
"""Keep the acme-dev plugin consistent across Claude Code, Codex and Cursor.

    python tools/check.py                      verify; exit 1 on any finding
    python tools/check.py --fix                rewrite the derived files, then verify
    python tools/check.py bump 0.2.0           set the plugin version everywhere, then --fix
    python tools/check.py todo                 list the TODO placeholders still to fill
    python tools/check.py rename <prefix> <Company Name>
                                               make the template yours: replace the
                                               prefix "acme" and the name "Acme" in every
                                               file and path, then --fix

Derived files are never edited by hand. Today that is one file: the Cursor rule
rules/acme-dev.mdc, which is the index with a Cursor frontmatter, because Cursor
injects context through always-on rules rather than a session hook.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

# The template's placeholders. `rename` replaces both everywhere, this file included,
# so a second rename starts from the current values.
PREFIX = "acme"
COMPANY = "Acme"

ROOT = Path(__file__).resolve().parent.parent
PLUGIN_NAME = f"{PREFIX}-dev"
PLUGIN = ROOT / "plugins" / PLUGIN_NAME
SKILLS = PLUGIN / "skills"
INDEX = SKILLS / PLUGIN_NAME / "SKILL.md"
RULE = PLUGIN / "rules" / f"{PLUGIN_NAME}.mdc"
HOOKS = PLUGIN / "hooks" / "hooks.json"

PLUGIN_MANIFESTS = [
    PLUGIN / ".claude-plugin" / "plugin.json",
    PLUGIN / ".codex-plugin" / "plugin.json",
    PLUGIN / ".cursor-plugin" / "plugin.json",
]
# Marketplace files whose plugin entry carries version and description.
VERSIONED_MARKETPLACES = [
    ROOT / ".claude-plugin" / "marketplace.json",
    ROOT / ".cursor-plugin" / "marketplace.json",
]
CODEX_MARKETPLACE = ROOT / ".agents" / "plugins" / "marketplace.json"

NAME_RE = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
TODO_RE = re.compile(r"\bTODO:")
# Fields every tool understands, plus the Claude Code extras that the others ignore.
FRONTMATTER_KEYS = {"name", "description", "disable-model-invocation", "user-invocable", "paths"}
# Claude Code only. Codex and Cursor ignore them and run the body inline, so a
# skill using them must still read as a complete instruction without them.
CLAUDE_ONLY_KEYS = {"argument-hint", "context", "agent", "background", "model", "effort"}
# The unslop rule, enforced mechanically. Empty the dict to switch it off.
BANNED_CHARS = {
    "—": "em dash",
    "–": "en dash",
    "‘": "curly quote",
    "’": "curly quote",
    "“": "curly quote",
    "”": "curly quote",
}
AGENT_KEYS_IGNORED_IN_PLUGINS = {"permissionMode", "mcpServers", "hooks"}
INDEX_MAX_LINES = 140
DESCRIPTION_MAX = 1024
# Never touched by `rename` and never scanned for TODOs.
SKIP_PARTS = {".git", ".venv", "node_modules", "__pycache__", "results", "worktrees"}


def read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, data: dict) -> None:
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8", newline="\n")


def frontmatter(text: str) -> tuple[dict[str, str], str]:
    """Split a SKILL.md into frontmatter fields and body. Values are single-line strings."""
    if not text.startswith("---"):
        return {}, text
    end = text.find("\n---", 3)
    if end == -1:
        return {}, text
    fields: dict[str, str] = {}
    for line in text[3:end].strip().splitlines():
        if ":" in line:
            key, value = line.split(":", 1)
            fields[key.strip()] = value.strip()
    return fields, text[end + 4 :].strip()


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def prose_files() -> list[Path]:
    return (
        sorted(SKILLS.rglob("*.md"))
        + sorted(PLUGIN.glob("agents/*.md"))
        + sorted(PLUGIN.glob("rules/*.mdc"))
        + sorted(ROOT.glob("install/*"))
        + [ROOT / "README.md"]
    )


def plugin_entry(data: dict, path: Path, findings: list[str]) -> dict | None:
    for entry in data.get("plugins", []):
        if entry.get("name") == PLUGIN_NAME:
            return entry
    findings.append(f"{rel(path)}: no {PLUGIN_NAME} entry")
    return None


def check_manifests() -> list[str]:
    findings: list[str] = []
    manifests = {p: read_json(p) for p in PLUGIN_MANIFESTS}
    reference = manifests[PLUGIN_MANIFESTS[0]]
    for path, data in manifests.items():
        for key in ("name", "version", "description"):
            if data.get(key) != reference.get(key):
                findings.append(f"{rel(path)}: {key} differs from {rel(PLUGIN_MANIFESTS[0])}")
    source = f"./plugins/{PLUGIN_NAME}"
    for path in VERSIONED_MARKETPLACES:
        entry = plugin_entry(read_json(path), path, findings)
        if entry is None:
            continue
        for key in ("version", "description"):
            if entry.get(key) != reference.get(key):
                findings.append(f"{rel(path)}: {PLUGIN_NAME} entry {key} differs from the plugin manifest")
        if entry.get("source") != source:
            findings.append(f"{rel(path)}: {PLUGIN_NAME} source must be {source}")
    entry = plugin_entry(read_json(CODEX_MARKETPLACE), CODEX_MARKETPLACE, findings)
    if entry is not None and entry.get("source", {}).get("path") != source:
        findings.append(f"{rel(CODEX_MARKETPLACE)}: {PLUGIN_NAME} source.path must be {source}")
    return findings


def check_skills() -> list[str]:
    findings: list[str] = []
    index_body = frontmatter(INDEX.read_text(encoding="utf-8"))[1]
    for skill_dir in sorted(p for p in SKILLS.iterdir() if p.is_dir()):
        skill = skill_dir / "SKILL.md"
        if not skill.exists():
            findings.append(f"{rel(skill_dir)}: no SKILL.md")
            continue
        fields, body = frontmatter(skill.read_text(encoding="utf-8"))
        name = fields.get("name", "")
        if name != skill_dir.name:
            findings.append(f"{rel(skill)}: name {name!r} must equal the folder name")
        if not NAME_RE.match(name) or len(name) > 64:
            findings.append(f"{rel(skill)}: name must be lowercase kebab-case, at most 64 chars")
        description = fields.get("description", "")
        if not description:
            findings.append(f"{rel(skill)}: description missing")
        elif len(description) > DESCRIPTION_MAX:
            findings.append(f"{rel(skill)}: description longer than {DESCRIPTION_MAX} chars")
        for key in fields.keys() - FRONTMATTER_KEYS - CLAUDE_ONLY_KEYS:
            findings.append(f"{rel(skill)}: frontmatter key {key!r} is not portable across tools")
        if not body:
            findings.append(f"{rel(skill)}: empty body")
        if skill_dir.name != PLUGIN_NAME and f"`{skill_dir.name}`" not in index_body:
            findings.append(f"{rel(INDEX)}: does not route to `{skill_dir.name}`")
    if len(index_body.splitlines()) > INDEX_MAX_LINES:
        findings.append(
            f"{rel(INDEX)}: body longer than {INDEX_MAX_LINES} lines; it lands in every session"
        )
    return findings


def check_prose() -> list[str]:
    findings: list[str] = []
    for path in prose_files():
        for number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
            for char, label in BANNED_CHARS.items():
                if char in line:
                    findings.append(f"{rel(path)}:{number}: {label}")
                    break
    return findings


def check_agents() -> list[str]:
    """Plugin agents: name equals the file name, a description, and none of the
    fields Claude Code ignores for plugin-shipped agents."""
    findings: list[str] = []
    for path in sorted((PLUGIN / "agents").glob("*.md")):
        fields, body = frontmatter(path.read_text(encoding="utf-8"))
        if fields.get("name") != path.stem:
            findings.append(f"{rel(path)}: name must equal the file name")
        if not fields.get("description"):
            findings.append(f"{rel(path)}: description missing")
        if not fields.get("model"):
            findings.append(f"{rel(path)}: model missing; an agent without one inherits the orchestrator's")
        for key in fields.keys() & AGENT_KEYS_IGNORED_IN_PLUGINS:
            findings.append(f"{rel(path)}: {key!r} is ignored for plugin agents")
        if not body:
            findings.append(f"{rel(path)}: empty body")
    return findings


def check_hooks() -> list[str]:
    findings: list[str] = []
    data = read_json(HOOKS)
    for event, groups in data.get("hooks", {}).items():
        for group in groups:
            for hook in group.get("hooks", []):
                for script in re.findall(r"hooks/([\w.-]+)", hook.get("command", "")):
                    if not (PLUGIN / "hooks" / script).exists():
                        findings.append(f"{rel(HOOKS)}: {event} references missing hooks/{script}")
    return findings


def cursor_rule() -> str:
    fields, body = frontmatter(INDEX.read_text(encoding="utf-8"))
    return (
        "---\n"
        f"description: {fields.get('description', '')}\n"
        "alwaysApply: true\n"
        "---\n"
        f"<!-- Generated from skills/{PLUGIN_NAME}/SKILL.md by tools/check.py --fix. Do not edit. -->\n\n"
        f"{body}\n"
    )


def check_derived() -> list[str]:
    if not RULE.exists() or RULE.read_text(encoding="utf-8") != cursor_rule():
        return [f"{rel(RULE)}: out of date, run tools/check.py --fix"]
    return []


def todos() -> list[str]:
    found: list[str] = []
    for path in prose_files():
        if path == RULE:
            continue
        for number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
            if TODO_RE.search(line):
                found.append(f"{rel(path)}:{number}: {line.strip()}")
    return found


def fix() -> None:
    RULE.parent.mkdir(exist_ok=True)
    RULE.write_text(cursor_rule(), encoding="utf-8", newline="\n")
    print(f"wrote {rel(RULE)}")


def bump(version: str) -> None:
    if not re.match(r"^\d+\.\d+\.\d+$", version):
        sys.exit(f"not a semantic version: {version}")
    for path in PLUGIN_MANIFESTS:
        data = read_json(path)
        data["version"] = version
        write_json(path, data)
    for path in VERSIONED_MARKETPLACES:
        data = read_json(path)
        for entry in data.get("plugins", []):
            if entry.get("name") == PLUGIN_NAME:
                entry["version"] = version
        write_json(path, data)
    print(f"{PLUGIN_NAME} is now {version}")


def rename(prefix: str, company: str) -> None:
    """Replace the placeholders in every text file and every path. Plain string
    replacement on purpose: the placeholders are chosen to occur nowhere else."""
    if not NAME_RE.match(prefix) or len(prefix) > 40:
        sys.exit(f"the prefix must be lowercase kebab-case: {prefix}")
    if not company.strip():
        sys.exit("the company name is empty")

    def kept(path: Path) -> bool:
        return not SKIP_PARTS & set(path.relative_to(ROOT).parts)

    changed = 0
    for path in (p for p in ROOT.rglob("*") if p.is_file() and kept(p)):
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        new = text.replace(COMPANY, company).replace(PREFIX, prefix)
        if new != text:
            path.write_text(new, encoding="utf-8", newline="\n")
            changed += 1
    # Deepest first, so renaming a folder does not invalidate the paths below it.
    paths = [p for p in ROOT.rglob("*") if PREFIX in p.name and kept(p)]
    for path in sorted(paths, key=lambda p: len(p.parts), reverse=True):
        path.rename(path.with_name(path.name.replace(PREFIX, prefix)))
    print(f"rewrote {changed} files, renamed {len(paths)} paths: {PREFIX} -> {prefix}, {COMPANY} -> {company}")
    print("run `python tools/check.py --fix` next; this process still holds the old paths")


def main(argv: list[str]) -> int:
    if argv[:1] == ["rename"]:
        if len(argv) < 3:
            sys.exit('usage: tools/check.py rename <prefix> "<Company Name>"')
        rename(argv[1], " ".join(argv[2:]))
        return 0
    if argv == ["todo"]:
        found = todos()
        print("\n".join(found) if found else "no TODO placeholders left")
        return 0
    if argv[:1] == ["bump"]:
        if len(argv) != 2:
            sys.exit("usage: tools/check.py bump X.Y.Z")
        bump(argv[1])
        fix()
    elif argv == ["--fix"]:
        fix()
    elif argv:
        sys.exit(__doc__)
    findings = (
        check_manifests()
        + check_skills()
        + check_agents()
        + check_prose()
        + check_hooks()
        + check_derived()
    )
    for finding in findings:
        print(finding)
    left = len(todos())
    if left:
        print(f"{left} TODO placeholder(s) left to fill; `python tools/check.py todo` lists them")
    print("ok" if not findings else f"{len(findings)} finding(s)")
    return 1 if findings else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
