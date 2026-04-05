# explore-domain Skill — Design Spec

**Date:** 2026-04-02
**Status:** Approved

---

## Overview

A Claude Code skill that analyzes a locally scoped folder or domain within a codebase and generates a structured markdown knowledge base file. Designed to be invoked interactively, domain by domain, rather than across an entire repo at once. Output files are manually fetched via script when needed — not auto-loaded into context.

---

## Invocation

- **Skill name:** `explore-domain`
- **Mode:** Interactive — the skill asks the user which folder/domain to analyze at the start
- **Example prompt:** *"Which folder or domain do you want to analyze?"* → user replies `src/auth`

---

## Output Location

All knowledge base files are written to:

```
docs/conotate/<domain-slug>.md
```

relative to the repo root where the skill is invoked. The domain slug is derived from the target path by replacing `/` with `-`:

- `src/auth` → `docs/conotate/src-auth.md`
- `packages/ui/components` → `docs/conotate/packages-ui-components.md`

---

## Knowledge Base File Structure

Each file follows a fixed template with domain-prefixed headings for reliable script extraction:

```markdown
<!-- domain: src/auth -->
<!-- generated: 2026-04-02T10:00:00Z -->
<!-- commit: abc1234 (optional, omitted if no git) -->

# src/auth: Knowledge Base

## src/auth: Overview
1-2 paragraph summary of what this domain does and why it exists.

## src/auth: Architecture
Directory tree + role of each key file/folder. Entry points called out explicitly.

## src/auth: Data Flows
How data moves through this domain — inputs, transformations, outputs.
Sequence descriptions for key operations.

## src/auth: Patterns & Conventions
Recurring patterns, naming conventions, abstractions used consistently across the domain.

## src/auth: Gotchas
Non-obvious behaviours, known quirks, things that have caused or could cause bugs.

<!-- end:src/auth -->
```

### Design rationale for domain-prefixed headings

Every `##` heading is prefixed with the domain name (e.g. `## src/auth: Overview`). This allows:

1. **Unambiguous section extraction** across concatenated multi-domain files
2. **Token trimming** — a script can strip the prefix before passing to Claude: `sed 's/## src\/auth: /## /g'`

### Delimiter

Each file ends with `<!-- end:<domain> -->`, mirroring the opening `<!-- domain: -->` header. Enables reliable block extraction when files are concatenated:

```bash
sed -n '/<!-- domain: src\/auth -->/,/<!-- end:src\/auth -->/p' combined.md
```

### Metadata header

- `<!-- generated: -->` — ISO 8601 timestamp of last generation
- `<!-- commit: -->` — git SHA at time of generation (optional; omitted if git is not available)

---

## Generation Mode (New File)

When no existing knowledge base file is found for the target domain:

1. Explore the target directory using the `Explore` agent
2. Populate all five sections from scratch using the fixed template
3. Write to `docs/conotate/<domain-slug>.md`
4. Include metadata header (with commit SHA if git is available)

---

## Update Mode (Existing File)

When a knowledge base file already exists:

1. Read `<!-- commit: -->` from the existing file
2. If commit SHA is present: run `git diff <sha> HEAD -- <target-dir>` to identify changed files
3. If no commit SHA (or no git): fall back to comparing file modification times against the `<!-- generated: -->` timestamp
4. Map changed files to affected sections:

| Change type | Sections to rebuild |
|---|---|
| New or deleted files | Architecture |
| Changed logic files | Data Flows, Gotchas |
| Changed config / conventions | Patterns & Conventions |
| >50% of files changed | Full regeneration |

5. Re-explore only the affected files
6. Rewrite only the affected sections in-place
7. Update the metadata header (`generated` timestamp and `commit` SHA)

**Edge case — no change signal:** If neither git nor mtime can determine what changed (e.g. fresh clone with no commit header), prompt the user: *"Can't determine what changed — do a full regeneration or skip?"*

---

## Skill Implementation

### Location

```
skills/explore-domain/
  SKILL.md           # Main skill document
  template.md        # Blank section template for generation
  section-map.md     # Reference table: file change type → sections to rebuild
```

### Allowed tools (frontmatter)

```yaml
allowed-tools:
  - Read
  - Write
  - Edit
  - Glob
  - Grep
  - Bash(git diff*, git log*, git rev-parse*)
  - Agent(Explore)
```

### Skill type

**Technique** — concrete steps to follow. Standard application scenario testing is sufficient (no pressure-testing required).

---

## Fetching Script (out of scope for this skill)

The skill does not include the fetching script — that is a separate concern. The file format is designed to make script authoring trivial:

- Extract a full domain block: `sed -n '/<!-- domain: X -->/,/<!-- end:X -->/p'`
- Extract a single section: `awk '/^## X: Data Flows$/,/^## X:/' file.md`
- Strip domain prefixes before sending to Claude: `sed 's/## X: /## /g'`
