# ACE Management Dashboard 3.1.1 Test Package

Phase 3.1.1 adds the first ACE Knowledge Base foundation for the administration layer.

This package remains read-only. It does not add SQL migrations and does not expose or mutate passwords, salts, hashes, or ACE game data.

## Highlights

- Adds Administration > Knowledge.
- Introduces a semantic property dictionary seed.
- Adds confidence levels: Unknown, Suspected, Inferred, Confirmed.
- Adds controlled observation planning for XP, skills, attributes, movement, and equipment tests.
- Fixes the Account Management summary card rendering bug where the Python dict `clear` method could leak into the UI.
- Updates project metadata to 3.1.1.

## Purpose

The Knowledge Base is the bridge between Phase 3 discovery and future administration modules. Raw ACE rows remain available for developer verification, but future admin pages should consume semantic concepts such as `Character.Name`, `Character.Level`, or `Account.Status` rather than raw table/type/value triples.
