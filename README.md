# ACE Management Dashboard 3.1.2.1 Release Candidate

This changed-files package finalizes **Phase 3.1.2.1 – Research Lab Persistence Correction**. Apply every file at its matching path beneath the ACE deployment root, normally `/opt/acserver`.

## Finalized behavior

- ACEMD runs as the numeric owner of the deployment directory.
- Docker socket group access is detected from `/var/run/docker.sock`.
- `ACEMD_UID`, `ACEMD_GID`, and `ACEMD_DOCKER_GID` are maintained automatically in `.env`.
- `/opt/acserver/data/` is the permanent ACEMD persistent-storage root.
- `/opt/acserver/backups/runtime/` remains a managed legacy writable-state path for Automation and Notifications.
- The entire persistent data root is mounted at `/app/data`.
- Research Lab evidence remains at `/app/data/research_lab` and has no container-local fallback.
- Runtime backups fail for missing required deployment content but only warn for missing optional documentation.
- `/docs/` provides a read-only browser for approved documentation file types.

## Deployment

```bash
cd /opt/acserver
unzip ACEMD-3.1.2.1-Release-Candidate.zip
./scripts/prepare-dashboard-owner.sh /opt/acserver
docker compose up -d --build --force-recreate ace-dashboard
```

The preparation script is safe to rerun. It detects ownership, updates only the three non-secret ACEMD identity values in `.env`, creates the complete persistent data tree, repairs both writable host trees, preserves `.env` ownership, and validates the resulting Compose configuration. It automatically requests `sudo` when inherited root-owned files require repair.

## Permanent data layout

```text
/opt/acserver/data/
├── research_lab/
│   └── snapshots/
├── registry/
├── knowledge/
├── screenshots/
├── imports/
├── exports/
├── cache/
└── logs/
```

Future persistent subsystems must use this root rather than container-local storage.

## Test documentation

After deployment, open:

```text
http://SERVER:8080/docs/Releases/3.1.2.1/TEST_PLAN.md
```

The complete deployment and ownership procedure is in `docs/Releases/3.1.2.1/OWNER_STORAGE.md`.

## Release-candidate scope

This package does not migrate Automation or Notifications. Their existing writable state beneath `backups/runtime/` is retained for compatibility and is now prepared automatically. A future storage-registry phase should migrate those subsystems beneath the canonical `data/` root.
