#!/usr/bin/env python3
"""Convert ACE community wiki registry HTML pages into Markdown reference seeds.

This importer is intentionally conservative. It stores community/wiki content as
reference material, not as confirmed ACEMD knowledge. The generated Markdown is
intended for Git review and later Knowledge Base seeding/verification.

Supported inputs:
  * local HTML files
  * directories containing .html/.htm files
  * URLs
  * manifest JSON files containing a list under "sources"

Optional link following can crawl a small number of same-domain wiki links so
registry pages such as INT -> ITEM_TYPE_INT -> CREATURE_TYPE_INT can be captured
without manually saving every page.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
import time
from dataclasses import dataclass, field
from datetime import datetime, timezone
from html import unescape
from html.parser import HTMLParser
from pathlib import Path
from typing import Iterable
from urllib.parse import urldefrag, urljoin, urlparse
from urllib.request import Request, urlopen

USER_AGENT = "ACEMD-Reference-Importer/3.1.3"
DEFAULT_OUTPUT = Path("docs/References/ACE-Community-Wiki")


@dataclass
class LinkRef:
    text: str
    href: str


@dataclass
class MarkdownCell:
    text: str = ""
    links: list[LinkRef] = field(default_factory=list)


@dataclass
class ParsedTable:
    rows: list[list[MarkdownCell]] = field(default_factory=list)


@dataclass
class ParsedPage:
    title: str = "Untitled Reference"
    headings: list[str] = field(default_factory=list)
    paragraphs: list[str] = field(default_factory=list)
    tables: list[ParsedTable] = field(default_factory=list)
    links: list[LinkRef] = field(default_factory=list)


class RegistryHTMLParser(HTMLParser):
    """Small HTML parser tuned for wiki-style registry tables.

    It does not try to produce a full Markdown version of a page. Instead it
    extracts the durable parts ACEMD needs: title, headings, paragraphs, tables,
    and links inside table cells.
    """

    def __init__(self, source_url: str | None = None):
        super().__init__(convert_charrefs=True)
        self.source_url = source_url or ""
        self.page = ParsedPage()
        self._tag_stack: list[str] = []
        self._capture_text: list[str] = []
        self._capture_kind: str | None = None
        self._current_table: ParsedTable | None = None
        self._current_row: list[MarkdownCell] | None = None
        self._current_cell: MarkdownCell | None = None
        self._current_link_href: str | None = None
        self._current_link_text: list[str] = []
        self._in_title = False
        self._skip_depth = 0

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        tag = tag.lower()
        self._tag_stack.append(tag)
        attrs_dict = {k.lower(): (v or "") for k, v in attrs}

        if tag in {"script", "style", "noscript", "svg"}:
            self._skip_depth += 1
            return

        if tag == "title":
            self._in_title = True
            self._capture_text = []
            return
        if tag in {"h1", "h2", "h3"}:
            self._capture_kind = tag
            self._capture_text = []
            return
        if tag == "p":
            self._capture_kind = "p"
            self._capture_text = []
            return
        if tag == "table":
            self._current_table = ParsedTable()
            return
        if tag == "tr" and self._current_table is not None:
            self._current_row = []
            return
        if tag in {"td", "th"} and self._current_row is not None:
            self._current_cell = MarkdownCell()
            return
        if tag == "a":
            href = attrs_dict.get("href", "").strip()
            if href:
                self._current_link_href = href
                self._current_link_text = []
            return
        if tag == "br":
            self._append_text(" ")

    def handle_endtag(self, tag: str) -> None:
        tag = tag.lower()
        if tag in {"script", "style", "noscript", "svg"} and self._skip_depth:
            self._skip_depth -= 1
        if self._skip_depth:
            return

        if tag == "title" and self._in_title:
            title = clean_text(" ".join(self._capture_text))
            if title and self.page.title == "Untitled Reference":
                self.page.title = title.split(" | ")[0].strip()
            self._in_title = False
            self._capture_text = []
        elif tag in {"h1", "h2", "h3"} and self._capture_kind == tag:
            text = clean_text(" ".join(self._capture_text))
            if text:
                if tag == "h1":
                    self.page.title = text
                else:
                    self.page.headings.append(text)
            self._capture_kind = None
            self._capture_text = []
        elif tag == "p" and self._capture_kind == "p":
            text = clean_text(" ".join(self._capture_text))
            if text and len(text) > 20:
                self.page.paragraphs.append(text)
            self._capture_kind = None
            self._capture_text = []
        elif tag in {"td", "th"} and self._current_cell is not None and self._current_row is not None:
            self._current_cell.text = clean_text(self._current_cell.text)
            self._current_row.append(self._current_cell)
            self._current_cell = None
        elif tag == "tr" and self._current_row is not None and self._current_table is not None:
            if any(cell.text or cell.links for cell in self._current_row):
                self._current_table.rows.append(self._current_row)
            self._current_row = None
        elif tag == "table" and self._current_table is not None:
            if self._current_table.rows:
                self.page.tables.append(self._current_table)
            self._current_table = None
        elif tag == "a" and self._current_link_href:
            text = clean_text(" ".join(self._current_link_text)) or self._current_link_href
            href = self._normalize_href(self._current_link_href)
            ref = LinkRef(text=text, href=href)
            self.page.links.append(ref)
            if self._current_cell is not None:
                self._current_cell.links.append(ref)
                if text not in self._current_cell.text:
                    self._current_cell.text = f"{self._current_cell.text} {text}".strip()
            self._current_link_href = None
            self._current_link_text = []

        if self._tag_stack:
            self._tag_stack.pop()

    def handle_data(self, data: str) -> None:
        if self._skip_depth:
            return
        text = unescape(data)
        if not text.strip():
            return
        if self._current_link_href:
            self._current_link_text.append(text)
        self._append_text(text)

    def _append_text(self, text: str) -> None:
        if self._current_cell is not None:
            self._current_cell.text = f"{self._current_cell.text} {text}".strip()
        elif self._in_title or self._capture_kind:
            self._capture_text.append(text)

    def _normalize_href(self, href: str) -> str:
        if not href:
            return href
        return urljoin(self.source_url, href) if self.source_url else href


def clean_text(value: str) -> str:
    return re.sub(r"\s+", " ", unescape(value or "")).strip()


def slugify(value: str) -> str:
    value = clean_text(value).lower()
    value = re.sub(r"[^a-z0-9]+", "-", value).strip("-")
    return value or "reference"


def is_url(value: str) -> bool:
    return value.startswith("http://") or value.startswith("https://")


def read_source(source: str, timeout: int = 30) -> tuple[str, str | None]:
    if is_url(source):
        req = Request(source, headers={"User-Agent": USER_AGENT})
        with urlopen(req, timeout=timeout) as response:  # noqa: S310 - intentional user-supplied reference fetcher
            charset = response.headers.get_content_charset() or "utf-8"
            return response.read().decode(charset, errors="replace"), response.geturl()
    path = Path(source)
    return path.read_text(encoding="utf-8", errors="replace"), None


def parse_page(html: str, source_url: str | None = None) -> ParsedPage:
    parser = RegistryHTMLParser(source_url=source_url)
    parser.feed(html)
    parser.close()
    return parser.page


def cell_to_markdown(cell: MarkdownCell) -> str:
    text = clean_text(cell.text).replace("|", "\\|")
    for link in cell.links:
        link_text = clean_text(link.text)
        if not link_text:
            continue
        md_link = f"[{link_text.replace('|', '\\|')}]({link.href})"
        escaped_link_text = link_text.replace("|", "\\|")
        if escaped_link_text in text:
            text = text.replace(escaped_link_text, md_link, 1)
    return text


def table_to_markdown(table: ParsedTable) -> str:
    rows = table.rows
    if not rows:
        return ""
    max_cols = max(len(r) for r in rows)
    normalized = [r + [MarkdownCell()] * (max_cols - len(r)) for r in rows]
    header = [cell_to_markdown(c) or f"Column {i + 1}" for i, c in enumerate(normalized[0])]
    body = normalized[1:]
    lines = [
        "| " + " | ".join(header) + " |",
        "| " + " | ".join("---" for _ in header) + " |",
    ]
    for row in body:
        lines.append("| " + " | ".join(cell_to_markdown(c) for c in row) + " |")
    return "\n".join(lines)


def front_matter(page: ParsedPage, source: str, source_url: str | None) -> str:
    imported_at = datetime.now(timezone.utc).isoformat(timespec="seconds")
    return "\n".join([
        "---",
        f"title: {json.dumps(page.title)}",
        f"source: {json.dumps(source_url or source)}",
        "source_type: community-reference",
        "status: reference-unverified",
        "verified_by_acemd: false",
        f"imported_at: {json.dumps(imported_at)}",
        "use_policy: seed-only; do not enable write operations from this reference alone",
        "---",
        "",
    ])


def page_to_markdown(page: ParsedPage, source: str, source_url: str | None) -> str:
    lines: list[str] = [front_matter(page, source, source_url), f"# {page.title}", ""]
    lines.extend([
        "> **Reference seed only.** This page was converted from community/wiki HTML for ACEMD reference use.",
        "> Treat it as imported documentation until it is confirmed by ACE source review or ACEMD observations.",
        "",
    ])
    if page.paragraphs:
        lines.append("## Extracted Notes")
        lines.append("")
        for p in page.paragraphs[:8]:
            lines.append(p)
            lines.append("")
    for index, table in enumerate(page.tables, start=1):
        lines.append(f"## Table {index}")
        lines.append("")
        lines.append(table_to_markdown(table))
        lines.append("")
    unique_links: dict[str, LinkRef] = {}
    for link in page.links:
        if link.href and not link.href.startswith("#"):
            unique_links.setdefault(link.href, link)
    if unique_links:
        lines.append("## Source Links")
        lines.append("")
        for link in sorted(unique_links.values(), key=lambda item: (item.text.lower(), item.href))[:250]:
            text = link.text.replace("[", "\\[").replace("]", "\\]")
            lines.append(f"- [{text}]({link.href})")
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def discover_inputs(inputs: Iterable[str]) -> list[str]:
    discovered: list[str] = []
    for item in inputs:
        if item.endswith(".json") and Path(item).exists():
            data = json.loads(Path(item).read_text(encoding="utf-8"))
            discovered.extend(str(src) for src in data.get("sources", []))
            continue
        if is_url(item):
            discovered.append(item)
            continue
        path = Path(item)
        if path.is_dir():
            discovered.extend(str(p) for p in sorted(path.rglob("*.htm*")))
        elif path.exists():
            discovered.append(str(path))
        else:
            raise FileNotFoundError(f"Input not found: {item}")
    return discovered


def link_is_followable(href: str, root_url: str) -> bool:
    href, _ = urldefrag(href)
    if not href:
        return False
    parsed = urlparse(href)
    root = urlparse(root_url)
    if parsed.netloc and parsed.netloc != root.netloc:
        return False
    if not parsed.path.startswith("/wiki/"):
        return False
    lowered = parsed.path.lower()
    blocked_prefixes = ("/wiki/special:", "/wiki/file:", "/wiki/category:", "/wiki/template:", "/wiki/help:")
    return not any(lowered.startswith(prefix) for prefix in blocked_prefixes)


def write_index(output_dir: Path, manifest: list[dict[str, object]]) -> None:
    lines = [
        "# ACE Community Wiki Reference Seeds",
        "",
        "These Markdown files are imported reference seeds. They are not ACEMD-confirmed knowledge.",
        "",
        "Use these documents to seed the ACE registry, then verify entries through ACE source review or Research Lab observations before enabling write operations.",
        "",
        "| Title | File | Tables | Source |",
        "| --- | --- | ---: | --- |",
    ]
    for row in manifest:
        title = str(row.get("title", ""))
        filename = str(row.get("file", ""))
        tables = int(row.get("tables", 0))
        source = str(row.get("source", ""))
        lines.append(f"| {title} | [{filename}]({filename}) | {tables} | {source} |")
    lines.append("")
    (output_dir / "README.md").write_text("\n".join(lines), encoding="utf-8")


def import_sources(args: argparse.Namespace) -> int:
    output_dir = Path(args.output)
    output_dir.mkdir(parents=True, exist_ok=True)
    queue = discover_inputs(args.inputs)
    seen_sources: set[str] = set()
    manifest: list[dict[str, object]] = []

    while queue and len(seen_sources) < args.max_pages:
        source = queue.pop(0)
        source_key = urldefrag(source)[0] if is_url(source) else str(Path(source).resolve())
        if source_key in seen_sources:
            continue
        seen_sources.add(source_key)
        try:
            html, source_url = read_source(source, timeout=args.timeout)
            page = parse_page(html, source_url or source if is_url(source) else None)
        except Exception as exc:  # noqa: BLE001 - CLI should continue through bad pages when requested
            if args.keep_going:
                print(f"WARN: failed to import {source}: {exc}", file=sys.stderr)
                continue
            raise
        slug = slugify(page.title)
        target = output_dir / f"{slug}.md"
        counter = 2
        while target.exists() and args.no_overwrite:
            target = output_dir / f"{slug}-{counter}.md"
            counter += 1
        target.write_text(page_to_markdown(page, source, source_url), encoding="utf-8")
        manifest.append({
            "title": page.title,
            "file": target.name,
            "source": source_url or source,
            "tables": len(page.tables),
            "links": len(page.links),
        })
        print(f"Imported {page.title} -> {target}")

        if args.follow_links and is_url(source_url or source):
            root_url = source_url or source
            for link in page.links:
                href = urldefrag(urljoin(root_url, link.href))[0]
                if link_is_followable(href, root_url) and href not in seen_sources and href not in queue:
                    queue.append(href)
            if args.delay:
                time.sleep(args.delay)

    (output_dir / "manifest.json").write_text(json.dumps(manifest, indent=2, sort_keys=True), encoding="utf-8")
    write_index(output_dir, manifest)
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Import ACE community wiki registry HTML into Markdown reference seeds.")
    parser.add_argument("inputs", nargs="+", help="HTML files, directories, URLs, or JSON manifest files with a 'sources' list.")
    parser.add_argument("--output", default=str(DEFAULT_OUTPUT), help=f"Output directory. Default: {DEFAULT_OUTPUT}")
    parser.add_argument("--follow-links", action="store_true", help="Follow same-domain /wiki/ links from URL inputs.")
    parser.add_argument("--max-pages", type=int, default=25, help="Maximum pages to import when following links. Default: 25.")
    parser.add_argument("--delay", type=float, default=0.5, help="Delay between followed URL requests. Default: 0.5 seconds.")
    parser.add_argument("--timeout", type=int, default=30, help="HTTP timeout in seconds. Default: 30.")
    parser.add_argument("--keep-going", action="store_true", help="Continue if a page fails to import.")
    parser.add_argument("--no-overwrite", action="store_true", help="Do not overwrite an existing Markdown file; append a numeric suffix instead.")
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    return import_sources(args)


if __name__ == "__main__":
    raise SystemExit(main())
