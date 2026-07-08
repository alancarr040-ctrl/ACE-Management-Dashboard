# Release Notes - ACE Management Dashboard v2.4.0

## Milestone
2.4.0 - Interactive Wrapper Integration

## Purpose
Convert the ACE Management Utility page from a read-only wrapper command reference into a controlled dashboard interface for running approved `manage.sh` actions.

## Changes
- Added whitelisted wrapper action catalog to `ManagementService`.
- Added controlled wrapper execution using direct argv subprocess calls with `shell=False`.
- Added `/management/run` POST route for dashboard-initiated wrapper actions.
- Added command output display for stdout and stderr.
- Added confirmation prompts for change-oriented actions.
- Added dashboard dry-run buttons for supported change actions.
- Excluded interactive shell actions from the web UI.
- Added recent management activity audit log display.
- Added EDR-0007 documenting the wrapper integration decision.
- Updated project metadata for Phase 2.4.0.

## Testing Notes
After deployment, rebuild the dashboard container:

```bash
docker compose up -d --build ace-dashboard
```

Then open:

```text
http://<server-ip>:8080/management
```

Recommended first tests:

```text
Help
Version
Status
Doctor
Dry Run -> Restart Server
```

Only run start, stop, restart, rebuild, or backup create actions when you are ready for the dashboard to invoke the wrapper against the local ACE stack.
