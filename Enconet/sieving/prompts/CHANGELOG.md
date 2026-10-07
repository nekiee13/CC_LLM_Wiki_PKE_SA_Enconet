# Sieving prompt registry

Every prompt version must be recorded here before use. Promotion and rejection entries
must name the golden-set score, decision reference, and deposited skill lesson.

| Version | Side | Date | Change and reason | Golden score | Decision | Decision reference | Skill lesson |
|---|---|---|---|---|---|---|---|
| `appb_rule_v1` | RULE | 2026-07-13 | Baseline authority-aware Appendix B extraction prompt | pending pilot golden set | baseline | n-a | seed rules in `crumb-quality` |
| `appb_document_v1` | DOCUMENT | 2026-07-13 | Baseline supplier-evidence extraction prompt | pending pilot golden set | baseline | n-a | seed rules in `crumb-quality` |
| `appb_document_v3_context_anchors` | DOCUMENT | 2026-10-07 | Candidate high-recall method with direct/concept passes and exact chapter-linked quotes; local Nuclear QA Plan sample prepared | 20-example manual draft self-check only; not independent prompt evaluation | pending local golden review and context storage compatibility | n-a | No promotion lesson yet; do not equate keyword leads with crumbs or a self-check with measured recall |

No later version may be marked promoted or rejected without a human decision and a linked
lesson in `sieving-run`, `crumb-quality`, or `sieving-tuning`.
