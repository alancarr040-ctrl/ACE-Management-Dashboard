# ACE Property Dictionary Plan

Phase 3.1 starts with Account Management. Character-friendly administration should not be built by guessing raw property ids directly in templates.

Future semantic character administration should use a centralized dictionary and decoder service:

```text
ACE raw property tables
  -> ACE property dictionary
  -> semantic decoder service
  -> administrator-facing character views
```

## Dictionary entry shape

Each mapping should carry at least:

- property group, such as string, int, bool, float, DID, IID, position, attribute, skill
- numeric type/key
- friendly label
- confidence, such as confirmed, inferred, or unknown
- source note, such as ACE source, emulator enum, observed database sample, or local verification
- admin display group, such as identity, status, vitals, allegiance, housing, inventory, equipment, spells, or raw

## Working example

The following mappings are plausible based on observed data, but should remain marked inferred until confirmed:

| Group | Type | Possible Label | Confidence |
| --- | ---: | --- | --- |
| string | 1 | Name | inferred |
| string | 3 | Sex | inferred |
| string | 4 | Race | inferred |
| string | 5 | Title | inferred |
| string | 43 | Born | inferred |

## Rule

Raw ACE property data remains available for verification, but administrator pages should prefer semantic summaries once mappings are confirmed or clearly marked as inferred.
