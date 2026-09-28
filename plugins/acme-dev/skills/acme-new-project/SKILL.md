---
name: acme-new-project
description: Recipe for starting a new Acme project. The questions to ask before writing anything, the scaffold, the files every repo starts with, and the done-checklist. Invoke when asked to create, scaffold or bootstrap a new service, tool, library or website.
---

# A new project

## Ask first

Before any scaffold, ask what the request does not say. Do not invent the
answers.

- Whose is it: the company's own or a customer's? Who operates it afterwards?
- What kind: service with a database, command-line tool, library, website?
- Where does it run, and which container runtime, if any?
- Which data does it hold, and is any of it personal?
- What does done look like for the first version?

TODO: Company-specific questions, for example the domain and DNS for a website or the customer's IT contact.

## Scaffold

TODO: The command that creates the project for the default stack (see `acme-stack`), and the packages every project starts with.

## First commit

Every repo starts with:

- `.gitattributes` with `* text=auto eol=lf` and binaries listed
- `.gitignore`, including `.env` and `.claude/worktrees/`
- `README.md`: what it is, how to run it, what it deliberately does not do
- `AGENTS.md` from the template in `acme-agent-files`
- a CI workflow that runs the check list
- `.env.example` when the project reads configuration from the environment

No licence file until one is decided; that is the user's call.

## Done when

- The check list passes locally and in CI.
- `README.md` and `AGENTS.md` describe the real commands, not planned ones.
- Anything never run is marked UNVERIFIED with the reason.
- The repo has a remote. A repo without one is a single copy on one disk; say so.
