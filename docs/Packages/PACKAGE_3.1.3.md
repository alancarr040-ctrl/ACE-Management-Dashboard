# Package 3.1.3 - ACE Registry Reference Importer

## Purpose

Adds a tool for importing ACE community/wiki registry pages into Markdown so ACEMD can preserve reference seed data in Git without treating it as confirmed Knowledge Base truth.

## Included

- `tools/import_ace_wiki_registry.py`
- `docs/References/ACE-Community-Wiki/README.md`
- `docs/References/ACE-Community-Wiki/sources.example.json`
- Release documentation and project metadata updates.

## Policy

Imported registry content is reference-only until verified. No write operation should rely solely on imported community data.

## SQL

No SQL migration.
