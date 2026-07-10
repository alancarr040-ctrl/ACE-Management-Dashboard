# ACE Management Dashboard 2.5.0 - Operational Health Dashboard

This package is built directly against the accepted 2.4.1b Operations Safety Hotfix baseline.

## Purpose

Phase 2.5.0 adds a compact, read-only Health workspace for daily operational visibility. It does not add new destructive controls or restart/rebuild workflows.

## Included Changes

- Adds `/health` navigation tab.
- Adds `/api/health` JSON endpoint.
- Adds `HealthService` aggregation layer.
- Adds compact overall health summary, service rows, disk/backup/wrapper checks, and recent management failure summary.
- Adds defensive health checks so individual subsystem failures render as warnings or critical rows instead of causing a page error.
- Updates dashboard metadata and release documentation.

## Deployment

Extract the package over the current ACE Management Dashboard repository or deployment tree, then rebuild the dashboard container if required:

```bash
docker compose up -d --build ace-dashboard
```

## Testing Checklist

1. Confirm the Dashboard, Docker, Backups, Logs, Management, Health, and About tabs load.
2. Open `/health` and verify the page renders without a 500 error.
3. Open `/api/health` and verify JSON is returned.
4. Confirm Health reports ace-dashboard, ace-server, and ace-db.
5. Confirm the page auto-refreshes after roughly 30 seconds.
6. Confirm Management page actions still behave as in 2.4.1b.

## Safety Notes

The Health page is read-only. Restart, rebuild, backup creation, and other state-changing actions remain on existing guarded workflows.
