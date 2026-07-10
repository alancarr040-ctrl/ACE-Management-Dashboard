# Release Documentation

This directory is the permanent delivery and certification history for ACE Management Dashboard.

## Standard release directory

New releases should use:

```text
<version>/
├── README.md
├── RELEASE_NOTES.md
├── TEST_PLAN.md
├── CERTIFICATION.md
└── KNOWN_ISSUES.md
```

Additional release-specific notes may be included when needed.

## Document responsibilities

| Document | Purpose |
|---|---|
| `README.md` | Release overview, status, and navigation. |
| `RELEASE_NOTES.md` | What was actually delivered. |
| `TEST_PLAN.md` | Repeatable validation and regression checks. |
| `CERTIFICATION.md` | Executed results, environment, date, and approval status. |
| `KNOWN_ISSUES.md` | Deferred, compatible legacy behavior, and unresolved limitations. |

The repository root `CHANGELOG.md` remains the cumulative human-facing history. Package intent is documented separately under `docs/Packages/`.

Historical release directories may not contain every modern standard file. They remain valid historical records and should not be rewritten without a dedicated documentation migration package.
