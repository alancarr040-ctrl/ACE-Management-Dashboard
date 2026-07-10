from __future__ import annotations

import html
import os
from pathlib import Path
from urllib.parse import quote

from flask import Blueprint, Response, abort, send_from_directory, url_for


docs_bp = Blueprint("docs", __name__)

_ALLOWED_SUFFIXES = {
    ".md", ".txt", ".json", ".yaml", ".yml", ".csv", ".log",
    ".png", ".jpg", ".jpeg", ".webp", ".gif", ".svg",
}


def _docs_root() -> Path:
    configured = os.environ.get("ACEMD_DOCS_ROOT", "/opt/acserver/docs")
    return Path(configured).expanduser().resolve()


def _safe_target(relative_path: str = "") -> tuple[Path, Path]:
    root = _docs_root()
    target = (root / relative_path).resolve()
    try:
        target.relative_to(root)
    except ValueError:
        abort(404)
    return root, target


def _directory_response(root: Path, target: Path) -> Response:
    relative = target.relative_to(root)
    entries: list[str] = []
    for path in sorted(target.iterdir(), key=lambda item: (not item.is_dir(), item.name.lower())):
        child_relative = path.relative_to(root).as_posix()
        suffix = "/" if path.is_dir() else ""
        href = url_for("docs.docs_file", relative_path=child_relative) + suffix
        entries.append(
            f'<li><a href="{html.escape(href, quote=True)}">'
            f'{html.escape(path.name)}{suffix}</a></li>'
        )

    if relative == Path("."):
        parent_href = None
        title = "ACEMD Documentation"
    else:
        parent = relative.parent.as_posix()
        parent_href = url_for("docs.docs_index") if parent == "." else url_for("docs.docs_file", relative_path=parent) + "/"
        title = relative.as_posix()

    parent_link = "" if parent_href is None else f'<p><a href="{html.escape(parent_href, quote=True)}">Parent</a></p>'
    body = "\n".join(entries) or "<li>No documentation found.</li>"
    page = (
        "<!doctype html><html><head><meta charset='utf-8'>"
        f"<title>{html.escape(title)}</title>"
        "<meta name='viewport' content='width=device-width,initial-scale=1'>"
        "<style>body{font-family:system-ui,sans-serif;max-width:1000px;margin:2rem auto;padding:0 1rem;"
        "background:#111827;color:#e5e7eb}a{color:#93c5fd}li{margin:.45rem 0}"
        "code{background:#1f2937;padding:.15rem .35rem;border-radius:.25rem}</style></head><body>"
        f"{parent_link}<h1>{html.escape(title)}</h1>"
        "<p>Read-only files from <code>docs/</code>.</p>"
        f"<ul>{body}</ul></body></html>"
    )
    response = Response(page, mimetype="text/html")
    response.headers["Content-Security-Policy"] = "default-src 'none'; style-src 'unsafe-inline'; img-src 'self';"
    response.headers["X-Content-Type-Options"] = "nosniff"
    return response


@docs_bp.get("/docs/")
def docs_index() -> Response:
    root, target = _safe_target("")
    if not target.is_dir():
        abort(404)
    return _directory_response(root, target)


@docs_bp.get("/docs/<path:relative_path>")
def docs_file(relative_path: str):
    root, target = _safe_target(relative_path)
    if target.is_dir():
        return _directory_response(root, target)
    if not target.is_file() or target.suffix.lower() not in _ALLOWED_SUFFIXES:
        abort(404)

    response = send_from_directory(root, target.relative_to(root).as_posix(), as_attachment=False)
    response.headers["Content-Disposition"] = f"inline; filename*=UTF-8''{quote(target.name)}"
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["Content-Security-Policy"] = "default-src 'none'; img-src 'self'; style-src 'none'; sandbox"
    response.headers["Cache-Control"] = "no-store"
    return response
