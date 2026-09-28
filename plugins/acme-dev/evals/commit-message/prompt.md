---
description: A commit message is a sentence subject plus a why body, without attribution or type prefix.
tags: [readonly]
max_turns: 6
allowed_tools: [Read, Glob, Grep, Skill]
---

Write the commit message for this change: I renamed getUser to fetchUser in the three call sites, because the old name hid that it makes a network call.
