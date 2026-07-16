# {{PROJECT_NAME}} support recordkeeping

| Class | Mutation rule |
|---|---|
| Controlled | Reviewed edit or controlled superseding version |
| Immutable | Never edit after publication; create a correction/successor |
| Append-only | Append events; correct by referencing a prior event |
| Replaceable | Replace validated current view; retain Git/log evidence |
| Curated ledger | Preserve identity, evidence, and state transitions |
| Generated | Regenerate from authority; never hand-treat as history |
| Historical | Retain as non-current context with successor link |

Use UTC timestamps and stable IDs. Records must not contain secrets, credentials, personal data,
private path values, or product data prohibited by `{{SUPPORT_PROFILE_PATH}}`.

States and validation outcomes are literal. Unknown, unavailable, skipped, blocked, not-run, and
not-configured are not synonyms for passed.
