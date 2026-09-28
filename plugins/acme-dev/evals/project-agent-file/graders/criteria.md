---
type: llm
---

Judge the agent file shown in the reply.
PASS if its frontmatter `tools` list (or `disallowedTools`) leaves the agent without Edit and Write, and its description says when to use the agent.
FAIL if the agent could edit files, or no complete file is shown.
