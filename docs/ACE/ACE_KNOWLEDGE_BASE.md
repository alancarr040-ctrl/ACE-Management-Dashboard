# ACE Knowledge Base

The ACE Knowledge Base is the semantic translation layer between ACE discovery data and administrator-facing modules.

Raw ACE data often appears as table/type/value rows. Administrators need concepts instead:

- Character name
- Level
- Race
- Account status
- Last login
- Equipment
- Inventory
- Allegiance

Each Knowledge Base entry should include:

- Domain
- Property set
- Type ID
- Label
- Semantic key
- Confidence
- Source/provenance
- Edit safety
- Notes

## Confidence Levels

- Unknown: observed but not interpreted.
- Suspected: plausible human hypothesis.
- Inferred: supported by repeated observations.
- Confirmed: verified by source, documentation, or controlled action testing.

## Future Write Rule

No property should become editable until its meaning, validation rules, storage target, and rollback/safety behavior are confirmed.
