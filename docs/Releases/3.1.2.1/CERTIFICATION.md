# 3.1.2.1 Certification Record

## Status

**Release Candidate — certification in progress**

This document records executed tests against the deployment candidate. It must be updated to **Certified** only after every required test has passed and the final Git-published repository matches the tested server code.

## Test environment

- Platform: Debian Linux
- Deployment root: `/opt/acserver`
- Runtime: Docker Compose
- Dashboard container identity: deployment owner UID:GID
- Tested deployment owner: `1000:1000`
- Tested Docker socket GID: `995`
- Test date: July 10, 2026

## Executed results

| Area | Result | Evidence summary |
|---|---|---|
| Preparation script first run | PASS | Detected UID `1000`, GID `1000`, Docker GID `995`; validation passed. |
| Preparation script repeated run | PASS | Second run completed successfully without duplicate configuration or manual repair. |
| `.env` identity values | PASS | `ACEMD_UID=1000`, `ACEMD_GID=1000`, `ACEMD_DOCKER_GID=995`. |
| Dashboard runtime identity | PASS | Container reports `uid=1000 gid=1000 groups=1000,995`. |
| Writable ownership | PASS | `data/` and `backups/runtime/` are owned by the deployment account. |
| Dashboard pages | PASS | Dashboard, Operations, Management, Docker, Automation, Notifications, and remaining visible pages load. |
| Docker SDK access | PASS | `docker.from_env().ping()` returned `True` inside the dashboard container. |
| Dashboard rebuild | PASS | Rebuild and forced recreation completed successfully. |
| Repeated rebuild | PASS | Second rebuild test completed successfully. |
| Image removal persistence | PASS | Research Lab evidence persisted after image removal and rebuild. |
| Standard runtime backup | PASS | Database and infrastructure archives created; manifest and verification succeeded. |
| Optional backup path missing | PASS | Missing `ROADMAP.md` produced a warning; backup succeeded and recorded one skipped optional path. |
| Required backup path missing | PASS | Missing `data/` failed during preflight with exit status `2`. |

## Remaining certification tests

- Documentation browser traversal and unsafe-file rejection.
- Restore verification into a temporary destination.
- Final dashboard log review for hidden exceptions.
- Final Automation and Notifications state check after all tests.
- Comparison of the final Git-publishable repository against the tested server snapshot.

## Certification decision

Not yet certified. No blocker has been found in deployment ownership, Docker access, Research Lab persistence, or backup required/optional behavior. Final certification awaits the remaining tests and publication of the exact tested source baseline.
