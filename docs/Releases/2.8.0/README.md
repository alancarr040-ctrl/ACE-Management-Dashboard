# ACE Management Dashboard 2.8.0 Test Package

## Package

**2.8.0 - Metrics & Resource Monitoring**

## Purpose

Adds the ACEMD Metrics Service, Metrics dashboard page, metrics API endpoint, resource threshold checks, and a metrics automation job.

## Test Checklist

- Confirm the dashboard starts after rebuild.
- Open `/metrics` and verify the Metrics tab renders.
- Open `/api/metrics` and verify JSON is returned.
- Confirm CPU, memory, disk, container, database, and ACEMD metrics appear.
- Confirm the page auto-refreshes without errors.
- Open Automation and verify the **Metrics Snapshot** job is registered.
- Run Metrics Snapshot manually and verify an automation event is recorded.
- Confirm existing Health, Events, Automation, Management, Docker, Backups, and Logs pages still render.

## Deployment

```bash
docker compose up -d --build ace-dashboard
```
