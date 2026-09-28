---
name: acme-project-agents
description: How to create a project agent for Claude Code in an Acme repo. When an agent earns its file, where it lives (.claude/agents/), the frontmatter fields and what each does, the system prompt body, tool and model restrictions, preloaded skills, worktree isolation, memory, and the four agents the plugin ships. Invoke when asked to create, edit or review a custom agent or subagent definition.
---

# Project agents

Claude Code conventions; Cursor keeps its own agents in `.cursor/agents/`
and Codex has none of this. Skills and the plugin work everywhere, agent
files are Claude Code only.

## When an agent earns a file

A one-off task gets a prompt to the `Agent` tool, not a file. An agent file
is for a role that recurs with the same tools, the same restrictions and the
same briefing: the reviewer that runs before every pull request, the
implementer that only ever touches one package. If you would write the same
brief a third time, write the file.

## Where

- `.claude/agents/<name>.md` in the repo: project agents, committed, shared with every session in that repo.
- `~/.claude/agents/<name>.md`: personal agents for every repo on the machine.
- `agents/<name>.md` in a plugin: shipped agents; these cannot use `permissionMode`, `mcpServers` or `hooks`.

Project beats user beats plugin when names collide.

## The file

```markdown
---
name: migration-reviewer
description: Reviews new database migrations in this repository before a pull request. Use when a diff adds or changes a migration.
tools: Read, Grep, Glob, Bash
model: opus
effort: high
skills: [acme-dev:acme-rules, acme-dev:acme-stack]
memory: project
color: blue
---

You review migrations in this repository. ...
```

The body is the agent's system prompt. Write it as a brief, not a
procedure: the outcome, what done means, the boundaries, the evidence to
return, and the few cases where the agent stops early. Leave out "think
carefully"; `effort` is the control. When an agent keeps stopping at the
wrong moment, name that kind of stop in the body ("a status note that
announces the next step is not a place to stop") rather than adding
emphasis.

| Field | What it does |
|---|---|
| `name`, `description` | Required. The description decides when the orchestrator delegates to it; write when, not what. |
| `tools` / `disallowedTools` | Allow or deny list. A reviewer gets no `Edit` or `Write`. MCP tools by `mcp__<server>__<tool>`. |
| `model` | `opus`, `sonnet`, `haiku`, `inherit`, or a full ID. The `model` of an `Agent` call beats this field, which beats `CLAUDE_CODE_SUBAGENT_MODEL`, which beats the main session's model. |
| `effort` | `low` to `max`; overrides the session. `medium` for implementers, `high` for reviewers. Leave it out on Haiku 4.5, which has no effort levels. |
| `permissionMode` | `default`, `acceptEdits`, `plan`, ... Not for plugin agents. |
| `skills` | Preloaded skills. Agents do not inherit the session's skills; list the ones the role needs. |
| `memory` | `project`, `user` or `local`: the agent keeps notes across sessions. For a reviewer that should remember what it already flagged. |
| `isolation` | `worktree`: the agent works in its own checkout. Default for implementers. |
| `background` | Run in the background even when the caller would wait. |
| `maxTurns` | A ceiling; the agent reports partial work instead of running on. |
| `hooks`, `mcpServers` | Lifecycle hooks and servers scoped to this agent. Not for plugin agents. |

## The four agents the plugin ships

They exist in every repo as `acme-dev:reviewer`, `acme-dev:researcher`,
`acme-dev:implementer` and `acme-dev:mechanic`; a repo overrides one with a
file of the same name in `.claude/agents/`. Their roles and models are in
`acme-orchestrator`. Start a repo-specific agent by copying one of them and
adding what only this repo knows.

## Checklist before committing an agent file

- The description says when to use it, in one or two sentences an orchestrator can match.
- Tools are the minimum for the role. A reviewer cannot write.
- The body names the repo's commands and rules, or points at them, rather than assuming the agent knows.
- The body says what done means and when the agent stops early.
- `model` is set, and `effort` unless the model is Haiku.
- The file is under a hundred lines and mentioned in the repo's `AGENTS.md`.
