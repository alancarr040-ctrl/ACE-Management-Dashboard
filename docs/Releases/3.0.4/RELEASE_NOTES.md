# Release Notes — 3.0.4

## ACE Property Dictionary Foundation

- Preserves the existing ACE Knowledge Base and observation plans.
- Adds a distinct, searchable Property Dictionary page.
- Imports 899 definitions derived from `AC DOM Properties.xlsx`.
- Preserves 576 confirmed and 323 research/test definitions across eight property groups.
- Adds a shared `(property group, type)` lookup service.
- Annotates raw character property rows while preserving raw group, type, and value.
- Provides explicit unknown-property fallback.
- Adds a repeatable standard-library XLSX importer.
- Performs no writes to ACE databases.

## Runtime persistence correction

- Installs `property_dictionary.json` under `data/`, which is bind-mounted into the dashboard container as `/app/data`.
- Retains the source copy under `dashboard/data/` for version control and importer output.
- Supports the `ACEMD_PROPERTY_DICTIONARY` environment variable for an explicit override.
- Uses `ACEMD_DATA_ROOT/property_dictionary.json` as the normal runtime location.
- Displays a visible diagnostic warning and resolved path if the dictionary cannot be loaded, instead of silently presenting zero entries.
