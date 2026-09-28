---
name: acme-orchestrator
description: Running Claude Code with Opus 5.5 as the orchestrator. The settings for the main session and for subagents, the model and effort table, what the orchestrator does itself and what it delegates, the loop from request to pull request, steering running agents, and the final report. Invoke when setting up a machine, choosing a model or effort for an agent, deciding whether to delegate, or before a run that will spawn agents.
---

# The Opus 5.5 orchestrator

The main session runs on Opus 5.5. It owns the conversation with the user,
the plan, the contracts and the final state of the branch. Subagents own the
reading that would flood its context and the building that can run in
parallel. The orchestrator's context is the scarce resource of a long run:
it keeps conclusions, decisions and the checklist of parts, never file dumps.

Facts below were checked against the Claude Code and Claude API docs on
2026-09-28. Model names, prices and defaults change; check again when a new
model ships.

## Setup on a machine

1. Install the plugin (`acme-howto`, "Install the plugin").
2. Merge `install/claude-settings.json` from the marketplace repo into `~/.claude/settings.json`:

   ```json
   {
     "model": "opus",
     "modelSettings": {
       "claude-opus-5-5": { "effortLevel": "medium" }
     },
     "worktree": { "baseRef": "head" }
   }
   ```

   - `model: "opus"` resolves to Opus 5.5 on the Anthropic API, Claude Platform on AWS, Bedrock and Google Cloud; on Microsoft Foundry it is still Opus 4.6. Write `"claude-opus-5-5"` to pin the version.
   - Effort for Opus 5.5 lives under `modelSettings`. A top-level `effortLevel` in the user settings does not apply to Opus 5.5 (it is the older form and still applies to earlier models). `/effort <level>` saves the level there too. `CLAUDE_CODE_EFFORT_LEVEL` beats every setting.
   - `worktree.baseRef: "head"` makes agent worktrees branch from the current HEAD. The default `"fresh"` branches from the remote default branch, and an implementer would never see the contracts committed on the session branch.
3. Optional: `CLAUDE_CODE_SUBAGENT_MODEL` in the `env` block sets the model for agents that are given none. Without it they inherit the main session's model. Precedence: the `model` of an `Agent` call, then the agent file's `model`, then this variable, then the main session.
4. Check: start a session in a repo. `/model` shows Opus 5.5, `/agents` lists the `acme-dev:*` agents, and the index is the first thing in the context.

## Models

| Model | ID | Price in / out per million tokens | Role here |
|---|---|---|---|
| Opus 5.5 | `claude-opus-5-5` | $4 / $20 | Orchestrator, implementer, reviewer |
| Sonnet 5 | `claude-sonnet-5` | $2 / $10 | Researcher, summaries, long reading |
| Haiku 4.5 | `claude-haiku-4-5` | $1 / $5 | Mechanic: edits with an exact spec. 200K context, no effort levels |
| Fable 5.1 | `claude-fable-5-1` | $10 / $50 | The most capable model. Only when the user asks for it or Opus 5.5 at `high` measurably failed |

Prices are the Anthropic API list prices; a subscription counts usage
differently. The `sonnet` alias resolves to Sonnet 5 only on the Anthropic
API; on Bedrock and Google Cloud it is still Sonnet 4.5.

## Effort

- Opus 5.5 supports `low`, `medium`, `high`, `xhigh`, `max`, and defaults to `medium`. Anthropic reports that at `medium` it matches or beats Opus 5 at `high` on coding and knowledge work, and that `low` comes close on several coding evaluations at much lower cost.
- At the same level, Opus 5.5 thinks more per turn than Opus 5. An effort level carried over from Opus 5 costs more than it did.
- Thinking cannot be switched off on Opus 5.5. Effort is the control for depth, latency and cost. Lower the effort before adding "be brief" or "think less" to a prompt; it works more reliably.
- `xhigh` and `max` only where a measured gain justifies them. `max` applies to the current session only unless it comes from the environment variable.

| Role | Model | Effort |
|---|---|---|
| Orchestrator | Opus 5.5 | `medium`; `high` for a hard design session |
| Implementer | Opus 5.5 | `medium` |
| Reviewer | Opus 5.5 | `high` |
| Researcher | Sonnet 5 | `high` |
| Mechanic | Haiku 4.5 | none, Haiku has no effort levels |

TODO: The company's cost line, for example "a run expected to spawn more than N agents asks first".

## Do it yourself or delegate

Do it in the main session:

- A question answered from one or two files you know.
- An edit under an hour in files already in context.
- Anything that needs the user halfway through.

Delegate:

- Reading many files or pages for one conclusion: `acme-dev:researcher`, or `Explore` for a code search.
- Parts that touch disjoint files against a frozen contract: `acme-dev:implementer`, one per part, in worktrees.
- A change stated as a rule: `acme-dev:mechanic`.
- The integrated diff before the pull request: `acme-dev:reviewer` through `/acme-dev:review`.
- A second opinion, or reproducing a bug from the description alone: a fresh agent that did not see your reasoning.

A fresh agent starts with an empty context and gets only its brief. A
`fork` inherits the whole conversation; use it when the child needs what was
said, not just what is in the repo.

## The loop

1. Restate the goal and what done means in two lines. Ask only for decisions the user owns (rule 4 of the index); decide the rest and say what you decided.
2. Read enough to cut the work: `AGENTS.md`, `docs/HANDOFF.md`, the modules involved. Send wide reading to a researcher.
3. Decide whether to fan out (`acme-subagents`, "When to fan out"). Most tasks do not.
4. Freeze the contracts on the session branch and commit them.
5. Write the briefs and spawn the agents in one message so they run concurrently, in the background.
6. While they run, do orchestrator work: the next brief, the docs, the handoff. Do not redo their work and do not guess their results.
7. Read each report as a claim. Check the evidence (the check list output, the diff). Send open items back to the same agent with `SendMessage`, at most twice, then take the rest over.
8. Integrate on the session branch and run the full check list once, in one checkout.
9. Run `/acme-dev:review`, fix what it confirms.
10. Report: blocked on the user, what changed, per agent what it built and left, the check list result, the pull request link, what nobody could verify.

## Limits

- A background agent cannot ask the user anything. A brief that needs a decision is not ready.
- More implementers mean more merge work, not proportionally more speed. Three to five parallel parts is a sensible ceiling for one integrator.
- Claude Code also has agent teams and dynamic workflows (a scripted fan-out of many agents, switched by the `enableWorkflows` setting). They are for runs the user asks for explicitly; the loop above covers ordinary work.
- Judge cost per finished task, not per token. A cheaper model that needs a second round is not cheaper.
