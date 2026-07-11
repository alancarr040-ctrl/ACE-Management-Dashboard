# Test Plan — 3.0.4

## Deployment

1. Back up the current ACEMD source.
2. Extract the ZIP directly into `/opt/acserver`.
3. Run `./scripts/prepare-dashboard-owner.sh /opt/acserver`.
4. Rebuild and recreate `ace-dashboard`.
5. Confirm the Project Information panel reports version/build `3.0.4` and status `Release`.

## Runtime dictionary

1. Confirm `/opt/acserver/dashboard/data/property_dictionary.json` exists.
2. Confirm `/opt/acserver/data/property_dictionary.json` exists.
3. Confirm `/app/data/property_dictionary.json` exists inside `ace-dashboard`.
4. Run:

```bash
docker compose exec -T ace-dashboard python - <<'PY'
from services.property_dictionary_service import PropertyDictionaryService
service = PropertyDictionaryService()
print("Dictionary path:", service.path)
print("Exists:", service.path.exists())
print("Entries:", len(service._entries))
print("Load error:", service.load_error or "None")
PY
```

Expected: `/app/data/property_dictionary.json`, `True`, `899`, and `None`.

## Knowledge Base preservation

1. Open `/administration/knowledge#knowledge`.
2. Confirm the five existing semantic seed entries remain present.
3. Confirm the Controlled Observation Plan remains present.
4. Confirm **Open Property Dictionary** is visible.

## Dictionary browser

1. Open `/administration/knowledge/properties#property-dictionary`.
2. Confirm 899 entries, 576 confirmed, 323 research, and eight groups.
3. Search `198`; confirm `ALLEGIANCE_SWEAR_TIMESTAMP_INT` appears.
4. Search `ITEM_TYPE_INT`; confirm it resolves as `INT 1`.
5. Test group/status filters, pagination, and per-page selection.

## Character integration

1. Open a character detail page.
2. Confirm mapped rows display friendly labels and raw identifiers.
3. Confirm unknown types display **Unknown Property** without hiding raw values.

## Failure visibility

1. In a disposable test environment, temporarily move the runtime dictionary away.
2. Restart the dashboard.
3. Confirm the Property Dictionary page shows a visible load warning containing the expected path.
4. Restore the file and restart the dashboard.

## Safety

1. Confirm no ACE schema migration runs.
2. Confirm no ACE data mutation occurs.
3. Confirm dashboard database access remains read-only.
