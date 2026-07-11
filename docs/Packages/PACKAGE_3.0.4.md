# Package 3.0.4 — ACE Property Dictionary

## Purpose

Create the shared read-only translation service that maps ACE property storage identifiers to documented property definitions.

## Source hierarchy

1. ACE source definitions when available.
2. Community `AC DOM Properties.xlsx` definitions.
3. Local research only for undocumented or behavior-specific gaps.

## Dictionary assets

The importer generates `dashboard/data/property_dictionary.json` as the version-controlled source asset. Release packaging also installs the same generated dictionary at `data/property_dictionary.json`, because the deployment bind-mounts `/opt/acserver/data` to `/app/data` in the dashboard container.

Normal runtime resolution order:

1. explicit `ACEMD_PROPERTY_DICTIONARY` path;
2. `ACEMD_DATA_ROOT/property_dictionary.json`;
3. packaged development/source-tree fallback.

A missing or malformed file produces a visible diagnostic warning in the Property Dictionary page.

## Lookup contract

```text
(property group, numeric type) -> dictionary definition
```

Example:

```text
(INT, 198) -> ALLEGIANCE_SWEAR_TIMESTAMP_INT
```

Unknown entries return an explicit fallback and never suppress raw ACE data.

## Write policy

Dictionary data is display metadata only. It does not authorize ACE database mutation.
