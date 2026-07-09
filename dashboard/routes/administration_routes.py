from __future__ import annotations

from flask import Blueprint, render_template, request

from routes.context import common_context, ace_data_service

administration_bp = Blueprint("administration", __name__)


def _ctx(active_tab: str):
    ctx = common_context(active_tab)
    ctx["ace_data"] = ace_data_service
    return ctx


@administration_bp.route("/administration/servers")
def servers_page():
    ctx = _ctx("servers")
    ctx["ace_overview"] = ace_data_service.get_overview()
    return render_template("index.html", **ctx)


@administration_bp.route("/administration/accounts")
def accounts_page():
    ctx = _ctx("accounts")
    search = request.args.get("q", "", type=str).strip()
    ctx["search_query"] = search
    ctx["account_data"] = ace_data_service.get_accounts(search=search)
    return render_template("index.html", **ctx)


@administration_bp.route("/administration/characters")
def characters_page():
    ctx = _ctx("characters")
    search = request.args.get("q", "", type=str).strip()
    ctx["search_query"] = search
    ctx["character_data"] = ace_data_service.get_characters(search=search)
    return render_template("index.html", **ctx)


@administration_bp.route("/administration/world")
def world_page():
    ctx = _ctx("world")
    ctx["world_data"] = ace_data_service.get_world_summary()
    return render_template("index.html", **ctx)


@administration_bp.route("/administration/database")
def database_page():
    ctx = _ctx("database")
    ctx["schema_inventory"] = ace_data_service.get_schema_inventory()
    return render_template("index.html", **ctx)
