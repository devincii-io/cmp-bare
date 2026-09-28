---
name: acme-howto
description: Runbooks for recurring tasks at Acme, one recipe each. Install the plugin on a machine, make the template your own, release a plugin change, run the plugin evals, start and end a work session. Invoke when asked how to do one of these, or when a task matches a recipe title.
---

# How-to runbooks

Each recipe is the shortest path that has worked. When a step fails, fix the
recipe in the same change.

## Install the plugin

Claude Code:

```
claude plugin marketplace add <absolute path to the marketplace repo, or owner/repo on GitHub>
claude plugin install acme-dev@acme-claude-marketplace
```

Then merge `install/claude-settings.json` into `~/.claude/settings.json`
(what each key does is in `acme-orchestrator`) and restart the session. The
index appears at the top of the context and `/agents` lists the four
`acme-dev:*` agents.

Codex: `codex plugin marketplace add <absolute path>`, then
`codex plugin add acme-dev@acme-claude-marketplace`. `~/.codex/config.toml`
needs `[features] hooks = true`; open `/hooks` in a session and trust the
SessionStart hook once. Until then, `$acme-dev` loads the index by hand.

Cursor: copy `plugins/acme-dev` to `~/.cursor/plugins/local/acme-dev` and
reload the window. A symlink out of that folder does not load. The index
arrives through the always-on rule in `rules/`.

## Make the template your own

1. `python tools/check.py rename <prefix> "<Company Name>"`. It replaces the prefix `acme` and the name `Acme` in every file and path.
2. `python tools/check.py --fix`, then `python tools/check.py` must print `ok`.
3. `python tools/check.py todo` lists the placeholders. Fill them, starting with the index and `acme-rules`. Delete a section rather than leave it empty.
4. Set the owner, e-mail and repository URL in the manifests.
5. Release it (next recipe) and install it.

## Release a plugin change

1. Edit the skill, agent or hook under `plugins/acme-dev`.
2. `python tools/check.py bump X.Y.Z` sets the version in every manifest and regenerates the Cursor rule. `python tools/check.py` must print `ok`.
3. `claude plugin validate .` and `claude plugin validate plugins/acme-dev`.
4. Commit and push.
5. `claude plugin update acme-dev@acme-claude-marketplace` and restart the session. Codex: `codex plugin add` again, and trust the hook again if it changed. Cursor: copy again.

Without the version bump the change does not ship; plugin updates are version-gated.

## Run the plugin evals

Before a release that changes a skill description, an agent's model or
effort, or the index. From `plugins/acme-dev`:

```
claude plugin eval . --model opus --judge-model sonnet -j 4 --max-cost-usd 10
```

Each case runs with and without the plugin; the difference is what the
plugin adds. A failing `skill-fired` grader means the skill's description
does not match how people ask; fix the description, not the case. Prefer
regex graders where the check is a fact. Results land in `evals/results/`,
which git ignores. Runs cost model usage and are not part of CI.

## Start and end a work session

`/acme-dev:start <topic>` and `/acme-dev:end` in Claude Code, `$start` and
`$end` in Codex. Before the pull request, `/acme-dev:review` runs the
reviewer agent on the branch.

TODO: The company's own runbooks: deploy, database migration, secret rotation, new machine.
