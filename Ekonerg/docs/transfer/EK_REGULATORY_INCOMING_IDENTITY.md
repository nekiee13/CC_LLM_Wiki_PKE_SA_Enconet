# Ekonerg regulatory files in `incoming/` — identity check

**Status:** Inventory only. No source intake, extraction, approval record, or audit result.

The owner stated on 2026-09-30 that valid versions of 10 CFR 50 Appendix B and
ASME NQA-1 are in `Ekonerg/incoming/`. This note records the files found there.
It does not decide which clauses apply to Ekonerg or approve an audit finding.

| File in `incoming/` | Bytes | SHA-256 |
|---|---:|---|
| `10CFR_Part 50_-_Appendix_B.md` | 20,932 | `b06bf6d7fbc8d92e122bbb3dd7efc5088842141127f2717e3ea6de976612c396` |
| `ASME_NQA-1_000-013_Preface.md` | 40,750 | `7df1e41b51d5618c1afe404ee89c2396e0c907e5efd768a09a480d593c0aa6be` |
| `ASME_NQA-1_014-046_Part_1.md` | 110,025 | `8e26ceadaf42cdedbee5505268b3610b2a33951c4b7d01626df7d0522a32d41b` |
| `ASME_NQA-1_047-128_Part_2.md` | 373,066 | `50bb4b0291e185f2d949556c6e03d507c31922d7818988b22747ad66c6764322` |
| `ASME_NQA-1_129-206_Part_3.md` | 318,221 | `a2cc79330bef84bd1323c102f06142ef1207b7db6092bad602ff09979d604f83` |
| `ASME_NQA-1_207-315_Part_4.md` | 698,868 | `0124984ff49898c6487b267fc298af5ca0e1757db36a08e03f8a6ecb070016e9` |

The NQA-1 preface names **ASME NQA-1–2015** and says it was issued on
February 20, 2015. The four Part files are the adjacent split files; this
inventory does not independently prove their edition or completeness.

The Appendix B file names the NRC Appendix B page as its source. The file does
not state a capture date or effective revision in its heading or footer. Its
hash identifies these exact local bytes. Record the source snapshot date, if
known, in the later controlled intake record; do not invent one here.

**Next gate:** Finish the clean framework and its review. Before audit use,
register each source with its approved identity and hash under the Ekonerg
intake process. Keep these owner files in `incoming/` unchanged until then.
