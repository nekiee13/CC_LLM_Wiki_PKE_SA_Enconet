# T1.3 — Gap, collision, sensitivity, and scale matrices

## Capability gap matrix

| Capability | CC_FIN | CC_Loto | Common transfer disposition |
|---|---|---|---|
| Product Master Plan | Owner-designated enhanced plan; header says Proposed | Owner-designated enhanced plan; header says Proposed | Retain as product authority; support plan stays separate; M1 records designation |
| Architecture / AS-IS | Rich project set; dated source commits | Rich set; known dated drift | Link and classify; never shadow |
| Existing agent guidance | Codex only | Claude only | Preserve existing owner; counterpart agent creates missing side |
| Record taxonomy/navigation | Fragmented rich records | Fragmented smaller set | Add thin support index and taxonomy around existing authorities |
| ADR register | Subsystem decision sets, no root register | None unified | Add one discoverable root support register; reference existing decisions |
| Coordination | Missing | Missing | Enable dual-agent + multi-writer modules |
| Handoff | Missing | Missing | Add clone-complete repo-local contract and publisher |
| AFI/LL/GP lifecycle | Product-plan AFIs only | Product-plan AFIs only | Add support ledgers; never duplicate product issues |
| Validation aggregate | pytest/CPI/ruff plus focused CI | layered unittest/optional/CI | Compose natively; common result vocabulary only |
| Hosted governance | Rich workflows/templates; one branch mismatch | CI core/optional/lockfile | Integrate; hosted mutation needs separate approval |
| Documentation freshness | Existing ledger | U7 proposed, no index | Preserve FIN ledger; coordinate Loto support docs with U7 |
| Release policy | Planned, package 2.1.0, no tags | Not configured, package 0.1.0, no tags | Record truthfully; do not create releases during transfer |
| Index module | Justified by 1,052 tracked files and vendor/generated exclusions | Optional at 131 tracked files | Recommend enabled for FIN, deferred for Loto |
| Skills module | No proven support workflow needing a repo skill | Same | Disabled initially; global handoff skill remains optional |
| Formal state machine | No need demonstrated | No need demonstrated | Disabled; use lightweight gates/status only |

## Collision register

| ID | Target | Collision | Risk | Recommended M1 disposition |
|---|---|---|---|---|
| FIN-C01 | FIN | Enhanced product plan is owner-designated but labeled Proposed | Ambiguous plan authority | Accept owner designation; do not edit product plan in support work |
| FIN-C02 | FIN | `AGENTS.md` says populated `pyproject.toml` is empty | Incorrect agent setup guidance | Authorize Codex correction during T4 |
| FIN-C03 | FIN | Follow-up CI push branch is `master`, repository branch is `main` | Gate may not run on direct main pushes | Separately authorize correction or explicitly defer |
| FIN-C04 | FIN | Governance doc recommends `git reset --hard` for intentional discard | User work/history loss | Replace with approval-gated, evidence-first recovery guidance |
| FIN-C05 | FIN | Multiple subsystem decision sets but no root register | Competing/hidden decision authority | Root register references existing sets without renumbering |
| LOTO-C01 | Loto | Enhanced product plan owner-designated but labeled Proposed | Ambiguous plan authority | Accept designation; no support-side product-plan edit |
| LOTO-C02 | Loto | Claude guidance contradicts packaging and omits webapp layer | Incorrect agent commands | Claude-owned U0/T4 correction |
| LOTO-C03 | Loto | Architecture packaging statement is internally stale | Misleading onboarding | U0/U7 correction; support index labels current status |
| LOTO-C04 | Loto | Progress 21/21 applies to prior TDD plan, not enhanced plan | False completion inference | Keep distinct plan/status scopes |
| LOTO-C05 | Loto | Tracked operational `DATA.csv` vs support indexing/records | Data leakage or accidental policy change | Exclude from support corpora; leave Git policy to product plan |
| BOTH-C01 | Both | Hosted branch protection is unknown | False enforcement claim | Record unknown; verify before any hosted mutation |
| BOTH-C02 | Both | User-global handoff skills are machine-local | Non-clone-complete support | Repo-local schema/publisher is core; skills optional |

## Sensitivity and exclusion matrix

| Class | CC_FIN | CC_Loto | Support rule |
|---|---|---|---|
| Secrets/credentials | `.env` ignored; none identified in targeted scan | None identified in targeted scan | Never enter records, messages, handoffs, indexes, fixtures, or logs |
| Machine-private paths | FIN worker/model/debug/database env overrides | DYNAMIX data/output/cache overrides | Record variable names and policy, not private values |
| Tracked product data | Market/source CSVs, Excel workbooks, output snapshots, model fixtures | `DATA.csv`, golden fixture JSON | Cite path/SHA/checksum only; exclude from support doc indexes |
| Generated/runtime data | `out/`, graphs, debug, temp, caches | `Output/`, plots, model cache | Exclude and never treat as committed evidence unless product contract promotes it |
| Vendor/external assets | Large vendor trees and archive tarballs | External DynaMix placeholder/cache | Exclude from support indexes; retain product provenance |
| Agent-owned infrastructure | Future `.agents/`, AGENTS, CX | Future `.claude/`, CLAUDE, CC plus counterparts | Each owner edits its side; shared validators inspect by contract |

## Scale assumptions

| Dimension | CC_FIN | CC_Loto | Design consequence |
|---|---|---|---|
| Repository size | 1,052 tracked files; 229 Python; significant vendor/data corpus | 131 tracked files; 108 Python | FIN index profile valuable; Loto starts without mandatory index service |
| Writers | Human owner + Codex + Claude | Same | Claims/board enabled; separate ownership required |
| Concurrency | Low, but two agents can overlap | Low | Non-overlapping claims; FIN/Loto publication sequential |
| Support record volume | Moderate/high because multiple subsystems and CI | Low/moderate | Same semantics, different retention/index needs |
| Runtime impact target | Support checks should add seconds, not rerun expensive forecasting | Support checks should add seconds, not run model/backtest/optimizer flows | Fast support validators separated from native full product checks |
| Retention | Git history; immutable decisions/messages/handoffs | Same | Archive resolved coordination; never delete evidence silently |
| Growth horizon | Product roadmap and many subsystem docs | Enhanced U0–U19 roadmap | Evolutionary modules; no service/database introduced for support records |

## M1 owner decisions required

1. Accept both owner-designated enhanced product plans as product authorities despite their
   `Proposed` headers, without editing those plans in support scope.
2. Accept CC_FIN as sequential pilot and prohibit parallel target publication.
3. Enable FIN docs/code index module with strict exclusions; defer Loto index module initially.
4. Disable formal state-machine and repo-local skills modules initially in both targets.
5. Classify FIN datasets and Loto `DATA.csv` as controlled product data excluded from support
   records/indexes, without changing product Git tracking.
6. Authorize Codex correction of FIN-owned guidance and safe divergence-recovery wording during
   T4/T3; authorize Claude correction of Loto-owned guidance through its side.
7. Decide FIN CI branch mismatch: recommended **authorize correction** as a separately reviewed
   hosted-workflow file change during the FIN pilot.
8. Keep branch protection `unknown` until verified through an authorized GitHub surface; no hosted
   setting changes are implied.

## T1.3 acceptance

- Missing and differently implemented capabilities are distinct.
- Path, naming, ownership, Git, test, authority, data, hosted, and release collisions are explicit.
- Scale, recovery, sensitivity, and index exclusions are ready for target profiles.
- Both target baselines match planning SHAs with zero drift.
- Neither target repository was mutated.
