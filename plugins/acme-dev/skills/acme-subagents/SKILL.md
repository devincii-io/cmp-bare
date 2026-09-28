---
name: acme-subagents
description: Subagent-driven development with Claude Code agents. When to fan out, freezing contracts first, writing briefs with strict file ownership, worktree isolation and its pitfalls, integrating on a session branch, the merge steps that recur, and the one-pull-request finish. Invoke when a scope is too big for one context, when asked to use subagents, parallel agents or worktrees, or before spawning more than one agent.
---

# Subagent-driven development

Claude Code conventions. Codex and Cursor have their own agent models; this
skill is not required to work there. Models, effort and the orchestrator's
loop are in `acme-orchestrator`; this skill is the mechanics.

## When to fan out

- The scope splits into parts that touch different files and can be described in one page each. Three parts with a shared contract beat eight parts that all edit the same router.
- Research that needs many files read but only a conclusion returned: one researcher or `Explore` agent per question, never the main context.
- Audits and migrations across many similar units (services, modules, sites): one agent per unit, each returning one row of a shared table (`unit | affected | evidence`). Check the evidence before accepting a row.
- Verification: a reviewer agent on the diff, a fresh agent reproducing a bug from the description alone.

Do not fan out when the parts share files, when the contract between them is still moving, or when the whole thing is under an hour of focused work.

## Order of work

1. **Freeze the contracts on the branch first.** Event names and payloads, function signatures, route paths and schemas, shared fixtures. Commit them before any agent starts. An agent that invents a contract produces work that cannot be merged.
2. **Cut the scope by file ownership.** Each agent owns a list of files or folders and touches nothing else. Two agents editing one file is a merge conflict with extra steps.
3. **Write one brief per agent** (below). Name the other agents' scopes in each brief so nobody fills a gap that belongs to someone else.
4. **Spawn** all agents in one message, in the background, implementers with worktree isolation.
5. **Wait for all reports.** Keep the parts as a checklist in the task list or `docs/HANDOFF.md`. Do not run end-to-end tests while agents are still building; fixed ports collide across checkouts.
6. **Integrate on the session branch.** Merge each worktree branch, resolve, run the full check list once at the end, in one checkout.
7. **Review the integrated diff** with `/acme-dev:review` before the pull request, not per agent.
8. **One pull request**, CI green, merge.

## The brief

A brief is the agent's whole world. It contains:

- The goal in two sentences and the definition of done, including the commands that must pass. The outcome, not the steps: an agent handed the whole task with a clear finish line does better than one walked through it step by step.
- The few cases where it stops early (a contract must change, a foreign check fails, a destructive or external action is next). Everything else it decides and names in the report.
- The owned files and folders, and an explicit "do not touch" list naming the other agents' scopes.
- The frozen contracts, quoted or pointed at by path and commit.
- The repo's `AGENTS.md` rules that matter for this part, one line each, and the gotchas that apply.
- What to report back: files changed, tests added, anything left undone, any contract it wanted to change and did not.

An agent does not inherit the conversation unless it is a `fork`. Everything it needs is in the brief or in the repo.

## Worktrees

- `isolation: "worktree"` gives the agent its own checkout under `.claude/worktrees/<name>`. With `worktree.baseRef: "head"` it branches from the current HEAD; with the default `"fresh"` from the remote default branch, which does not contain the contracts you just committed. `acme-orchestrator` has the setting.
- A worktree is a fresh checkout of the tracked files. A `.worktreeinclude` in the repo root (gitignore syntax) copies gitignored files such as `.env` into every new worktree. Dependencies (`.venv`, `node_modules`) are installed in the worktree. When a build fails in a worktree, check that first.
- Worktrees with no changes are removed when the agent finishes; changed ones stay until merged and cleaned.
- Hooks keep `${CLAUDE_PROJECT_DIR}` at the launch point; the `cwd` in the hook input follows the worktree.

## Merge steps that recur

Parallel work collides in the same places every time: migrations branched from the same parent, version constants, shared test fixtures, two new files with the same name. Plan for them at integration.

TODO: The merge steps that recur in Acme's own repos, one line each, once they are known.

## Reporting

Lead with what is blocked on the user. Then per agent: what it built, what passed, what it left. Then the integrated state: the check list result, the pull request link, what is not built, and what nobody could verify.
