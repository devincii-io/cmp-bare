---
name: acme-dev
description: Acme development index. Injected at session start. Says where code, tasks and documents live, how the Opus 5.5 orchestrator and its subagents split the work, the rules that hold in every repo, and which acme-* skill answers what. Invoke when unsure where something lives or which convention applies.
---

# Acme development index

TODO: Two sentences on who Acme is: how many people build and run the software, what they build and for whom. The rules below should follow from that.

## Where things live

| What | Where |
|---|---|
| Code | TODO: the Git host and org, and the local layout (one repo per folder, parent folders are not repos). |
| Tasks, tickets, customers | TODO: the tracker or ERP, and how an agent reaches it (CLI, MCP server, read-only). |
| Business documents | TODO: the drive or wiki, and the folders that matter. |
| Accounts and access | TODO: where access is documented. Secrets never go into a repo. |
| Development conventions | This plugin. A repo's `AGENTS.md` holds only what is specific to that repo. |
| Session state of a repo | `docs/HANDOFF.md`. Decisions in `docs/adr/`. |

## How a session runs

The main session runs on Opus 5.5 and is the orchestrator. It talks to the user, plans, freezes contracts, writes briefs, delegates, integrates, reviews and reports. Subagents do the wide reading and the parallel building, each in its own context, and return conclusions:

| Agent | Model | Job |
|---|---|---|
| `acme-dev:researcher` | Sonnet, effort high | Reads many files or pages, returns an answer with citations |
| `acme-dev:implementer` | Opus, effort medium, own worktree | Builds one scoped part against frozen contracts |
| `acme-dev:mechanic` | Haiku | Applies a change that can be stated as a rule |
| `acme-dev:reviewer` | Opus, effort high, read-only | Reviews the integrated diff before the pull request |

Small tasks stay in the main session; a subagent starts empty and costs a full briefing. Setup, models and effort are in `acme-orchestrator`, the fan-out mechanics in `acme-subagents`.

## Rules that hold everywhere

A starter set. Replace or extend it; every rule keeps its reason in `acme-rules`.

1. Run the repo's full check list before saying anything is done. It is in the repo's `AGENTS.md`.
2. Work on a session branch and open one pull request at the end. Never push `main` directly.
3. Never invent a product, price, name, address, figure or legal text. Say what is missing.
4. Money, legal, vendors, publishing and deleting are not the agent's decisions. Name them, recommend, wait.
5. No secret in a repo, ever.
6. Comment where the code needs it: the non-obvious constraint, the rejected cheaper option. Never what the line already says.
7. No em dashes, no curly quotes. Apply `unslop` to docs, commits, comments and customer text.
8. Answer concisely and lead with the result. Commits carry no agent attribution.
9. Keep going through steps that need no input. Stop only for rule 4, a failing check you cannot fix, or a destructive or external action. End a long run with: blocked on the user, changed, found.

TODO: Add the company's own rules, one line each, with their reasons in `acme-rules`: the languages for code and for customers, the default stack, which records must stay append-only, what a regulator or a customer contract demands.

## Which skill for what

| Task | Use |
|---|---|
| Setting up or running the Opus 5.5 orchestrator: settings, models, effort, when to delegate | `acme-orchestrator` |
| Splitting a big scope across subagents: contracts, briefs, worktrees, integration | `acme-subagents` |
| Creating a project agent in `.claude/agents/`, or changing a shipped one | `acme-project-agents` |
| The development rules with their reasons | `acme-rules` |
| The default stack: toolchain, layout, commands, CI | `acme-stack` |
| Starting a new project | `acme-new-project` |
| Git, branches, commits, pull requests, issues, archiving a repo | `acme-repo` |
| Writing or fixing a repo's `AGENTS.md` | `acme-agent-files` |
| Prose others read: docs, commits, comments, customer text | `unslop` |
| Starting or ending a work session in a repo | `/acme-dev:start <topic>` and `/acme-dev:end`, skills `start` and `end` |
| Reviewing a branch before its pull request | `/acme-dev:review [base]`, skill `review`, runs `acme-dev:reviewer` |
| A recurring task: install the plugin, release a change, run the evals | `acme-howto` |
| Machine and shell specifics | The global instruction file of the tool you run in (`~/.claude/CLAUDE.md` or `~/.codex/AGENTS.md`) |

## Precedence

A repo's `AGENTS.md` beats this plugin for that repo. This plugin beats the tool's defaults and any older note. When two sources disagree, say so instead of picking silently.
