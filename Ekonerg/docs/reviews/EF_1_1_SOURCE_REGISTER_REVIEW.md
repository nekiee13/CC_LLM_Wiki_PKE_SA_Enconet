# EF-1.1 source-register review packet

Codex prepared a local, ignored source register for the 31 owner-supplied
Markdown files in `Ekonerg/incoming/`. Each file has a stable ID, full relative
path, byte count, SHA-256 hash, source role, language, and stated edition or
revision. The files total 1,851,547 bytes. A live recheck found no missing,
empty, duplicate, unreadable UTF-8, or changed files in the register. The
register SHA-256 is
`f0b62b19a989ec9960d39df56181c34d6821be3d050ffd4c37b0beb64c516662`.

What needs care:

- The supplied NQA-1 preface says 2015. The five file-name page spans run in
  order, but that alone does not prove that all pages or editions match.
- The two NRC Markdown files lack a capture or effective date in the checked
  headings. Their exact bytes are recorded for traceability.
- Twenty-six files link to image assets not present in Ekonerg. A claim that
  needs an image must wait for the original asset or source.
- Part 21 is listed as supplied context. Its audit role is still open. Its
  presence does not add a new audit duty.
- The owner's source statement and request to process the files are recorded.
  The formal G1 source-set decision is not yet recorded.

The full register, issue notes, and check log are local in
`Ekonerg/work/fast_audit/EF-20261001-01/`. Source text and local work copies
are not committed. The next task, EF-1.2, tests safe direct reading from
byte-identical copies. Draft reading can start without calling G1 approved.

Reviewer: Claude. Check the identity method, open issues, and G1 boundary.
