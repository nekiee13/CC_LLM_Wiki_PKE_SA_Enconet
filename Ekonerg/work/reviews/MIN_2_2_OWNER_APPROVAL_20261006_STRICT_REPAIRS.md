# MIN-2.2 owner approval — strict quote repairs

**Date:** 2026-10-06  
**Decision:** Owner approved use of the corrected source copy.

The approval applies to the two explicit pending generation decisions in the
strict raw-source repair request:

| Document | Candidate | Replaces | Decision reference |
|---|---|---|---|
| DOC-0019 | `RUN-20261003-16` | `RUN-20261003-14` | `REPAIR-DOC0019-GEN2-20261006-OWNER` |
| DOC-0011 | `RUN-20261005-52` | `RUN-20261005-51` | `REPAIR-DOC0011-GEN3-20261006-OWNER` |

The candidates preserve the crumb meaning and replace only the stored quote
with source-exact text. The approval is for traceability repair. It is not an
Appendix B conformity judgment and does not change the audit score by itself.

Promotion still uses the controlled `sieve_generation.py promote` command. If
another machine gate (such as a missing golden score or downstream-evidence
lock) refuses promotion, the refusal must remain recorded; no direct database
edit is allowed.
