# Test Plan - 3.1.3

## Objective

Verify that ACE community/wiki registry HTML can be converted into reviewable Markdown reference seeds.

## Test 1 - Local HTML file

1. Save a wiki registry page as HTML.
2. Run:

   ```bash
   python tools/import_ace_wiki_registry.py /path/to/page.html --output docs/References/ACE-Community-Wiki
   ```

3. Confirm a Markdown file is created.
4. Confirm tables are converted to Markdown.
5. Confirm front matter includes `status: reference-unverified`.

## Test 2 - Folder import

1. Place several saved `.html` files in a folder.
2. Run:

   ```bash
   python tools/import_ace_wiki_registry.py /path/to/folder --output docs/References/ACE-Community-Wiki
   ```

3. Confirm one Markdown file is created per HTML page.
4. Confirm `manifest.json` and `README.md` are generated.

## Test 3 - URL import, optional

Only run when the host has internet access:

```bash
python tools/import_ace_wiki_registry.py https://asheron.fandom.com/wiki/INT --output docs/References/ACE-Community-Wiki
```

## Test 4 - Link-following, optional

Only run cautiously with a small page limit:

```bash
python tools/import_ace_wiki_registry.py https://asheron.fandom.com/wiki/INT --output docs/References/ACE-Community-Wiki --follow-links --max-pages 10
```

## Expected Result

The repository contains clean Markdown reference seeds that are suitable for Git review. Imported entries must not be considered confirmed ACEMD semantic knowledge until verified.
