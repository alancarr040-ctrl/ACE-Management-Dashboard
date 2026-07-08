# ACE Management Dashboard Documentation

This directory contains the long-form documentation for **ACE Management Dashboard** (**ACEMD**).

The repository root is intentionally kept small and contains only repository identity files such as `README.md`, `ROADMAP.md`, `CHANGELOG.md`, `LICENSE`, `VERSION`, `.gitignore`, and deployment entry points.

## Documentation layout

| Directory | Purpose |
|---|---|
| `AI/` | AI governance, engineering standards, and detailed roadmap material. |
| `Architecture/` | System architecture notes and engineering decision records. |
| `Automation/` | Scheduler, automation, and job architecture documentation. |
| `Development/` | Git workflow, documentation standards, and contributor guidance. |
| `Operations/` | Runtime operations such as Docker, backups, database, network, recovery, and server notes. |
| `Packages/` | Work package definitions for upcoming or active phases. |
| `Releases/` | Per-release README and release notes. |
| `Vision/` | Product vision, project identity, and infrastructure overview. |
| `Prompts/` | Preserved development prompts or historical planning artifacts. |

## Root document policy

Only repository-level documents belong in the project root. Package-specific README files, release notes, architecture notes, engineering decisions, prompts, and operational documentation belong under `docs/`.

This keeps GitHub's landing view readable while preserving the full certified documentation baseline.
