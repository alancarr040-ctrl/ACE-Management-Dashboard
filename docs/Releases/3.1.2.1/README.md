# Release 3.1.2.1 — Research Lab Persistence Correction

This release finalizes the corrective persistence package for long-term Research Lab use.

Documents:

- `RELEASE_NOTES.md` — finalized behavior and scope;
- `OWNER_STORAGE.md` — deployment identity and permanent storage procedure;
- `TEST_PLAN.md` — certification test sequence.

Deployment sequence:

```bash
cd /opt/acserver
./scripts/prepare-dashboard-owner.sh /opt/acserver
docker compose up -d --build --force-recreate ace-dashboard
```

After deployment, these documents are available through the read-only browser at `/docs/Releases/3.1.2.1/`.

The release candidate additionally repairs the legacy writable runtime-state tree used by Automation and Notifications and validates that `.env` remains owned by the deployment account.
