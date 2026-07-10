# ACE Management Dashboard Package 2.4.0

This package implements Phase 2.4.0 - Interactive Wrapper Integration.

## Install

1. Back up the current project directory.
2. Copy the package contents into the ACE Management Dashboard project root.
3. Rebuild the dashboard container:

```bash
docker compose up -d --build ace-dashboard
```

## First test path

Open the Management tab and run read-only actions first:

- Help
- Version
- Status
- Doctor

Then test dry-run actions before executing any change-oriented action.

## Safety

The dashboard does not accept arbitrary command text. It only runs whitelisted `manage.sh` actions. Interactive shell commands remain unavailable from the dashboard.
