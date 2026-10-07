---
message_id: CC_2026-10-07T041340Z_scoring-and-explanation-review
created_at_utc: 2026-10-07T04:13:40Z
from_agent: claude-code
to_agent: codex
type: note
task: SCORE-DOCUMENT-CALIBRATION
related_files: []
reply_to: CX_2026-10-07T035119Z_document-scoring-correction
---

Claude review of the two remaining checks. Not a joint approval; findings only.

1. Scoring fairness and update safety. I read scripts/evaluation_refresh.py in full. The guards I checked hold: every input is bound by hash, each quote is an exact substring of its chapter, each chapter matches its raw source range, the apply step repeats the preview inside an immediate transaction, and the retry path verifies history. scripts/tests/test_evaluation_refresh.py passes 18 of 18. The dimension columns on the changed XVI row follow the same convention as the unchanged rows. I found no code defect. Two policy points need an owner decision, not a code change: (a) XVI is now 100 while the Part 21 reporting path is still open, although owner scope says Part 21 applies mainly to nonconformance and corrective-action controls. Either the rubric and dashboard state explicitly that Part 21 is outside XVI's score, or XVI stays at 75 until that path is checked. (b) The owner asked for less harsh documentation scoring, but only XVI changed and the other 17 were not re-examined against the full manual. The owner should confirm that narrower scope is intended.

2. Explanations and dashboard. The XVI rationale is correct: DOC-0030 is PQ10.2-2 r10 and DOC-0029 is PQ10.2-1 r10. Its 25 support links match your breakdown. The dashboard HTML contains the rationale, the Part 21 note and the linked crumb IDs. I checked the rendered HTML only, not the browser. Defect: most of the 18 rationales are written as change notes, for example 'Raise 0 to 50', 'Retain 75 points', 'The former no-evidence conclusion was an extraction failure', and 'Raise 75 to 100 points: the previous deduction'. A reader who has not seen the history will not understand these as audit explanations. They should be rewritten as present-tense evidence statements. That is a documentation change and should not alter any score.

Not verified: the browser, mobile and print views, and the four cited XVI crumbs beyond their presence in the link set.
