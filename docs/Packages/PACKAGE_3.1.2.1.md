# Package 3.1.2.1 — Research Lab Persistence Correction

## Objective

Finalize Research Lab persistence so observations, snapshots, and evidence survive dashboard restart, container recreation, rebuild, and image replacement without depending on container-local storage.

This package also hardens the deployment identity, writable-path preparation, runtime backup policy, and documentation access required to support that persistence safely.

## Scope

- Detect the deployment UID and GID from the owner of the deployment root.
- Detect the Docker socket GID from `/var/run/docker.sock`.
- Maintain `ACEMD_UID`, `ACEMD_GID`, and `ACEMD_DOCKER_GID` in `.env`.
- Run the dashboard under the detected deployment identity with the Docker socket group added.
- Formalize `/opt/acserver/data` as ACEMD's permanent persistent-storage root.
- Store Research Lab evidence under `/opt/acserver/data/research_lab`.
- Prepare and validate all current writable host paths.
- Make runtime backups enforce required content while treating documentation as optional.
- Record optional backup inclusions and omissions in the manifest.
- Provide a read-only documentation browser.
- Complete only minor Research Lab polish required for production persistence.

## Storage contract

| Purpose | Host path | Container path |
|---|---|---|
| ACEMD permanent data root | `/opt/acserver/data` | `/app/data` |
| Research Lab | `/opt/acserver/data/research_lab` | `/app/data/research_lab` |
| Research Lab configuration | `ACEMD_RESEARCH_ROOT=/app/data/research_lab` | Required |
| Legacy Automation and Notifications state | `/opt/acserver/backups/runtime` | Compatibility path for this release |

Research Lab must not fall back to container-local storage.

## Reserved persistent directories

```text
data/
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

Future durable subsystems should use the canonical data root rather than introduce new container-local stores.

## Backup policy

Required content:

```text
docker-compose.yml
.env
ace/Config/
data/
scripts/
```

Optional content:

```text
README.md
CHANGELOG.md
ROADMAP.md
VERSION
LICENSE
docs/
```

Missing required content must fail before backup creation. Missing optional content must warn and be recorded as skipped.

## Compatibility and exclusions

- Automation and Notifications are not migrated into `data/` in this package.
- Their existing state under `backups/runtime/` remains supported and ownership-managed.
- No new Research Lab feature phase is introduced.
- No unrelated ACE, database, or management subsystem refactoring is included.
- A future storage-registry package should centralize writable-path declarations and migrate remaining legacy state.

## Acceptance criteria

- Owner preparation is safe and idempotent.
- No manual `.env`, Compose, ownership, or Docker-group editing is required.
- Dashboard runtime identity matches the deployment owner and includes the Docker socket group.
- All current writable host paths are accessible by the dashboard identity.
- Research Lab evidence survives restart, recreation, rebuild, and image removal.
- Automation and Notifications load after ownership preparation.
- Runtime backup succeeds with missing optional documentation and fails with missing required content.
- Backup manifests identify included and skipped optional paths.
- The documentation browser is read-only and prevents traversal.
- The executed test record is captured in the release certification document.
