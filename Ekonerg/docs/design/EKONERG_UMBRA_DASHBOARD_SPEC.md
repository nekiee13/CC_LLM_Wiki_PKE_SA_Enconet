# Ekonerg audit dashboard — UMBRA design specification

Status: draft design for review  
Owner: Codex  
Scope: offline Ekonerg audit dashboard  
Reference: `Ekonerg/vendor/design/Umbra-Dark_Mode_Design_Sys`

## What this screen is for

The dashboard is a quick map of audit work. It helps a reviewer answer four simple
questions:

1. What material has been read?
2. Which Appendix B criteria have usable evidence?
3. What is still blocked or needs a decision?
4. Can anyone see where each number came from?

This is an evidence-work screen, not a score calculator. The current Ekonerg snapshot
is an owner-approved draft with Claude review pending. The screen must therefore show
`Score withheld` and must never guess a conformity result.

## UMBRA rules used

The design follows the supplied UMBRA examples and guides:

- dark, navy-tinted surfaces; no pure black or pure grey;
- one teal accent for the main action, selection, focus, and one key figure;
- thin borders and clear panel steps instead of heavy shadows;
- Space Grotesk for headings, IBM Plex Sans for reading text, and JetBrains Mono for
  IDs and numbers when the fonts are packaged locally;
- 8 px control corners, 12 px panel corners, and 4 px tag corners;
- 4 px spacing base, 16 px panel gaps, and 20–28 px main padding;
- one primary action per view; focus is a 2 px accent outline with a 2 px offset;
- status colour is a second cue, never the only cue.

The offline project contract forbids remote scripts, remote fonts, CDNs, OAuth, and
external sign-in links. The prototype uses system fallbacks so it can be opened from a
file with no network.

## Information architecture

The 1440 px reference layout is adapted to audit work:

| Region | Purpose | Ekonerg content |
| --- | --- | --- |
| Sidebar | Move between work areas | Overview, Criteria, Evidence, Sources, Gates |
| Header | Identify the snapshot and safe actions | Ekonerg / Audit overview, run ID, Export snapshot |
| KPI row | Give the four fastest answers | Files read, verified quotes, criteria with draft coverage, score state |
| Coverage panel | Show all 18 criteria without hiding gaps | 12 partial policy matches, 6 without a direct mapped quote |
| Evidence gate | Make approvals visible | Owner-approved draft; Claude review pending |
| Evidence queue | Turn gaps into next actions | implementation records, missing references/images, reviewer decision |
| Recent batches | Keep provenance close to the view | B01–B10 evidence batches and source counts |

## Token map

| Token | Value | Use |
| --- | --- | --- |
| `bg/0` | `#0B0F14` | page background |
| `surface/1` | `#111821` | panels and sidebar |
| `surface/2` | `#17202B` | nested regions and hover |
| `surface/3` | `#1E2935` | selected controls and draft tags |
| `border/subtle` | `#243140` | hairline separators |
| `border/strong` | `#33455A` | inputs and secondary buttons |
| `accent/fill` | `#3CCFB4` | primary action and selection |
| `accent/text` | `#5FDCC6` | accent text on dark surfaces |
| `text/primary` | `#E8EEF4` | headings and important values |
| `text/secondary` | `#A9B6C4` | body copy and table cells |
| `text/muted` | `#8392A3` | labels and helper text |
| `status/review` | `#E8B04B` | review pending |
| `status/blocked` | `#F07178` | missing or blocked work |
| `status/approved` | `#6FD39A` | approved work only |

## Data binding and safety

The source shape is `Ekonerg/schemas/dashboard_schema.yml`. The production view must
bind to the 18 `criterion_object` records and top-level run metadata; it must not copy
mock data from the UMBRA example.

Until the evidence gate is closed:

- `supplier` is the configured supplier, `Ekonerg`;
- `dash_id` and `run_id` are shown as monospace IDs from the run record;
- `classification_counts` may show draft counts with a `Draft` label;
- `weighted_score`, `applicable_count`, and any final classification are shown as
  `Withheld` when the approved evaluation is absent;
- every criterion row links to its crumb IDs (`refs`), affirmative text (`aff`),
  contrary text (`con`), ruling (`judge`), and verification actions (`verify`);
- a missing quote is displayed as `No direct mapped quote`, not as `Fail`;
- a pending review is displayed as `Review pending`, not as `Approved`.

## Responsive behaviour

- At 1200 px and above, use the 232 px sidebar and a two-column content grid.
- From 760–1199 px, keep the sidebar compact and stack the coverage and gate panels.
- Below 760 px, turn the sidebar into a top bar, make KPI cards one column, and let
  tables scroll horizontally. Never remove the criterion ID or evidence status.
- Keep text at least 15 px for body copy and make controls at least 36 px high.

## TDD acceptance criteria

The implementation is ready only when these checks pass:

1. A failing token test proves that every UMBRA colour used by the view is declared in
   one token block; the green test then proves no one-off colour replaces it.
2. A component test renders all four KPI cards, all 18 criteria, the gate state, and
   the B01–B10 evidence batches from fixture data.
3. A safety test proves that no score or final classification appears when approval is
   pending, and that no `Fail` label is produced from a missing quote alone.
4. An offline test finds no remote script, remote stylesheet, CDN, OAuth, or sign-in
   URL in the built artifact.
5. An accessibility test checks landmarks, heading order, keyboard focus, visible
   status text, table headers, and a 44 px pointer target for primary actions.
6. A responsive test checks the 760 px and 1200 px layouts without horizontal page
   overflow; only data tables may scroll.
7. A visual test checks the UMBRA surface ladder, teal accent use, panel radii, and
   focus ring against the reference tokens.
8. A provenance test confirms every displayed evidence count has a source run ID and
   generated date.

## Prototype

`EKONERG_UMBRA_DASHBOARD.html` is a static, offline visual prototype. It is intentionally
not a production score dashboard. The values are marked as a draft snapshot and are
there to validate hierarchy, states, and reading order before implementation.
