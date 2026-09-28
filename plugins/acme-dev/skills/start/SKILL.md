---
name: start
description: Starts a work session in an Acme repository. Shows the git state and the handoff, runs the check list, and puts the work on a session branch. Run at the beginning of a session, with the topic as argument.
disable-model-invocation: true
argument-hint: [topic]
---

# Start a work session

Topic: $ARGUMENTS

## State when the command ran

Branch and working tree:

!`git status --short --branch 2>&1 || true`

Last commits:

!`git log --oneline -5 2>&1 || true`

Handoff:

!`cat docs/HANDOFF.md 2>/dev/null || cat HANDOFF.md 2>/dev/null || echo "no HANDOFF.md"`

If the three blocks above are empty or show the raw commands, the tool did
not run them; run them yourself first.

## Steps

1. Read `AGENTS.md` if it is not already in context. Its check list is the
   one to run.
2. Run the full check list. A red check before anything was touched is the
   first finding; report it, do not fix it silently.
3. Uncommitted changes that are not from this session stay untouched. Say
   they are there.
4. When the handoff names a branch to continue on, switch to it. Otherwise
   create `session/<YYYY-MM-DD>-<topic>` from the default branch, with the
   topic in kebab-case. No topic given: ask for one.
5. Report in a few lines: branch, check list result, what the handoff says
   is next, anything odd in the tree. Then wait for the task.
