---
name: crumb-quality
description: Review sieved crumb statements, item types, verbatim multilingual quotes, source locators, authority separation, and borderline Appendix B classification. Use when checking generated crumbs, tuning extraction prompts, or adjudicating criterion confusion.
---

# Crumb Quality

Read `sieving/SIEVING_PLAYBOOK.md`, `Sieving_method_specification_Guide.md`, and the
source chunk before judging. Require one atomic, auditable claim per crumb; verbatim
quotes and source locators must support that exact claim. Preserve the quote language
(`sl`, `en`, or `hr`) and never translate evidence. RULE crumbs may carry governing or
interpretive authority references; DOCUMENT crumbs must never acquire normative
authority.

Borderline-criterion decision table (seeded confusion pairs; grow from tuning lessons):

| Confusion pair | Choose the first when… | Choose the second when… |
|---|---|---|
| V / VI / XVII | V: work is performed to instructions/procedures/drawings with acceptance criteria | VI: the issue and change of prescribing documents is controlled; XVII: completed evidence is retained as records |
| IV / VII | IV: requirements are flowed down into procurement documents | VII: purchased items/services or the supplier's conformance is evaluated, inspected, or evidenced |
| X / XI | X: independent inspection verifies work or item characteristics | XI: a planned test demonstrates performance under specified conditions |

Reject or split a crumb when its statement spans unrelated controls, its quote only
implies rather than states the claim, its item type is unsupported by the statement, or
its classification depends on translated wording. Add new recurring confusion rules to
this table after prompt decisions and link the lesson from `sieving/prompts/CHANGELOG.md`.
