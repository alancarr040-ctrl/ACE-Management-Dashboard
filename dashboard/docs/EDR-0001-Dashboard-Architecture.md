# EDR-0001 - ACE Management Dashboard Architecture

## Decision

The ACE Management Dashboard uses a manager/service-oriented architecture.

Routes remain thin. Business logic belongs in services. Templates render normalized dictionaries and should not contain business logic.

## Principles

- Dashboard tab is a summary.
- Tabs are management workspaces.
- Scripts remain reusable outside the dashboard.
- Existing administrative scripts may be invoked from services when appropriate.
- Management operations must provide clear success/failure feedback.
- Dangerous operations require guarded workflows before enablement.

## Status

Accepted.
