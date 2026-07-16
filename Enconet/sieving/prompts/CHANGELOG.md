# Sieving prompt registry

Every prompt version must be recorded here before use. Promotion and rejection entries
must name the golden-set score, decision reference, and deposited skill lesson.

| Version | Side | Date | Change and reason | Golden score | Decision | Decision reference | Skill lesson |
|---|---|---|---|---|---|---|---|
| `appb_rule_v1` | RULE | 2026-07-13 | Baseline authority-aware Appendix B extraction prompt | pending pilot golden set | baseline | n-a | seed rules in `crumb-quality` |
| `appb_document_v1` | DOCUMENT | 2026-07-13 | Baseline supplier-evidence extraction prompt | pending pilot golden set | baseline | n-a | seed rules in `crumb-quality` |

No later version may be marked promoted or rejected without a human decision and a linked
lesson in `sieving-run`, `crumb-quality`, or `sieving-tuning`.
