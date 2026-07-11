# Changelog

## 3.0.4 — ACE Property Dictionary Foundation

- Added a separate searchable Property Dictionary while preserving the existing Knowledge Base.
- Imported 899 community property definitions with confirmed/research provenance.
- Added shared property lookup and character-detail annotation.
- Installed the generated dictionary in the persistent runtime data path used by Docker.
- Added configurable runtime path resolution and visible load-error diagnostics.
- Finalized release metadata and deployment documentation.

## 3.1.2.1 — Research Lab Persistence Correction

- Moved Research Lab evidence to persistent host-mounted storage.
- Added mandatory storage configuration and writability validation.
- Added atomic JSON writes and visible Evidence Storage status.
- Added Research Lab evidence to runtime infrastructure backups.
- Added backup preflight validation for required runtime paths.
- Made documentation and non-runtime project files optional backup content.
- Added exact included/missing path reporting to backup manifests.
- Added a read-only `/docs/` route for project documentation.

- Runs the dashboard as the configured deployment-owner UID/GID instead of root.
- Adds Docker socket supplemental-group configuration.
- Adds owner-safe persistent-data initialization helper.
- Preserves an existing Research Lab marker instead of rewriting it at startup.
- Expands runtime backup coverage to the complete persistent `data/` tree.

## 3.1.2.1 Finalization

- automated deployment UID, GID, and Docker socket GID detection;
- removed hard-coded Compose identity fallbacks;
- formalized `/opt/acserver/data/` as ACEMD's permanent storage root;
- added reserved persistent subsystem directories;
- mounted the complete persistent data root at `/app/data`;
- made owner preparation idempotent with permission and Compose validation;
- aligned runtime backup required and optional path policy;
- recorded included and skipped optional files in backup manifests;
- hardened the read-only documentation browser against traversal and unsafe filenames;
- expanded deployment and certification documentation.

## 3.1.2.1 Documentation Cleanup

- restored the repository root `README.md` as the public project overview;
- formalized package specifications under `docs/Packages/`;
- formalized release records under `docs/Releases/<version>/`;
- added 3.1.2.1 certification and known-issues records;
- moved release-package details out of the repository root;
- documented Windows extraction and FTP/SCP executable-permission behavior;
- expanded `.gitignore` coverage for deployment secrets and generated runtime evidence.

## 3.1.2.1 Release Candidate

- automatically elevates owner preparation when inherited root-owned files require repair;
- repairs and validates ownership for both `/opt/acserver/data` and `/opt/acserver/backups/runtime`;
- preserves `/opt/acserver/backups/runtime` as a compatibility location for current Automation and Notifications state;
- restores `.env` ownership to the detected deployment UID:GID after atomic updates;
- validates writable paths using the deployment identity rather than root;
- adds regression checks for Dashboard, Operations, Management, Docker, Automation, and Notifications;
- confirms the release package contains no source `Test/` content.
