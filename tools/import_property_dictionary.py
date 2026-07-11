#!/usr/bin/env python3
"""Import AC DOM Properties.xlsx into ACEMD's property dictionary JSON.

The importer uses only Python's standard library. It expects the workbook layout
used by the community AC DOM Properties document:
  A = confirmed flag (1 means confirmed)
  B = numeric type
  C = official property name
  D = description
  E = lookup table/reference
  F = notes
  G = additional reference
"""
from __future__ import annotations

import argparse
import json
import re
import zipfile
from pathlib import Path
from xml.etree import ElementTree as ET

NS = {"m": "http://schemas.openxmlformats.org/spreadsheetml/2006/main",
      "r": "http://schemas.openxmlformats.org/officeDocument/2006/relationships"}

SECTIONS = {
    "int": (26, 416),
    "bool": (419, 549),
    "float": (552, 723),
    "string": (726, 778),
    "int64": (781, 807),
    "position": (812, 839),
    "did": (842, 903),
    "iid": (906, 982),
}

def shared_strings(archive: zipfile.ZipFile) -> list[str]:
    try:
        root = ET.fromstring(archive.read("xl/sharedStrings.xml"))
    except KeyError:
        return []
    values = []
    for item in root.findall("m:si", NS):
        values.append("".join(node.text or "" for node in item.iterfind(".//m:t", NS)))
    return values

def master_sheet_path(archive: zipfile.ZipFile) -> str:
    workbook = ET.fromstring(archive.read("xl/workbook.xml"))
    rels = ET.fromstring(archive.read("xl/_rels/workbook.xml.rels"))
    targets = {rel.attrib["Id"]: rel.attrib["Target"] for rel in rels}
    for sheet in workbook.findall("m:sheets/m:sheet", NS):
        if sheet.attrib.get("name") == "Master List":
            rel_id = sheet.attrib.get(f"{{{NS['r']}}}id")
            target = targets[rel_id].lstrip("/")
            return target if target.startswith("xl/") else f"xl/{target}"
    raise RuntimeError("Workbook does not contain a Master List sheet.")

def cell_value(cell: ET.Element, strings: list[str]):
    kind = cell.attrib.get("t")
    value = cell.find("m:v", NS)
    if value is None:
        inline = cell.find("m:is/m:t", NS)
        return inline.text if inline is not None else None
    text = value.text or ""
    if kind == "s":
        return strings[int(text)]
    if kind == "b":
        return text == "1"
    try:
        number = float(text)
        return int(number) if number.is_integer() else number
    except ValueError:
        return text

def column_index(reference: str) -> int:
    letters = re.match(r"[A-Z]+", reference).group(0)
    value = 0
    for letter in letters:
        value = value * 26 + ord(letter) - 64
    return value - 1

def friendly_name(name: str) -> str:
    cleaned = re.sub(r"_(INT64|INT|BOOL|FLOAT|STRING|DID|IID|POSITION)$", "", name)
    return cleaned.replace("_", " ").title()

def import_workbook(source: Path) -> dict:
    with zipfile.ZipFile(source) as archive:
        strings = shared_strings(archive)
        sheet = ET.fromstring(archive.read(master_sheet_path(archive)))
    rows = {}
    for row_node in sheet.findall("m:sheetData/m:row", NS):
        row_number = int(row_node.attrib["r"])
        row = [None] * 7
        for cell in row_node.findall("m:c", NS):
            index = column_index(cell.attrib["r"])
            if index < len(row):
                row[index] = cell_value(cell, strings)
        rows[row_number] = row

    entries = []
    for group, (start, end) in SECTIONS.items():
        for row_number in range(start, end + 1):
            flag, type_id, name, description, lookup, notes, reference = rows.get(row_number, [None] * 7)
            if not isinstance(type_id, (int, float)) or not isinstance(name, str) or not name.strip():
                continue
            entries.append({
                "group": group,
                "type": int(type_id),
                "name": name.strip(),
                "friendly_name": friendly_name(name.strip()),
                "description": description.strip() if isinstance(description, str) else "",
                "lookup": lookup.strip() if isinstance(lookup, str) else "",
                "notes": notes.strip() if isinstance(notes, str) else "",
                "reference": reference.strip() if isinstance(reference, str) else "",
                "status": "confirmed" if flag == 1 else "research",
                "origin": "Community Spreadsheet",
                "source": f"{source.name} / Master List",
                "source_row": row_number,
            })
    entries.sort(key=lambda row: (row["group"], row["type"], row["name"]))
    return {
        "schema_version": 1,
        "dictionary_version": source.stem,
        "source": {
            "name": source.name,
            "sheet": "Master List",
            "status_rule": "Column A value 1 = confirmed; blank = research/test",
            "redistribution": "Derived structured data only",
        },
        "entries": entries,
    }

def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("workbook", type=Path)
    parser.add_argument("--output", type=Path, default=Path("dashboard/data/property_dictionary.json"))
    args = parser.parse_args()
    payload = import_workbook(args.workbook)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(f"Imported {len(payload['entries'])} property definitions to {args.output}")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
