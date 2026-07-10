# Deployment Ownership and Persistent Storage

ACE Management Dashboard uses the account that owns the ACE deployment directory as its runtime identity. The container does not run as root and does not depend on hard-coded host IDs.

## Automated preparation

Run from the deployment host:

```bash
cd /opt/acserver
./scripts/prepare-dashboard-owner.sh /opt/acserver
```

The script obtains the deployment identity with:

```bash
stat -c '%u:%g' /opt/acserver
stat -c '%g' /var/run/docker.sock
```

The script automatically requests `sudo` when necessary, while still deriving the runtime identity from `/opt/acserver`. It then creates or updates only these entries in `.env`:

```text
ACEMD_UID=<deployment-directory owner UID>
ACEMD_GID=<deployment-directory owner GID>
ACEMD_DOCKER_GID=<Docker socket GID>
```

Existing secrets and unrelated environment values are preserved. Duplicate ACEMD identity entries are reduced to one current value.

## Validation and failure behavior

The script is idempotent and safe to rerun. It:

1. verifies the project root and Docker socket;
2. validates detected IDs as numeric values;
3. creates the permanent data layout and legacy runtime-state directory;
4. preserves existing Research Lab, Automation, and Notifications state;
5. repairs owner/group and modes beneath both writable host trees;
6. restores `.env` ownership to the deployment identity after atomic updates;
7. confirms Research Lab and legacy runtime paths are writable as the deployment account;
8. runs `docker compose config` when Docker Compose is available;
9. fails if either writable tree retains foreign ownership.

When inherited root-owned data exists, the script re-executes itself through `sudo`. Running the normal command is sufficient:

```bash
/opt/acserver/scripts/prepare-dashboard-owner.sh /opt/acserver
```

The detected runtime UID and GID still come from `/opt/acserver`; privilege elevation never causes the dashboard to run as root.

## Compose runtime identity

The dashboard service uses values populated in `.env`:

```yaml
user: "${ACEMD_UID}:${ACEMD_GID}"
group_add:
  - "${ACEMD_DOCKER_GID}"
```

There are no default numeric fallbacks. Missing preparation values cause Compose validation to fail rather than silently selecting the wrong host identity.

## Permanent storage standard

All generated, durable ACEMD content belongs under:

```text
/opt/acserver/data/
```

Reserved subsystem paths are:

```text
research_lab/
registry/
knowledge/
screenshots/
imports/
exports/
cache/
logs/
```

The complete host directory is mounted read-write into the dashboard at `/app/data`. Research Lab uses `/app/data/research_lab`, supplied through the required `ACEMD_RESEARCH_ROOT` setting.

Application source, documentation, and ACE configuration remain mounted separately and are not writable storage substitutes.

## Current writable host trees

```text
/opt/acserver/data/
/opt/acserver/backups/runtime/
```

`data/` is the canonical permanent storage root. `backups/runtime/` is temporarily retained because the existing Automation and Notifications implementations store writable JSON state there. This release candidate manages that path but does not migrate those subsystems.

Nothing beneath either writable tree should remain owned by root after preparation.
