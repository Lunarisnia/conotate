---
name: hello-name
description: Greets with a random name by running a bundled Python script. Use to test skill+script integration.
allowed-tools: Bash(python *)
---

Run the random name script and greet the result:

1. Run: `python ${CLAUDE_SKILL_DIR}/scripts/random_name.py`
2. Capture the output as `<name>`
3. Print: `Hello, <name>`
