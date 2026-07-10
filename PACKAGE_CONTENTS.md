# ACEMD 3.1.2.1 Release Candidate — Package Contents

This is a changed-files-only corrective package for the deployed 3.1.2.1 finalization test.

Included paths:

```text
CHANGELOG.md
README.md
PACKAGE_CONTENTS.md
scripts/prepare-dashboard-owner.sh
docs/Releases/3.1.2.1/README.md
docs/Releases/3.1.2.1/OWNER_STORAGE.md
docs/Releases/3.1.2.1/RELEASE_NOTES.md
docs/Releases/3.1.2.1/TEST_PLAN.md
```

No `Test/` or `test/` directory is included. The package does not migrate Automation or Notifications; it repairs their existing writable runtime-state location.
