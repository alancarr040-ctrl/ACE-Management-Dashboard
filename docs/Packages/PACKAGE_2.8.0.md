# Package 2.8.0 - Metrics & Resource Monitoring

## Objective

Add compact ACEMD metrics views that help operators understand why services may be slow, unhealthy, or under load.

## Planned Scope

- System CPU summary.
- System memory summary.
- Disk usage and disk I/O summary where available.
- Container resource usage for dashboard, ACE server, and database containers.
- Metrics API endpoint.
- Compact Health-page metrics summary or link-out.
- Event publication when resource thresholds are crossed.

## Constraints

- Avoid graph-heavy UI bloat in the initial release.
- Prefer compact summary cards and drill-down details.
- Keep Health read-only.
- Do not add alert delivery channels in this phase; notifications are reserved for 2.9.0.

## Documentation Requirements

- Update `ROADMAP.md`.
- Update `docs/AI/AI_ROADMAP.md`.
- Add metrics architecture documentation.
- Add release notes and package README.
