# EF-1.2 reading-route review packet

Codex made 31 local work copies from the owner-supplied `incoming/` set.
Each copy matches its pinned source hash. A repeat apply preserved all 31
copies without replacing them. The originals were not edited.

`Ekonerg/tools/fast_audit_copy.py` previews by default. It checks the full
registered set before copying and refuses a changed source, new unregistered
file, unsafe path, or conflicting work copy. It writes only below the chosen
Ekonerg run folder. Six focused fake-company tests passed, including names
with spaces and Croatian letters, with and without a sibling project. The
full Ekonerg tool suite passed 117 tests.

A synthetic quote test checked source ID, heading, line range, and exact text.
A live locator check matched SRC-002, its Introduction heading, and line 9
of the Appendix B work copy. This proves a reading route, not an audit claim.

The local setup log is
`Ekonerg/work/fast_audit/EF-20261001-01/EF_1_2_SETUP.md`.
Its source copies and register are ignored by Git and are available in
the shared local workspace. They are not a tested backup. Existing workspace
access rules apply; controlled storage, backup, G1 intake, and Claude review
remain open. No extraction tool was needed; direct Markdown reading works.

Reviewer: Claude. Please check copy safety, retry and conflict behavior,
cross-company isolation, exact quote lookup, and the G1 boundary.
