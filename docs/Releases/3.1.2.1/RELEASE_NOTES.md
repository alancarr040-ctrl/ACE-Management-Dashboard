# ACE Management Dashboard 3.1.2.1

## Research Lab Persistence Correction — Release Candidate

This corrective package completes the production hardening required before Research Lab development continues.

### Deployment ownership

The dashboard runtime identity is now derived from the owner of `/opt/acserver`. Docker socket access uses the socket's actual host GID. `scripts/prepare-dashboard-owner.sh` writes the three required non-secret values to `.env`, repairs the permanent data tree, and validates the resulting deployment.

Compose no longer supplies hard-coded UID, GID, or Docker group fallbacks. A deployment must be prepared correctly rather than silently running under an incorrect host identity.

### Permanent data root

`/opt/acserver/data/` is now the permanent storage root for ACEMD-generated durable content. The complete root is mounted at `/app/data` and reserves paths for Research Lab, registry, knowledge, screenshots, imports, exports, cache, and logs.

Research Lab continues to require `ACEMD_RESEARCH_ROOT=/app/data/research_lab` and does not fall back to container-local storage.

### Runtime backup

Backup preflight now requires:

- `docker-compose.yml`;
- `.env`;
- `ace/Config/`;
- `data/`;
- `scripts/`.

README, CHANGELOG, ROADMAP, VERSION, LICENSE, and `docs/` are optional. Missing optional content produces warnings but does not fail the backup. The manifest records optional paths that were included and skipped.

### Documentation browser

The read-only `/docs/` browser supports safe directory navigation and inline viewing of approved documentation formats. Path traversal, disallowed extensions, and unsafe filename rendering are blocked.

### Scope

No future Research Lab feature work is included. This package is limited to persistence, deployment ownership, backup robustness, installer automation, documentation access, and minor production polish.

### Release-candidate ownership correction

Testing identified inherited root ownership in Research Lab evidence and in `backups/runtime/notifications.json`. Owner preparation now elevates automatically, repairs both writable host trees, restores `.env` ownership after updates, and verifies access using the detected deployment identity.

Automation and Notifications continue using `backups/runtime/` in this release. Migration into the canonical `data/` root is intentionally deferred to avoid widening the corrective scope.
