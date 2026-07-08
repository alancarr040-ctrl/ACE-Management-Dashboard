# Release Notes - ACE Management Dashboard 2.4.0

Phase 2.4.0 integrates the ACE Management Utility wrapper into the dashboard.

## Included
- Dashboard-managed wrapper actions on the Management page.
- Safe action whitelist.
- Direct wrapper execution with `shell=False`.
- Captured stdout/stderr display.
- Dry-run support for supported change actions.
- Confirmation prompts for change actions.
- Recent activity/audit display.
- EDR-0007 documentation.

## Deployment
Copy the package contents over the existing project and rebuild the dashboard container:

```bash
docker compose up -d --build ace-dashboard
```
