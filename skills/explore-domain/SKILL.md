---
name: explore-domain
description: Use when you want to generate or update a structured knowledge base markdown file for a specific folder or domain in the codebase. Scoped to a single directory — not the whole repo.
allowed-tools: Read, Write, Edit, Glob, Grep, Bash(git diff*), Bash(git log*), Bash(git rev-parse*), Agent(Explore)
---

# explore-domain

Generates a structured knowledge base file for a locally scoped folder or domain. Output is written to `docs/knowledge/<domain-slug>.md` and designed for manual script-based fetching — not auto-loaded into context.

## Invocation

Ask the user:

> "Which folder or domain do you want to analyze? (e.g. `src/auth`, `packages/ui`)"

Derive the **domain slug** from the path by replacing `/` and ` ` with `-`:
- `src/auth` → `src-auth`
- `packages/ui/components` → `packages-ui-components`
- `animation system` → `animation-system`

Output path: `docs/conotate/<slug>.md`

## Mode Detection

Check if `docs/conotate/<slug>.md` already exists:
- **Not found** → [Generation Mode](#generation-mode)
- **Found** → [Update Mode](#update-mode)

## Generation Mode

1. Use `Agent(Explore)` to thoroughly explore the target directory — files, structure, responsibilities, data flows, patterns, quirks
2. Read the blank template from `${CLAUDE_SKILL_DIR}/template.md`
3. Get current timestamp (ISO 8601) and git SHA if available:
   - `git rev-parse HEAD` → use as `<sha>`; if git unavailable, omit the `<!-- commit: -->` line entirely
4. Replace all `<domain>` placeholders with the actual domain path (e.g. `src/auth`)
5. Populate all five sections from exploration results:
   - **Overview** — what this domain does and why it exists (1-2 paragraphs)
   - **Architecture** — directory tree with role of each key file/folder; call out entry points explicitly
   - **Data Flows** — how data moves through the domain (inputs → transformations → outputs); sequence descriptions for key operations
   - **Patterns & Conventions** — recurring patterns, naming conventions, shared abstractions
   - **Gotchas** — non-obvious behaviours, known quirks, things likely to cause bugs
6. Write the completed file to `docs/conotate/<slug>.md`
7. Generate a short 3–7 word description of the domain based on the exploration (e.g. "User authentication and session management")
8. Upsert `docs/conotate/domains.txt`:
   - File doesn't exist → create it with one line: `<description>:<slug>`
   - File exists, no line ending with `:<slug>` → append `<description>:<slug>` as a new line
   - File exists, line ending with `:<slug>` found → replace that line with `<description>:<slug>`
9. Confirm: print the output path

## Update Mode

1. Read `<!-- commit: -->` from the existing file header
2. Determine what changed:
   - **Commit present**: `git diff <sha> HEAD --name-only -- <target-dir>`
   - **No commit / no git**: compare `<!-- generated: -->` timestamp against file mtimes using `Glob` to list files, then `Bash(git log*)` to check recent history
   - **No signal at all**: ask the user — *"Can't determine what changed — full regeneration or skip?"*
3. Map changed files to sections using `${CLAUDE_SKILL_DIR}/section-map.md`
4. Re-explore only the affected files using `Agent(Explore)` with a focused prompt
5. Rewrite only the affected sections in-place using `Edit`
6. Update the metadata header: new `<!-- generated: -->` timestamp and `<!-- commit: -->` SHA
7. If the Overview section was rebuilt: regenerate the description and update the `:<slug>` line in `docs/conotate/domains.txt`
8. Confirm: print the output path and list of sections rebuilt

## Output Format

Each knowledge base file uses domain-prefixed `##` headings for reliable script extraction:

```
<!-- domain: src/auth -->
<!-- generated: 2026-04-02T10:00:00Z -->
<!-- commit: abc1234 -->

# src/auth: Knowledge Base

## src/auth: Overview
## src/auth: Architecture
## src/auth: Data Flows
## src/auth: Patterns & Conventions
## src/auth: Gotchas

<!-- end:src/auth -->
```

**Script extraction examples:**
```bash
# Extract full domain block
sed -n '/<!-- domain: src\/auth -->/,/<!-- end:src\/auth -->/p' docs/knowledge/src-auth.md

# Strip domain prefix before passing to Claude (reduces tokens)
sed 's/## src\/auth: /## /g' docs/knowledge/src-auth.md
```

## Supporting Files

- `${CLAUDE_SKILL_DIR}/template.md` — blank template for generation
- `${CLAUDE_SKILL_DIR}/section-map.md` — file change type → sections to rebuild
