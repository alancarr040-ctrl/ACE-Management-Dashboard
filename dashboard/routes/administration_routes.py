from __future__ import annotations

from flask import Blueprint, redirect, render_template, request

from routes.context import common_context, ace_data_service, research_service

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
    status = request.args.get("status", "all", type=str).strip() or "all"
    access = request.args.get("access", "all", type=str).strip() or "all"
    sort = request.args.get("sort", "accountName", type=str).strip() or "accountName"
    page = request.args.get("page", 1, type=int)
    per_page = request.args.get("per_page", 25, type=int)
    ctx["search_query"] = search
    ctx["account_data"] = ace_data_service.get_accounts(search=search, status=status, access=access, sort=sort, page=page, per_page=per_page)
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


@administration_bp.route("/administration/knowledge")
def knowledge_page():
    ctx = _ctx("knowledge")
    ctx["knowledge_base"] = ace_data_service.get_ace_knowledge_base()
    return render_template("index.html", **ctx)


@administration_bp.route("/administration/research", methods=["GET", "POST"])
def research_page():
    message = None
    if request.method == "POST":
        action = request.form.get("action", "", type=str)
        if action == "snapshot":
            character_id = request.form.get("character_id", 0, type=int)
            result = research_service.create_snapshot(
                character_id=character_id,
                label=request.form.get("label", "", type=str),
                notes=request.form.get("notes", "", type=str),
                expected_state=request.form.get("expected_state", "", type=str),
            )
            message = {"level": "ok" if result.get("ok") else "warning", "text": result.get("error") or "Character snapshot created."}
        elif action == "observation":
            result = research_service.create_observation(
                title=request.form.get("title", "", type=str),
                before_snapshot_id=request.form.get("before_snapshot_id", "", type=str),
                after_snapshot_id=request.form.get("after_snapshot_id", "", type=str),
                action_notes=request.form.get("action_notes", "", type=str),
                outcome_notes=request.form.get("outcome_notes", "", type=str),
            )
            message = {"level": "ok" if result.get("ok") else "warning", "text": result.get("error") or f"Observation {result.get('observation', {}).get('observation_id', '')} created."}
    ctx = _ctx("research")
    ctx["message"] = message
    ctx["research_lab"] = research_service.get_dashboard()
    ctx["character_data"] = ace_data_service.get_characters(limit=200)
    return render_template("index.html", **ctx)


@administration_bp.route("/administration/research/observations/<observation_id>")
def observation_detail_page(observation_id: str):
    ctx = _ctx("observation_detail")
    ctx["observation_detail"] = research_service.get_observation(observation_id)
    return render_template("index.html", **ctx)


@administration_bp.route("/administration/database")
def database_page():
    ctx = _ctx("database")
    ctx["schema_inventory"] = ace_data_service.get_schema_inventory()
    return render_template("index.html", **ctx)
