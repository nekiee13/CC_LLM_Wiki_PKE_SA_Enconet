# ADR-0025 — Browser harness dependency and runtime

| Field | Value |
|---|---|
| Status | Accepted |
| Date | 2026-09-03 |
| Decided by | Human (project owner) |
| Scope | EA5.1 offline browser-test dependency and runtime |
| Register | Owner response `Approved` after Codex proposed the exact dependency/runtime choice |
| Authored by | Codex (`CX_` prefix) |

## Context

EA5.1 requires a real headless browser to verify the self-contained dashboard through `file://`.
ADR-0024 deferred browser-test dependency selection and installation to an explicit Owner decision.
The project already has a dedicated Conda prefix, but no browser automation package or pinned
browser runtime was installed there.

## Decision

1. Use the Playwright Python library pinned to `playwright==1.62.0`; do not add the larger pytest
   plugin because the small project-specific harness needs only the synchronous library API.
2. Install Playwright's matching Chromium headless shell using `--only-shell chromium`. The
   installed runtime is Chromium `151.0.7922.34`, Playwright revision `1234`.
3. Store browser runtime files beneath `C:\xPY\vEnv\WikiEnconet\pw-browsers`. CI may override the
   root using `PLAYWRIGHT_BROWSERS_PATH` but must install and verify the same pinned revision.
4. Browser checks must open local HTML through `file://`, fail rather than skip when the package or
   runtime is absent or mismatched, and reject any observed HTTP(S) request.
5. A failed page check retains `screenshot.png`, `dom.html`, and `console.log`. Passing checks do
   not create failure artifacts.
6. This harness tests the offline Evidence Explorer only. It does not restore a live service or
   supersede ADR-0007.

## Consequences

- Browser/runtime installation is reproducible and isolated from the repository and global Python.
- EA2.2 can use a real browser RED test for interactive evidence controls.
- The current inert-control browser check remains a strict expected failure until EA2.2 implements
  the control.
- A Playwright or browser revision change requires a new Owner-approved ADR and synchronized pins.
