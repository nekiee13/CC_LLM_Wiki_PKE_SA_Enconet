# Offline browser testing

EA5.1 uses the Owner-approved contract in `schemas/browser_harness.yml`: Playwright 1.62.0 and its
matching Chromium headless shell (revision 1234, Chromium 151.0.7922.34). Tests open the generated
dashboard directly through `file://`; no HTTP server is involved.

## Install or repair the pinned runtime

From `Enconet` in PowerShell:

```powershell
$env:PLAYWRIGHT_BROWSERS_PATH='C:\xPY\vEnv\WikiEnconet\pw-browsers'
& 'C:\xPY\vEnv\WikiEnconet\python.exe' -m pip install -r sieving\requirements.txt
& 'C:\xPY\vEnv\WikiEnconet\python.exe' -m playwright install --only-shell chromium
```

## Local and CI command

Set `PLAYWRIGHT_BROWSERS_PATH` to the controlled runtime directory on the executing machine. Then
run the same preflight and browser command locally or in CI:

```powershell
$env:PLAYWRIGHT_BROWSERS_PATH='C:\xPY\vEnv\WikiEnconet\pw-browsers'
& 'C:\xPY\vEnv\WikiEnconet\python.exe' scripts\browser_harness.py preflight
& 'C:\xPY\vEnv\WikiEnconet\python.exe' scripts\browser_harness.py check `
  outputs\candidates\evidence_access\RUN-20260728-01\enconet_appendix_b_dashboard.html `
  --artifacts outputs\candidates\evidence_access\RUN-20260728-01\browser-test-artifacts
```

Both commands return non-zero with an actionable message when the library, runtime, local HTML,
offline contract, or page assertion fails. A failed page check retains `screenshot.png`,
`dom.html`, and `console.log` in the specified artifact directory. Passing checks do not create
that directory. Add `--require-interactive` for the EA2.2 control contract; it intentionally fails
against the current EA2.1 candidate because evidence references are still inert text.
