# 3.1.2.1 Test Plan — Research Lab Persistence Correction

## Objective

Certify automated deployment ownership, all current writable host paths, permanent ACEMD storage, Research Lab rebuild survival, robust runtime backup behavior, and the read-only documentation browser.

## 1. Apply and prepare

Apply all package paths beneath `/opt/acserver`, then run:

```bash
cd /opt/acserver
sudo bash ./scripts/prepare-dashboard-owner.sh /opt/acserver
docker compose up -d --build --force-recreate ace-dashboard
```

Expected:

- preparation may request `sudo`, then reports `Validation : PASS`;
- `.env` contains one current value for each of `ACEMD_UID`, `ACEMD_GID`, and `ACEMD_DOCKER_GID`;
- `docker compose config` succeeds;
- no manual `.env` or Compose editing is required.

Run the preparation command a second time. It must succeed without changing existing evidence, changing `.env` ownership to root, or creating duplicate `.env` keys.

## 2. Runtime identity and Docker access

```bash
stat -c '%u:%g' /opt/acserver
stat -c '%g' /var/run/docker.sock
grep -E '^ACEMD_(UID|GID|DOCKER_GID)=' /opt/acserver/.env
docker inspect ace-dashboard --format '{{.Config.User}} {{json .HostConfig.GroupAdd}}'
```

Expected:

- container user equals the deployment directory owner UID:GID;
- supplemental groups contain the Docker socket GID;
- a dashboard Docker-management action succeeds.


## 3. Writable ownership regression

```bash
stat -c '%U:%G %a %n' /opt/acserver/.env
find /opt/acserver/data /opt/acserver/backups/runtime -xdev \
  \( ! -uid 1000 -o ! -gid 1000 \) -print
```

Use the detected values from `.env` rather than assuming `1000:1000` on other deployments. Expected:

- `.env` is owned by the deployment account and mode `600`;
- no path in either writable tree is owned by root or another identity;
- `data/research_lab/observations.json` is writable by the dashboard identity;
- `backups/runtime/notifications.json`, when present, is writable by the dashboard identity.

Open these pages and confirm they load without HTTP 500 errors:

- Dashboard;
- Operations;
- Management;
- Docker;
- Automation;
- Notifications.

## 4. Permanent data layout

```bash
find /opt/acserver/data -maxdepth 2 -type d -printf '%P\n' | sort
```

Confirm these paths exist:

```text
research_lab/
research_lab/snapshots/
registry/
knowledge/
screenshots/
imports/
exports/
cache/
logs/
```

In **Administration → Research Lab**, confirm Evidence Storage reports `Persistent and writable` at `/app/data/research_lab`.

## 5. Research Lab persistence

1. Create a character snapshot.
2. Create a second snapshot for the same character.
3. Create an observation comparing the two snapshots.
4. Confirm host files exist beneath `/opt/acserver/data/research_lab`.
5. Restart the application.
6. Rebuild and force-recreate `ace-dashboard`.
7. Confirm both snapshots and the observation remain visible.
8. Confirm newly written files are owned by the deployment UID:GID rather than root.

## 6. Runtime backup required paths

Required backup content is:

```text
docker-compose.yml
.env
ace/Config/
data/
scripts/
```

Create a runtime backup and confirm all required paths appear in `manifest.txt` and `ace_infrastructure.tar.gz`.

Temporarily remove or rename one required path in a controlled test. Backup preflight must fail clearly and must not leave an empty timestamped backup directory. Restore the path immediately.

## 7. Runtime backup optional paths

Optional content is:

```text
README.md
CHANGELOG.md
ROADMAP.md
VERSION
LICENSE
docs/
```

Temporarily remove or rename one optional item, create a backup, and confirm:

- the backup succeeds;
- a warning identifies the skipped item;
- `manifest.txt` records both **Optional paths included** and **Optional paths skipped**.

Inspect Research Lab evidence:

```bash
tar -tzf backups/runtime/<NEW_BACKUP>/ace_infrastructure.tar.gz \
  | grep '^data/research_lab/'
```

## 8. Documentation browser

Open:

```text
http://SERVER:8080/docs/
http://SERVER:8080/docs/Releases/3.1.2.1/TEST_PLAN.md
```

Confirm directories can be browsed and the test plan is served inline and read-only.

Confirm these controls:

- traversal such as `/docs/../.env` does not expose files;
- disallowed file types return 404;
- filenames containing HTML characters render as text, not markup;
- direct responses include no-store and content-type protection headers.

## 9. Regression checks

Confirm:

- dashboard home and Administration pages load;
- Research Lab snapshot and observation operations still work;
- application startup fails clearly when `ACEMD_RESEARCH_ROOT` is absent or invalid;
- existing ACE services remain unaffected;
- Automation and Notifications load with their existing state after preparation;
- responsive navigation remains usable.

## Certification result

Phase 3.1.2.1 is ready for certification when all tests pass without manual ownership edits, persistent evidence survives recreation, backup behavior matches required/optional policy, and documentation remains read-only.

## 10. Package isolation

Before distribution, inspect the ZIP listing and confirm there is no `Test/` or `test/` path. The source test directory may be empty or populated; it must never be copied into this changed-files release package.
