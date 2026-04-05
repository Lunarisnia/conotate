# Conotate

Your codebase is too big to hold in your head. Conotate helps Claude hold it for you.

Conotate is a Claude Code skill plugin that generates and maintains structured
knowledge bases for any part of your codebase — so you can ask Claude about
your auth module, your UI components, or your data pipeline without pasting
in mountains of code every time.

## The Problem

When you're working with a large codebase, Claude only knows what's in the
conversation. That means you're either pasting files constantly, or hoping
Claude can figure it out from a vague description. Neither scales. Conotate
gives you a better way: teach Claude about a domain once, then load that
knowledge whenever you need it.

## How It Works

Conotate gives you two skills:

**`/explore-domain`** — Point it at a folder or domain in your codebase.
Claude will explore it thoroughly and generate a structured knowledge file
covering: overview, architecture, data flows, patterns & conventions, and
gotchas. Run it again later and it only updates what changed.

**`/read-knowledge`** — Load one or more knowledge files into your
conversation. Use the domain path, a slug, or just describe what it does —
Conotate will figure out which file you mean.

Knowledge files live in `docs/conotate/` and are plain markdown — readable
by humans, optimized for Claude.

## Walkthrough

### Generate a knowledge base

Run `/explore-domain` and tell Claude which part of your codebase to document:

> `/explore-domain src/auth`

Claude will explore the folder and write a knowledge file to
`docs/conotate/src-auth.md`, structured like this:

```
## src/auth: Overview
Handles user authentication and session management...

## src/auth: Architecture
src/auth/
├── index.ts         — public API
├── session.ts       — session lifecycle
└── middleware.ts    — Express middleware
...

## src/auth: Gotchas
Sessions are invalidated on password change but not on email change...
```

### Load it later

In any future conversation, just say:

> `/read-knowledge auth`

Conotate resolves "auth" to `src-auth`, loads the file, and Claude
is immediately up to speed — no copy-pasting required.

### Keep it fresh

When your code changes, run `/explore-domain src/auth` again.
Conotate detects what changed via git and only regenerates the
affected sections.

## Installation

Conotate is a Claude Code skill plugin.

### Via Claude Marketplace

```
/plugin install conotate
```

### Via GitHub

If Conotate isn't in the official marketplace yet, install it directly
from GitHub using Claude Code's custom marketplace feature:

```
/plugin marketplace add https://github.com/Lunarisnia/conotate
/plugin install conotate@conotate-dev
```

That's it — `/explore-domain` and `/read-knowledge` will be available
in any Claude Code session.

## Requirements

- [Claude Code](https://claude.ai/code) (CLI, desktop, or IDE extension)

## Contributing

Contributions are welcome! Feel free to open an issue or pull request on
[GitHub](https://github.com/Lunarisnia/conotate).

## License

MIT — see [LICENSE](./LICENSE)
