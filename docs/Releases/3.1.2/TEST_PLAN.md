# 3.1.2 Test Plan

## Objective

Verify that ACEMD can store character snapshots and compare two snapshots without modifying ACE data.

## Scenario 1 - Create baseline snapshot

1. Open Administration → Research Lab.
2. Select a known character.
3. Enter a label such as `OBS-0001 Level 5 unspent baseline`.
4. Enter expected state notes.
5. Create Snapshot.

Expected: snapshot appears in Recent Snapshots with character name, row count, and table count.

## Scenario 2 - Create after snapshot

1. Perform one known action in game.
2. Return to Research Lab.
3. Create another snapshot for the same character.

Expected: a second snapshot appears.

## Scenario 3 - Create observation

1. Choose the before snapshot.
2. Choose the after snapshot.
3. Add action/outcome notes.
4. Create Observation.

Expected: observation appears with changed/added/removed row counts.

## Scenario 4 - View diff

1. Open the observation detail.

Expected: changed tables and changed columns are visible. No ACE write operation occurs.

## Known limitations

- Diff output is raw ACE data; semantic classification comes later.
- Snapshots are local JSON artifacts and are not yet linked to runtime backup metadata.
- Observation history does not yet promote hypotheses into the Knowledge Base automatically.
