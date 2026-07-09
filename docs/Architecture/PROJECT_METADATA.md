# ACEMD Project Metadata

ACEMD 3.0.3 centralizes project metadata so version, phase, milestone, status, and build information come from one certified source of truth.

## Primary metadata file

```text
dashboard/config/project.json
```

This file is consumed by `dashboard/services/project_service.py` and rendered by the shared header Project Information card and the About page.

## Required fields

- `product`
- `short_name`
- `version`
- `phase`
- `milestone`
- `status`
- `build`

## Policy

Do not hardcode ACEMD version or milestone text in templates or routes. Pages should receive `project` from `common_context()` and render metadata from that object.

Legacy flat files such as `dashboard/VERSION`, `dashboard/PHASE`, `dashboard/MILESTONE`, `dashboard/STATUS`, and `dashboard/BUILD` may remain for compatibility, but they are fallback sources only. The JSON file is authoritative for Phase 3.0.3 and later.

## Reason

During the 3.0.1 development cycle, a changed-file package briefly caused the Project Information panel to regress to an older 2.2.0 development version. Centralizing metadata prevents that class of "de-versioning" problem.
