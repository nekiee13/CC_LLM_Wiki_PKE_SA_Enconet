# EK-1.2 candidate: local draft gap workflow

This slice copies two scripts from one versioned template. `gap_register.py`
previews a gap by default. `--apply` writes one gap and, when its status is
`missing-evidence`, one linked draft action in a single database transaction.
The caller must state the action type and description; the tool does not guess
them from document text. A matching retry preserves the records, while a
different record or progressed action is refused.

`validate_gaps.py` reads the local database only. It checks evidence pointers,
missing-evidence actions, criterion links, run links, and foreign keys. Its
PASS means the structure is sound, not that evidence is true or approved.
It does not append an audit approval or validation log row by itself.

Synthetic tests use two fake companies, including spaces and a Croatian
character, with and without a sibling project. They check preview, apply,
retry, conflict refusal, missing and foreign databases, foreign record paths,
transaction safety, draft-only action state, and a validator failure when an
action is removed. A fake nested old-project folder also stays unchanged.
An injected action-insert failure proves the gap insert rolls back too.
Ekonerg's real database and source intake remain absent.
No owner document in `incoming/` is read or changed. Claude review is pending;
EK-1.2 remains open.
