# Workspace & Navigation Framework

ACEMD 2.9.1 reorganizes the application around permanent platform workspaces instead of continuing to add one top-level tab per feature.

## Top-Level Workspaces

- Dashboard: daily operator summary.
- Operations: modules that perform controlled changes.
- Monitoring: modules that observe state and history.
- Administration: Phase 3 ACE administration modules.
- Tools: diagnostics, maintenance, import/export, API, and developer utilities.
- About: project identity and release information.

## Navigation Rule

Top-level navigation represents permanent platform workspaces, not individual features.

New modules must be assigned to the workspace that owns their responsibility. If a module does not fit any workspace, the workspace model should be reviewed before another top-level tab is added.
