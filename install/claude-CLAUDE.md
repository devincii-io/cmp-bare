# Global context

## Machine

TODO: Operating system and default shell, with the traps an agent hits there
(PowerShell 5.1 has no `&&`; `python3` may be a store alias). The installed
tools that matter: language runtimes, package managers, container runtime,
`gh`. Cloud accounts and profiles by name, never keys.

## Conventions

Everything about how Acme develops software is in the `acme-dev` plugin. Its
index is injected at session start; the other skills are
`/acme-dev:<name>`, listed in the index. A repo's `AGENTS.md` beats the
plugin for that repo. When the index is missing from the context, invoke
`/acme-dev:acme-dev` first.

This session is the orchestrator. Delegate wide reading and parallel
building to the `acme-dev:*` agents as `acme-orchestrator` describes.

Apply the `unslop` skill (shipped in `acme-dev`) to text other people read:
docs, commits, comments, customer text.
