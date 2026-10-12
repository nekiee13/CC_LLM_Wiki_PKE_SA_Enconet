---
record_type: exact_render_evidence
target: CC_Loto
slice: codex-guidance-vocabulary-correction
target_parent: d5dc65e568ee73d82389e6e1d3fdf24122661adf
recorded_at_utc: 2026-07-20T03:02:47Z
target_write: none
---

# CC_Loto Codex guidance correction — exact render evidence

The renderer reads committed `d5dc65e:AGENTS.md`, requires parent object `34b7eb93`, replaces one
exact defective enumeration, and preserves the separate blocker warning. It emitted:

| Artifact | SHA-256 | Git object | Bytes |
|---|---|---|---:|
| `rendered/loto-codex-guidance-correction/AGENTS.md` | `44E3AC42AC2A6F0BDB01777972C0F14EB473200A6693163213A2EB0C0F9AA2AC` | `42571a2c5f67b5a11759f38d7d65f50f156087c3` | 8355 |
| `rendered/render_loto_codex_guidance_correction.py` | `1EF6756FD400A62F7C5BEF186ACD2C50B0D714ADB0DE78412F96DDF88D16701A` | n/a | n/a |

The candidate-to-parent diff is exactly 3 additions, 2 deletions in `AGENTS.md`. It adds the
canonical seven check states and the explicit rule that `blocked` is a handoff/blocker state, never
a check result. The line-129 warning remains byte-present exactly once. `CLAUDE.md` stays pinned to
object `3edd8750` and is never written by the renderer.

Two render outputs matched byte-for-byte after removal of two accidental trailing blank lines from
the initially assembled Wiki copy. The renderer-derived 8355-byte output is the sole authority.
