---
name: end
description: Ends a work session in an Acme repository. Runs the check list, rewrites the handoff, commits and pushes the session branch, opens the pull request when the scope is done, and reports with the decisions waiting for the user first. Run at the end of a session.
disable-model-invocation: true
---

# End a work session

## State when the command ran

!`git status --short --branch 2>&1 || true`

Commits on this branch that are not on the default branch:

!`git log --oneline origin/HEAD..HEAD 2>&1 || git log --oneline -10 2>&1 || true`

If the blocks above are empty or show the raw commands, run them yourself.

## Steps

1. Run the full check list from `AGENTS.md`. A red check is fixed or
   reported, never left out of the report.
2. Rewrite `docs/HANDOFF.md` (or `HANDOFF.md` where the repo keeps it):
   date, where work stopped, what is decided, what is open, and a "Start
   here" block for the next session. Replace stale content; do not append.
3. Commit what belongs to this session. Subject says what the tree now
   does, body says why, no agent attribution. Changes that were in the tree
   before the session stay out.
4. Never commit or push on `main` unless the repo's `AGENTS.md` says that
   repo works on `main`. Push the session branch.
5. Scope done: open the pull request with `gh pr create`, title as a
   sentence, body with what changed and how it was checked. Scope not done:
   no pull request; the handoff says what is left.
6. Report in this order: decisions waiting for the user, what changed, the
   check list result, the pull request link, what is not built, what could
   not be verified.
