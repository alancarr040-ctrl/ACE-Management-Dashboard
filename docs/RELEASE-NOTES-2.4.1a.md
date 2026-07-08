# Release Notes - 2.4.1a

## ACE Management Dashboard - Docker Compose Provider Hotfix

This hotfix corrects wrapper execution from inside the dashboard container when the Docker CLI is present but the Docker Compose plugin is missing.

### Fixed

- Added Docker Compose provider detection to `manage.sh` support libraries.
- Added support for both `docker compose` and legacy `docker-compose` providers.
- Improved failure output when Compose is unavailable.
- Updated the dashboard Dockerfile to install `docker-compose-plugin` with `docker-ce-cli`.
- Updated `doctor` checks to report the Compose provider and Docker socket status.

### Testing Focus

After rebuilding the dashboard container, verify:

- `./manage.sh doctor`
- `./manage.sh status`
- `./manage.sh server status`
- `./manage.sh server logs 150`
- `./manage.sh db status`
- `./manage.sh db logs 150`
