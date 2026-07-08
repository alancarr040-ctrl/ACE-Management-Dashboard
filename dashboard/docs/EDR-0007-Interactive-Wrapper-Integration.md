# EDR-0007 - Interactive Wrapper Integration

## Status
Accepted

## Context
Phase 2.3 introduced `manage.sh` as the canonical command-line wrapper for ACE stack administration. The dashboard displayed wrapper commands as documentation only. Phase 2.4 begins integrating the wrapper into the dashboard so common operational tasks can be run from the ACE Management Utility page.

## Decision
The dashboard will invoke the wrapper only through a dedicated management service layer. Browser requests may select from whitelisted action identifiers, but may not submit arbitrary shell commands or command arguments.

The service layer executes `manage.sh` using `subprocess.run()` with `shell=False`, a fixed working directory, captured output, and a timeout. Interactive shell actions are intentionally excluded from the dashboard action catalog and remain SSH/manual-only.

## Consequences
- The management page becomes an operational interface instead of a read-only command reference.
- Wrapper integration remains centralized in `dashboard/services/management_service.py`.
- Future Docker, backup, server, and database pages should call the management service rather than embedding one-off Docker Compose commands.
- Changes and restarts are guarded by confirmation prompts and support dry-run when the wrapper supports it.
- Recent dashboard-managed wrapper actions are recorded in `backups/runtime/management-audit.jsonl`.

## Safety Rules
- No arbitrary command text from the browser.
- No shell execution.
- No interactive shell actions from the dashboard.
- Change-oriented actions require confirmation.
- Wrapper execution has a timeout.
- Command output is captured and displayed to the operator.
