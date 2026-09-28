# Global context

## Machine

TODO: Operating system and default shell, with the traps an agent hits there.
The installed tools that matter.

## Conventions

Everything about how Acme develops software is in the `acme-dev` plugin from
the `acme-claude-marketplace` marketplace. Its SessionStart hook injects the
index; when the hook is not trusted yet or the index is missing, invoke
`$acme-dev` first. The other skills are `$acme-rules`, `$acme-stack`,
`$acme-repo`, `$acme-agent-files`, `$acme-new-project`, `$acme-howto` and
`$unslop`. A repo's `AGENTS.md` beats the plugin for that repo.

Apply `$unslop` to docs, commits, comments and customer text.

## Unattended runs

A scheduled `codex exec` gets no follow-up prompt: never block on a
question, never leave work half done, lead with what matters, no preamble.
