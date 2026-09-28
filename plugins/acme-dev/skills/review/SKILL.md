---
name: review
description: Reviews the current branch against the acme-dev rules and the repository's AGENTS.md with the read-only acme-dev reviewer, in its own context. Run before opening a pull request or after integrating subagent work; the argument is the base branch, main by default.
disable-model-invocation: true
argument-hint: [base-branch]
context: fork
agent: acme-dev:reviewer
background: false
---

Review the changes on the current branch against the base branch
`$ARGUMENTS`; when that is empty, use `main`, or `master` if `main` does not
exist. Include uncommitted changes in the working tree and say that you did.

Changed files:

!`git diff --stat "$(git merge-base HEAD origin/HEAD 2>/dev/null || echo HEAD)" 2>&1 || true`

If the block above is empty or shows the raw command, run
`git diff --stat <base>...HEAD` and `git status --short` yourself.

Follow your review order and report format. Change nothing.
