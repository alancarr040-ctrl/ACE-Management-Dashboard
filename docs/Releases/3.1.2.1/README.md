# Release 3.1.2.1 — Research Lab Persistence Correction

**Status:** Release Candidate — certification in progress

This corrective release establishes production-safe persistent Research Lab storage and the deployment ownership, backup, and documentation behavior required to support it long term.

## Release records

- [`RELEASE_NOTES.md`](RELEASE_NOTES.md) — delivered behavior and scope.
- [`TEST_PLAN.md`](TEST_PLAN.md) — repeatable certification sequence.
- [`CERTIFICATION.md`](CERTIFICATION.md) — executed test results and release status.
- [`KNOWN_ISSUES.md`](KNOWN_ISSUES.md) — deferred and compatibility items.
- [`OWNER_STORAGE.md`](OWNER_STORAGE.md) — deployment identity and persistent-storage procedure.
- [`../../Packages/PACKAGE_3.1.2.1.md`](../../Packages/PACKAGE_3.1.2.1.md) — original package objective and acceptance criteria.

## Deployment

```bash
cd /opt/acserver
sudo bash ./scripts/prepare-dashboard-owner.sh /opt/acserver
docker compose up -d --build --force-recreate ace-dashboard
```

The explicit `bash` invocation is intentional because Windows extraction and FTP/SCP upload workflows may strip Unix executable permissions.

After deployment, the release documentation is available through the read-only browser at:

```text
http://SERVER:8080/docs/Releases/3.1.2.1/
```

## Scope boundary

Automation and Notifications continue using their legacy writable state beneath `backups/runtime/` in this release. Their migration into the canonical `data/` root is deferred to a future storage-registry package.
