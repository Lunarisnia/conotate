# Section Map

Reference table for update mode: maps changed file types to which sections need rebuilding.

| Changed files pattern | Sections to rebuild |
|---|---|
| New or deleted files | `<domain>: Architecture` |
| Modified logic/implementation files (`.ts`, `.js`, `.py`, `.go`, `.rs`, `.java`, etc.) | `<domain>: Data Flows`, `<domain>: Gotchas` |
| Modified config/convention files (`.json`, `.yaml`, `.toml`, `*.config.*`, `*.rc`, `*.env`) | `<domain>: Patterns & Conventions` |
| >50% of files in domain changed | Full regeneration (all sections + Overview) |
| Mixed changes across multiple types | Rebuild all affected sections (union of above) |

## Notes

- When in doubt, rebuild more sections rather than fewer — missing an update is worse than a redundant one.
- `Overview` is only rebuilt on full regeneration. It describes the domain's purpose, which changes rarely.
- Always update the metadata header (`<!-- generated: -->` and `<!-- commit: -->`) after any partial or full rebuild.
