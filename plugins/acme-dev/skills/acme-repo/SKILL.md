---
name: acme-repo
description: Repositories and git at Acme. Folder layout, creating a repo, session branches and the one-pull-request rule, commit message style, issues for code work, worktrees, HANDOFF.md and ADRs, and archiving a repo before deleting it. Invoke when creating, cloning, branching, committing, opening a pull request, filing an issue, or archiving or deleting a repository.
---

# Repositories and git

## Layout on a machine

TODO: The folder tree: where company repos, customer repos and personal projects live. One git repo per folder; the parent folders are not repos.

`git rev-parse --show-toplevel` from inside a project must return the
project folder. If it returns the parent, a stray `.git` sits there; report
it.

## A new repository

TODO: The Git host, the org, default visibility, and the commit identity to use.

The first commit carries the files listed in `acme-new-project`.

## Branches, pull requests, CI

- Work on a session branch: `session/<date>-<topic>`. Commit there freely, push it a few times at most, open one pull request at the end, merge when CI is green, delete the branch.
- Never push `main` directly, never force-push `main`.
- CI runs on pull requests and on pushes to `main`, with read-only permissions and cancel-in-progress per branch.

## Commits

- Subject: one sentence under 72 characters saying what the tree now does. Not "fix stuff".
- Body: why, and what a reader six months later needs. It does not restate the diff.
- No agent attribution: no co-author line, no generated-by note.
- Stage your files by name. Unrelated work in the tree stays out.

TODO: The company's stance on type prefixes (`feat:`, `fix:`) and on issue references.

## Issues

Code work is tracked as issues in the repo it concerns. Title as a sentence,
body with what is wrong or wanted, why it matters, and what done looks like.
An agent that finds something out of scope files an issue instead of fixing
it silently, and says so in its report.

TODO: Where business tasks live instead, and the label set.

## Worktrees

Agent worktrees live in `.claude/worktrees/` and are gitignored. The setup
and pitfalls are in `acme-subagents`.

## Session state and decisions

- `docs/HANDOFF.md` is session state: date, where work stopped, what is decided, what is open, and a "Start here" block. Rewrite it when it is stale instead of appending.
- `docs/adr/NNNN-title.md` records a decision: date, status, context, decision, rationale, consequences. Superseded ADRs stay and say by which one.

## Archiving and deleting a repo

Deletion is the one operation git does not undo.

1. `git bundle create <name>.bundle --all`, then `git bundle verify <name>.bundle`.
2. Store the bundle where backups live. TODO: that place.
3. The user deletes the remote repo. Never as part of another task.
4. Delete the local folder and fix everything that pointed at the repo.
