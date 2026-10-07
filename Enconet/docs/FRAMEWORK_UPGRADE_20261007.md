# Enconet framework upgrade — 7 October 2026

The owner requested the portable Ekonerg improvements in Enconet. Fourteen
files were added from the versioned v2 upgrade. Existing closed-audit files,
database, raw sources, source editions, approvals, ratings and active prompt
were preserved. No audit was reset or re-sieved.

Added tools: full keyword sweep and concept cards; v3 DOCUMENT prompt candidate;
optional context contract; reset v2; neutral light-dashboard renderer; and
separate dark overlay with the accepted lighting, grid and cursor effects.

The new light and dark presentation candidates use Enconet's own recorded run:
87.5%, 234 active vendor crumbs, and 18 criteria. They have criterion summaries,
score-supporting crumbs, exact quotes, and clickable source chapters.

- [Light candidate](../out/2026-10-07/framework-v2/ENCONET_DASHBOARD_LIGHT.html)
- [Dark candidate](../out/2026-10-07/framework-v2/ENCONET_DASHBOARD_DARK.html)
- [Method](FRAMEWORK_METHOD_V2.md)
- [Detailed rollout and checks](../../doc/framework-reuse/ROLLOUT_20261007.md)
- [Ekonerg work summary](../../Ekonerg/docs/EKONERG_IMPROVEMENTS_SUMMARY_20261007.md)

The current approved dashboard remains in `outputs/`. These candidates do not
change it, change the Croatian report, or create a new issued audit.

The v3 prompt is available but not active in Enconet. For a future audit, check
its schema/runtime compatibility and calibrate it on Enconet evidence before
activation. Ekonerg's golden approvals and regulatory decisions were not copied.

Reset defaults to preview; applying it is destructive. Do not run reset to
finish this upgrade. Its v2 plan includes `out/`, raw-source registry entries
and old candidates, while preserving incoming, code, docs and history.

Claude review and any Claude-owned guidance update remain pending.
