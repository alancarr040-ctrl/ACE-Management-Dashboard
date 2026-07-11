# ACE Property Dictionary

ACEMD resolves typed ACE properties through a stable composite key:

```text
(property group, numeric type)
```

Example:

```text
(INT, 198) -> ALLEGIANCE_SWEAR_TIMESTAMP_INT
```

The stored property value is never altered by the translation layer.

## Source and status

The initial dataset is derived from the community `AC DOM Properties.xlsx` workbook.

- Column A value `1`: `confirmed`
- Blank column A: `research`

The source workbook is not required at runtime. ACEMD ships the derived JSON dataset in `dashboard/data/property_dictionary.json`.

## Runtime API

`PropertyDictionaryService.lookup(group, type)` returns a definition or an explicit `Unknown Property` record. `annotate_rows()` adds `_property` metadata to read-only database rows.

## Refreshing from a workbook

```bash
python tools/import_property_dictionary.py "/path/to/AC DOM Properties.xlsx"
```

Review the generated diff before publishing it. Workbook imports must not silently promote research entries to confirmed status.

## Write policy

Dictionary labels are display metadata. Property writes require separate validation of value domains, constraints, side effects, and the installed ACE version.
