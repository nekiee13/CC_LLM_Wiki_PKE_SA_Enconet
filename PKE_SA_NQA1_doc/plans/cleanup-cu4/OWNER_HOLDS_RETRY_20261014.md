# Owner cleanup-hold retry

Decision: OWNER-CLEANUP-HOLDS-RETRY-20261014.

Owner request: "try again on remaining known holds (Ekonerg's outputs/candidates
WinError 5 tree, old doc/ retained files, legacy pytest scratch)."

Continue the existing CU-4.2 cleanup, not a new task. Retry the previously
authorized Ekonerg directory batch without changing ACLs. Move eight eligible
workspace support files to the corresponding PKE_SA_NQA1_doc homes, with exact
hash/identity checks and tested undo. Preserve the four unfinished owner edits
byte-for-byte and unstaged at their new paths; stage only original index blobs.
Do not rewrite those documents or run the historical external-project generator.
Old generator path strings remain historical, not a promise that it is runnable.

Retain proved empty legacy scratch trees under .tmp, including only symbolic
shortcuts that point to captured directories inside their own original tree.
Never follow redirects. Retain their absolute target strings unchanged; these
are historical shortcuts, not runnable aliases at the archive location.
Do not move populated/unknown scratch or any tree containing Claude-owned files.

Claude review deferral remains the owner's existing instruction; no new
pre-execution approval is claimed. Request post-execution review through the
neutral coordination channel. Claude must handle its seven retained doc files
and any protected test-fixture trees. This is no ownership override, permission
takeover, recursive-deletion authority, audit reset or audit-data change.
