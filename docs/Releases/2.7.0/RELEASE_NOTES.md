# Release Notes - 2.7.0 Scheduler & Automation

## Added

- New Automation tab.
- New `/automation` page.
- New `/api/automation` endpoint.
- Request-driven automation scheduler.
- Built-in read-only automation jobs.
- Manual **Run Now** support for built-in jobs.
- Automation job history stored in runtime JSON.
- Automation events published to the Events subsystem.
- Automation documentation under `docs/Automation/`.

## Changed

- Navigation now includes Automation.
- Runtime version metadata updated to 2.7.0-dev.
- `.gitignore` now ignores the repository-root `Test/` staging folder.

## Safety

No write-capable automation jobs are introduced in this release.
