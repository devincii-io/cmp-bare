# cmp-bare

A bare Claude Code plugin marketplace to copy and make your own. It ships one
plugin, `acme-dev`, which holds how a company develops software with Claude
Code: an index that every session starts with, an Opus 5.5 orchestrator setup
with four subagents, a starter set of rules, and one skill per stack and
process. Repos keep only their own facts in `AGENTS.md`; everything shared
lives here, so it cannot drift between projects.

`Acme` and the prefix `acme` are placeholders. One command replaces them.
Company-specific slots are marked `TODO` in the skills; the orchestrator
setup, the agents and the tooling work as they are.

Works in Claude Code, Codex and Cursor. Skills and the plugin install work in
all three; agents, hooks and the orchestrator setup are Claude Code first.

## Make it yours

```
git clone https://github.com/devincii-io/cmp-bare my-marketplace
cd my-marketplace
python tools/check.py rename <prefix> "<Company Name>"
python tools/check.py --fix
python tools/check.py            # must print ok
python tools/check.py todo       # the placeholders left to fill
```

Then set the owner, e-mail and repository URL in the manifests, fill the
index and `<prefix>-rules` first, and install (below). The `acme-howto` skill
has the same steps as a runbook.

## The Opus 5.5 orchestrator

The main session runs on Opus 5.5 and orchestrates: it plans, freezes the
contracts, briefs agents, integrates their work and reports. The plugin ships
the agents it delegates to:

| Agent | Model | Job |
|---|---|---|
| `acme-dev:researcher` | Sonnet, effort high | Reads many files or pages, returns an answer with citations |
| `acme-dev:implementer` | Opus, effort medium, own worktree, background | Builds one scoped part against frozen contracts |
| `acme-dev:mechanic` | Haiku | Applies a change that can be stated as a rule |
| `acme-dev:reviewer` | Opus, effort high, read-only | Reviews the integrated diff before the pull request |

Two settings matter, and `install/claude-settings.json` has both. Merge it
into `~/.claude/settings.json`:

```json
{
  "model": "opus",
  "modelSettings": { "claude-opus-5-5": { "effortLevel": "medium" } },
  "worktree": { "baseRef": "head" }
}
```

- Effort for Opus 5.5 goes under `modelSettings`. A top-level `effortLevel` in the user settings does not apply to Opus 5.5, and Opus 5.5 defaults to `medium`.
- `worktree.baseRef: "head"` makes agent worktrees branch from the session branch. On the default (`"fresh"`) they branch from the remote default branch and never see the contracts the orchestrator committed first.

The `acme-orchestrator` skill has the rest: the model and effort table, when
to delegate, the loop from request to pull request, and the limits.

## Layout

```
.claude-plugin/marketplace.json     Claude Code, and Codex through its legacy fallback
.agents/plugins/marketplace.json    Codex
.cursor-plugin/marketplace.json     Cursor
plugins/acme-dev/
  .claude-plugin/plugin.json        Claude Code and Codex manifest
  .codex-plugin/plugin.json         Codex display metadata
  .cursor-plugin/plugin.json        Cursor manifest
  hooks/hooks.json                  SessionStart hook, read by Claude Code and Codex
  hooks/session_start.py            prints the index; Python so the shell does not matter
  rules/acme-dev.mdc                generated: the index as an always-on Cursor rule
  agents/<name>.md                  researcher, implementer, mechanic, reviewer
  skills/<name>/SKILL.md            the skills
  evals/                            cases for `claude plugin eval`
tools/check.py                      consistency checks, version bump, rename, placeholder list
install/                            global instruction files and settings per tool
```

## Skills

| Skill | Holds | State |
|---|---|---|
| `acme-dev` | The index: where things live, how a session runs, the starter rules, which skill for what. Injected at session start. | Fill the TODOs |
| `acme-orchestrator` | Opus 5.5 orchestrator setup: settings, models, effort, delegation, the loop. | Ready |
| `acme-subagents` | Fan-out mechanics: contracts, briefs, worktrees, integration. | Ready |
| `acme-project-agents` | Writing an agent file in `.claude/agents/`. | Ready |
| `acme-agent-files` | One `AGENTS.md` per repo, and migrating a `CLAUDE.md`. | Ready |
| `acme-rules` | Starter rules with reasons. | Edit to taste |
| `acme-repo` | Git, branches, commits, issues, archiving. | Fill the TODOs |
| `acme-stack` | The default stack. | Bare |
| `acme-new-project` | Questions to ask, first commit, done-checklist. | Fill the TODOs |
| `acme-howto` | Install, adopt, release, evals. | Add your runbooks |
| `unslop` | Cutting AI patterns from prose. | Ready |
| `start`, `end`, `review` | `/acme-dev:start <topic>`, `/acme-dev:end`, `/acme-dev:review [base]`. Only run when typed. | Ready |

## Install

Claude Code, from a checkout or from GitHub:

```
claude plugin marketplace add <path to this folder, or owner/repo>
claude plugin install acme-dev@acme-claude-marketplace
```

Restart the session. The index is the first thing in the context.

Codex: `codex plugin marketplace add <absolute path>`, then
`codex plugin add acme-dev@acme-claude-marketplace`. `~/.codex/config.toml`
needs `[features] hooks = true`; trust the SessionStart hook once in `/hooks`.

Cursor: copy `plugins/acme-dev` to `~/.cursor/plugins/local/acme-dev` and
reload the window. The index arrives through the always-on rule.

`install/` also holds the recommended `~/.claude/CLAUDE.md` and
`~/.codex/AGENTS.md`: machine facts and a pointer to the plugin.

## Changing the plugin

1. Edit a skill, agent or hook under `plugins/acme-dev/`.
2. A new skill needs a row in the routing table of `skills/acme-dev/SKILL.md`; the check fails otherwise.
3. `python tools/check.py bump X.Y.Z`, then `python tools/check.py` must print `ok`. It also refuses em dashes and curly quotes in the prose.
4. `claude plugin validate .` and `claude plugin validate plugins/acme-dev`.
5. Commit, push. CI runs the same check.
6. `claude plugin update acme-dev@acme-claude-marketplace` and restart.

Updates are version-gated: without the bump the change does not ship.

## What goes where

| Content | Place |
|---|---|
| A convention that holds in every repo | A skill here |
| A fact about one repo: commands, its rules, gotchas | That repo's `AGENTS.md` |
| Session state | That repo's `docs/HANDOFF.md` |
| A decision | That repo's `docs/adr/` |
| Machine and shell specifics | The global instruction file of the tool |

Model facts, prices and settings were checked against the Claude Code and
Claude API docs on 2026-09-28.
