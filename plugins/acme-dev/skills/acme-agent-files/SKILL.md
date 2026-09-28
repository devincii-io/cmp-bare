---
name: acme-agent-files
description: How an Acme repo instructs coding agents. One AGENTS.md per repo with only repo-specific facts, no CLAUDE.md, nothing the acme-dev plugin already says. The template, what belongs in and out, size limits, and migrating an existing CLAUDE.md. Invoke when creating, reviewing or migrating a repo's AGENTS.md or CLAUDE.md, or when asked where a convention should be written down.
---

# AGENTS.md, one per repo

Claude Code, Codex and Cursor all read `AGENTS.md`. Claude Code reads it
when no `CLAUDE.md` exists in the folder or above, which is the point: a
repo has one instruction file, so there is nothing to drift.

## What goes in

- What the project is, in three lines, and what it deliberately does not do.
- Where the docs are: architecture, handoff, ADRs.
- The commands: set up, lint, types, tests, run. The full check list, with the sentence "Run all of them before saying anything is done."
- The rules specific to this repo, numbered, each with its reason. Rules that hold everywhere are in the plugin and not repeated.
- Gotchas that already cost time, one line each, with the mechanism.
- The layout, as a tree with one comment per folder.
- Decisions not yet taken, so an agent does not take them silently.
- Repo-specific agents in `.claude/agents/`, one line each.

## What stays out

- Anything the plugin says: language rules, the git workflow, the stack defaults. A copy here drifts.
- Session state. That is `docs/HANDOFF.md`.
- Secrets, and anything a customer must not see if the repo is handed over.

## Size

Under 150 lines. A gotcha list that outgrows the file moves to `docs/` with a
one-line pointer. The commands block stays whatever the size; every session
runs it.

## Template

````markdown
# <name>

<What it is, three lines. Stack in one line.>

`docs/HANDOFF.md` is session state, decisions are in `docs/adr/`.
Conventions that hold in every repo come from the acme-dev plugin.

## Commands

```bash
<set up>
<lint>
<test>
```

Run all of them before saying anything is done. CI runs the same set.

## Rules

1. **<Rule.>** <Reason.>

## Gotchas that already cost time

- **<Symptom.>** <Mechanism and fix.>

## Layout

```
src/   ...
```

## Not decided yet

<List. Do not pick these silently.>
````

## Migrating a CLAUDE.md

1. Read `CLAUDE.md` and any `AGENTS.md` next to it. Where they disagree, the one describing the current deployment wins.
2. Write `AGENTS.md` from the newer content. Remove every paragraph the plugin covers. Keep every repo-specific rule, gotcha and command.
3. `git rm CLAUDE.md`, `git add AGENTS.md`.
4. Replace references to `CLAUDE.md` in docs and scripts.
5. Commit: "Replace CLAUDE.md with AGENTS.md" with one line on what moved to the plugin.
