# ACE Community Wiki Reference Seeds

This directory is reserved for Markdown reference material imported from community-maintained Asheron's Call wiki pages.

These files are **reference seeds**, not confirmed ACEMD Knowledge Base entries. They may be incomplete, outdated, or different from a specific ACE server version. Use them to accelerate semantic mapping, then verify important entries through ACE source review or Research Lab observations before using them for administration or write tooling.

## Importer

Use the repository tool:

```bash
python tools/import_ace_wiki_registry.py saved_html_folder \
  --output docs/References/ACE-Community-Wiki
```

The importer also supports URL input when the environment has internet access:

```bash
python tools/import_ace_wiki_registry.py https://asheron.fandom.com/wiki/INT \
  --output docs/References/ACE-Community-Wiki
```

To gather linked registry pages from a starting page:

```bash
python tools/import_ace_wiki_registry.py https://asheron.fandom.com/wiki/INT \
  --output docs/References/ACE-Community-Wiki \
  --follow-links \
  --max-pages 25
```

## Output policy

Each generated Markdown file includes front matter:

```yaml
status: reference-unverified
verified_by_acemd: false
use_policy: seed-only; do not enable write operations from this reference alone
```

The importer writes:

- one Markdown file per imported page,
- `manifest.json` with source metadata,
- `README.md` index listing imported files.

## Storage policy

Do not store large raw HTML archives here unless there is a specific reason. Prefer storing the converted Markdown plus source URL metadata.
