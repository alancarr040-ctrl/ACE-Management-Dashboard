# ACE Management Dashboard Documentation

This directory contains the long-form documentation for **ACE Management Dashboard (ACEMD)**.

The repository root is reserved for project identity and primary entry points. Package-specific and release-specific material belongs under `docs/` so the GitHub landing page continues to explain the project rather than one particular update.

## Documentation model

ACEMD uses four documentation layers:

| Layer | Location | Question answered |
|---|---|---|
| Project identity | Repository root | What is ACEMD, where is it going, and what has changed over time? |
| Package specification | `docs/Packages/PACKAGE_<version>.md` | What are we planning or building for this package? |
| Release record | `docs/Releases/<version>/` | What was delivered, how is it tested, and was it certified? |
| Long-lived technical documentation | Architecture, Operations, Development, Services, and other topic directories | How does the system work and how is it maintained? |

## Required repository-root documents

```text
README.md       Project overview and entry point
ROADMAP.md      Development direction
CHANGELOG.md    Cumulative release history
VERSION         Current repository version
LICENSE         License terms
```

A release-package README, package contents list, test instructions, or deployment note must not replace the root `README.md`.

## Package specifications

Each planned or active package should have one canonical specification:

```text
docs/Packages/PACKAGE_<version>.md
```

The package specification should define:

- objective and reason for the package;
- scope and exclusions;
- architecture or storage contracts;
- expected implementation areas;
- dependencies and compatibility requirements;
- acceptance criteria;
- deferred work.

Package documents describe **what is intended to be built**. They are not proof that the package was delivered or certified.

## Release records

Each delivered release should use:

```text
docs/Releases/<version>/
├── README.md
├── RELEASE_NOTES.md
├── TEST_PLAN.md
├── CERTIFICATION.md
└── KNOWN_ISSUES.md
```

Additional release-specific technical notes are allowed when useful, such as `OWNER_STORAGE.md`.

- `README.md` gives the release overview and links to its records.
- `RELEASE_NOTES.md` records what was actually delivered.
- `TEST_PLAN.md` defines repeatable verification.
- `CERTIFICATION.md` records test results and approval status.
- `KNOWN_ISSUES.md` records intentionally deferred or unresolved items.

A release may remain marked **Release Candidate** or **Certification in progress** until its certification record is complete.

## Long-lived documentation

| Directory | Purpose |
|---|---|
| `ACE/` | ACE discovery, schema, property, and read-only research material. |
| `AI/` | AI governance, engineering standards, workflow, and certified subsystem records. |
| `Architecture/` | Architecture references and engineering decision records. |
| `Automation/` | Automation and job architecture. |
| `Development/` | Git workflow, documentation standards, and contributor guidance. |
| `Metrics/` | Metrics architecture and collector documentation. |
| `Notifications/` | Notification architecture and behavior. |
| `Operations/` | Docker, backups, database, network, recovery, and server operations. |
| `Packages/` | Package specifications. |
| `Releases/` | Delivered release records. |
| `References/` | External or imported reference indexes. |
| `Server/` | ACE server administration references. |
| `Vision/` | Product vision and project identity. |

Older documents outside the current convention are retained as historical records unless a dedicated migration package explicitly normalizes them.

## In-application browser

The dashboard exposes approved documentation through the read-only `/docs/` route. This browser is for viewing repository documentation and does not permit editing or arbitrary filesystem access.
