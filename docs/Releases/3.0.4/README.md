# ACE Management Dashboard 3.0.4

Phase 3.0.4 establishes the ACE Property Dictionary as shared read-only knowledge infrastructure beneath the existing Knowledge Base.

Apply this changed-files package at matching paths beneath the ACE deployment root, normally `/opt/acserver`, then rebuild the dashboard container.

```bash
cd /opt/acserver
unzip -o ACE-Management-Dashboard-3.0.4-Git.zip
./scripts/prepare-dashboard-owner.sh /opt/acserver
docker compose up -d --build --force-recreate ace-dashboard
```

The release installs the version-controlled dictionary in both locations required by the project:

- `dashboard/data/property_dictionary.json` — source/build asset
- `data/property_dictionary.json` — runtime copy mounted at `/app/data/property_dictionary.json`

After deployment:

- Open **Administration → Knowledge** and confirm the existing Knowledge Base remains available.
- Select **Open Property Dictionary**.
- Confirm 899 entries, 576 confirmed entries, 323 research entries, and eight property groups.
- Search for `198` or `ALLEGIANCE_SWEAR_TIMESTAMP_INT`.
- Open a character detail page and inspect translated property labels.

This release is display-only and performs no ACE database writes.
