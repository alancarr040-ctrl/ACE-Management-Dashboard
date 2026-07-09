# ACEMD 3.0.2 - ACE Relationship Explorer

## Purpose

3.0.2 extends the ACE Data Explorer with read-only relationship-aware views. The goal is to help ACEMD understand how ACE auth, shard, and world data connect before any future write-capable administration modules are introduced.

## Added

- Added Administration > Relationships module.
- Added account-to-character relationship overview.
- Added character-to-biota relationship overview.
- Added biota-to-property-table relationship counts.
- Added character-to-world-template relationship lookup by WCID/class id.
- Added character relationship detail page.
- Added relationship chain UI for Account -> Character -> Biota -> Properties -> World Template.
- Added links from character detail to the relationship explorer.

## Cleanup in testing

- Replaced hard-coded property-table ordering with schema-aware ordering.
- Property row lookups now prefer `type`, then `key`, then other safe identifying columns when available.
- Relationship views no longer assume all ACE property tables share the same column layout.

## Safety

- All ACE access remains routed through ACEDataService.
- All new relationship views are read-only.
- No mutation routes, forms, or write SQL were added.
- Sensitive sample-row redaction remains in place.

## Testing Notes

- Verify Administration > Relationships loads.
- Verify a live character appears in the relationship entry-point table.
- Open the character relationship view and confirm property counts, location/skill/attribute tables, and world template lookup render safely.
