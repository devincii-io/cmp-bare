---
name: acme-rules
description: The Acme development rules with their reasons, grouped by architecture, dependencies, errors, data, security, testing, style, delivery and agents. Invoke before designing a module, adding a dependency, choosing an error strategy, writing tests, or when a rule in the index needs its reason.
---

# Development rules

Starter set, version 0.1. Every rule has a reason, because a rule without a
reason gets argued away in the next session. Change a rule here, with a new
version line, never silently in a repo. The TODO lines are slots for the
company's own rules; delete the ones that do not apply.

## Architecture

1. One deployable and one database until a second one has a written reason. Reason: every extra moving part is one more thing that fails at night.
2. Business rules live in pure functions: no ORM, no framework, no clock inside. Reason: the rules are what the customer pays for; they must be testable without a server.

TODO: The default runtime, hosting and container setup, or the sentence "ask before choosing".

## Dependencies

3. Standard library first. A dependency enters when it replaces more than it costs. Reason: every dependency is a future upgrade and a supply-chain risk.
4. Lock everything and install from the lockfile in CI. Reason: a build that resolves a different tree than the one tested is not the tested build.
5. No external service without a written reason in an ADR: where the data goes, what it costs, who signs. Reason: each service is money, a second place for data, and a contract.

## Errors and logging

6. Fail loudly at boundaries, never swallow an exception. Reason: a swallowed error surfaces weeks later as wrong data.
7. Logs carry what, when, version and stack trace, never personal data. Validation errors never echo the submitted body. Reason: more people read logs than the database, and a body can hold a password.

## Data

8. Every schema change is a migration; nobody edits a database by hand. Reason: a database that drifts from the code cannot be recovered.
9. Timestamps are stored in UTC and shown in local time. Reason: time zones and DST break every comparison otherwise.
10. A backup that was never restored does not exist. Reason: the first restore must not be the emergency.

TODO: Which records are append-only (money, stock, evidence) and how a correction is written.

## Security

11. No secret in a repo, ever. `.env` is gitignored, `.env.example` lists the variables. Reason: git history is forever and the repos are read by agents.
12. Validate at the boundary once, trust inside. Least privilege per role. Reason: validation scattered through the code is missing somewhere.

## Testing

13. Every behaviour change gets a test; a boundary case is a test, not a comment. Reason: the suite is the specification.
14. Run the full check list before saying anything is done; CI runs the same list. Reason: "it works here" is not a state anyone can install.
15. Something never executed is marked UNVERIFIED in the docs, with the reason. Reason: the most useful section of a README is the one that says what was never run.

## Style and documentation

16. Comment the non-obvious constraint and the rejected cheaper option, never what the line says. Reason: comments that restate code are the first to go stale.
17. No em dashes, no curly quotes, in code, comments, docs or chat. Reason: they read as machine-written, and some consoles render them as question marks.
18. `README.md` says what it is and how to run it, `AGENTS.md` holds the repo's working rules and check list, `docs/HANDOFF.md` is session state, `docs/adr/` records decisions. Reason: four files with four jobs; a reader knows where to look.

TODO: Languages. Which language code, commits and dev docs use; which language customers and operators read.

## Delivery

19. Session branch, one pull request, CI green, merge. Never push or force-push `main`. Reason: a broken `main` blocks every other session, and every push to it costs CI minutes.
20. Commit messages carry no agent attribution. Reason: the history belongs to the company, not to a tool.

## Agents

21. The main session orchestrates; subagents read wide and build in parallel, and return conclusions. Reason: the orchestrator's context is the scarcest resource in a long run.
22. A subagent report is a claim. The orchestrator checks the evidence before accepting it. Reason: an agent that says "tests pass" may have run the wrong ones.
23. Keep going through steps that need no input; stop only for a decision from the list below, a failing check you cannot fix, or a destructive or external action. End a long run with what is blocked on the user, then what changed, then what was found. Reason: a run that stops after every milestone waits for an answer nobody was going to give.

## What the agent asks instead of deciding

Runtime and hosting, vendors and services, prices, licences, legal text,
publishing anything, deleting anything. Name the decision, give a
recommendation, wait.

TODO: Company-specific decisions that always go to a person.
