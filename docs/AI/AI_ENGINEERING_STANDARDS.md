# ACEMD Engineering Standards

## Terminology standard

The product shall be referred to as **ACE Management Dashboard** in user-facing documentation.

The approved short name is **ACEMD**.

The term **ACE** refers exclusively to the underlying ACE emulator/server project and must not be used interchangeably with ACE Management Dashboard.

## UI standards

- Grow functionality before growing the UI.
- Add new cards/pages only when they represent distinct operational domains.
- Keep the primary operational dashboard compact enough to summarize state in one screen whenever practical.
- Prefer drill-down pages for detail.
- Health pages are read-only; corrective actions belong in Management or guided operations workflows.

## Operations standards

- Operational actions should flow through `manage.sh` or a certified ACEMD service layer.
- Do not accept arbitrary shell commands from the UI.
- Use whitelists for management actions.
- Preserve dry-run support where practical.
- Disruptive operations that restart or rebuild the dashboard should require special handling or remain SSH/manual until task-runner support exists.

## Event standards

- Subsystems should publish operationally meaningful events through a shared event service.
- Health transitions, management command results, future automation jobs, backup results, and alert decisions should be event-capable.

## Documentation standards

- `README.md` explains the project entry point.
- `VISION.md` defines product identity and philosophy.
- `ROADMAP.md` is the public GitHub roadmap.
- `CHANGELOG.md` summarizes certified releases.
- `docs/AI/AI_ROADMAP.md` provides governance roadmap detail.
- Future package work must update documentation when architecture, roadmap, naming, or workflow expectations change.

## Git and certification standards

- Build from the current accepted baseline.
- Test locally before accepting.
- Review changes in GitHub Desktop or git diff before commit.
- Commit only accepted packages to the main branch.
- Preserve package ZIPs as recovery points.
