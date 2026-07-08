# README - Package 2.6.1 Roadmap & Vision

## Overview

Package 2.6.1 is a documentation and governance package for **ACE Management Dashboard** (**ACEMD**).

This package does not change runtime behavior. It defines the public roadmap, product identity, naming rules, and project vision before development moves into Scheduler & Automation.

## Included changes

- Added `ROADMAP.md`.
- Added `VISION.md`.
- Added root `CHANGELOG.md`.
- Updated `README.md`.
- Updated `PROJECT.md` with ACEMD identity language.
- Added/updated AI governance roadmap and engineering standards.
- Added `docs/Packages/PACKAGE_2.7.0.md`.
- Updated version metadata to 2.6.1-dev.

## Testing

This is a documentation-only package. Runtime testing should confirm that existing dashboard behavior from 2.6.0 remains unchanged after deployment.

Recommended checks:

```bash
docker compose up -d --build ace-dashboard
```

Then verify:

- Dashboard loads.
- Health page loads.
- Events page loads.
- Management page loads.
- `ROADMAP.md`, `VISION.md`, and `CHANGELOG.md` are present in Git review.

## Certification note

After review, this package may be certified as the project identity and roadmap baseline for future ACEMD development.
