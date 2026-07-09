from __future__ import annotations

from flask import Blueprint, jsonify, render_template, request
from routes.context import ace_data_service, common_context

administration_bp = Blueprint('administration', __name__)


def _limit() -> int:
    try:
        return max(1, min(int(request.args.get('limit', '50')), 200))
    except ValueError:
        return 50


@administration_bp.route('/administration/servers')
def servers_page():
    ctx = common_context('servers')
    ctx['ace_admin'] = {'section': 'servers', 'data': ace_data_service.get_server_data()}
    return render_template('index.html', **ctx)


@administration_bp.route('/administration/accounts')
def accounts_page():
    search = request.args.get('q', '').strip()
    ctx = common_context('accounts')
    ctx['ace_admin'] = {'section': 'accounts', 'data': ace_data_service.get_accounts(limit=_limit(), search=search)}
    return render_template('index.html', **ctx)


@administration_bp.route('/administration/characters')
def characters_page():
    search = request.args.get('q', '').strip()
    ctx = common_context('characters')
    ctx['ace_admin'] = {'section': 'characters', 'data': ace_data_service.get_characters(limit=_limit(), search=search)}
    return render_template('index.html', **ctx)


@administration_bp.route('/administration/world')
def world_page():
    ctx = common_context('world')
    ctx['ace_admin'] = {'section': 'world', 'data': ace_data_service.get_world()}
    return render_template('index.html', **ctx)


@administration_bp.route('/administration/database')
def database_page():
    ctx = common_context('database')
    ctx['ace_admin'] = {'section': 'database', 'data': ace_data_service.get_schema_inventory()}
    return render_template('index.html', **ctx)


@administration_bp.route('/api/administration/ace-data')
def ace_data_api():
    return jsonify(ace_data_service.get_overview())
