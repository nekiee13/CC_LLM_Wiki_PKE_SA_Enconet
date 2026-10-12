# MIN-2.2: owner golden approvals

The owner approved the two scope-two golden fixtures. This confirms that the
listed crumbs and exact source quotes are the expected sieve answers for the
two documents. It does **not** promote either database generation and does not
decide Appendix B conformity.

| Document | Fixture | Approval reference | Fresh candidate | Score |
|---|---|---|---|---|
| DOC-0016 | `manifest_document_doc0016_v3_scope2_draft_20261006.yml` | `GOLDEN-DOC0016-V3-SCOPE2-20261006-OWNER` | `RUN-20261006-67` | 28 found, 0 missed, 0 spurious; promotion-ready |
| DOC-0021 | `manifest_document_doc0021_v3_scope2_draft_20261006.yml` | `GOLDEN-DOC0021-V3-SCOPE2-20261006-OWNER` | `RUN-20261006-68` | 21 found, 0 missed, 0 spurious; promotion-ready |

The score was run without `--allow-draft`, using the approved fixtures and the
exported fresh candidates. The active generations remain `RUN-20261004-49`
and `RUN-20261004-42` until the owner records a separate generation decision.
