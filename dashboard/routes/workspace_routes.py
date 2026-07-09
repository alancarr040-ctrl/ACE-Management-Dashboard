from __future__ import annotations

from flask import Blueprint, render_template, request
from routes.context import common_context, workspace_service
from services.ace_data_service import ACEDataService

workspace_bp = Blueprint('workspace', __name__)
ace_data_service = ACEDataService()


def _workspace_context(active_tab: str):
    ctx = common_context(active_tab)
    ctx['workspace'] = workspace_service.get_workspace(workspace_service.get_workspace_for_tab(active_tab))
    return ctx


@workspace_bp.route('/operations')
def operations_page():
    return render_template('index.html', **_workspace_context('operations'))


@workspace_bp.route('/monitoring')
def monitoring_page():
    return render_template('index.html', **_workspace_context('monitoring'))


@workspace_bp.route('/administration')
def administration_page():
    ctx = _workspace_context('administration')
    return render_template('index.html', **ctx)


@workspace_bp.route('/administration/servers')
def administration_servers_page():
    ctx = _workspace_context('servers')
    ctx['ace_overview'] = ace_data_service.get_overview()
    return render_template('index.html', **ctx)


@workspace_bp.route('/administration/accounts')
def administration_accounts_page():
    search_query = request.args.get('q', '').strip()
    status = request.args.get('status', 'all').strip() or 'all'
    access = request.args.get('access', 'all').strip() or 'all'
    sort = request.args.get('sort', 'accountName').strip() or 'accountName'
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 25, type=int)
    ctx = _workspace_context('accounts')
    ctx['search_query'] = search_query
    ctx['account_data'] = ace_data_service.get_accounts(
        search=search_query,
        status=status,
        access=access,
        sort=sort,
        page=page,
        per_page=per_page,
    )
    return render_template('index.html', **ctx)


@workspace_bp.route('/administration/accounts/<int:account_id>')
def administration_account_detail_page(account_id: int):
    ctx = _workspace_context('account_detail')
    ctx['account_detail'] = ace_data_service.get_account_detail(account_id)
    return render_template('index.html', **ctx)


@workspace_bp.route('/administration/characters')
def administration_characters_page():
    search_query = request.args.get('q', '').strip()
    ctx = _workspace_context('characters')
    ctx['search_query'] = search_query
    ctx['character_data'] = ace_data_service.get_characters(search_query)
    return render_template('index.html', **ctx)


@workspace_bp.route('/administration/characters/<int:character_id>')
def administration_character_detail_page(character_id: int):
    ctx = _workspace_context('character_detail')
    ctx['character_detail'] = ace_data_service.get_character_detail(character_id)
    return render_template('index.html', **ctx)


@workspace_bp.route('/administration/relationships')
def administration_relationships_page():
    ctx = _workspace_context('relationships')
    ctx['relationship_data'] = ace_data_service.get_relationship_overview()
    return render_template('index.html', **ctx)


@workspace_bp.route('/administration/relationships/characters/<int:character_id>')
def administration_character_relationships_page(character_id: int):
    ctx = _workspace_context('character_relationships')
    ctx['character_relationships'] = ace_data_service.get_character_relationships(character_id)
    return render_template('index.html', **ctx)


@workspace_bp.route('/administration/world')
def administration_world_page():
    ctx = _workspace_context('world')
    ctx['world_data'] = ace_data_service.get_world_summary()
    return render_template('index.html', **ctx)


@workspace_bp.route('/administration/database')
def administration_database_page():
    ctx = _workspace_context('database')
    ctx['schema_inventory'] = ace_data_service.get_schema_inventory()
    return render_template('index.html', **ctx)


@workspace_bp.route('/administration/database/<database_key>/<table_name>')
def administration_table_detail_page(database_key: str, table_name: str):
    ctx = _workspace_context('database')
    ctx['schema_inventory'] = ace_data_service.get_schema_inventory()
    ctx['table_detail'] = ace_data_service.get_table_detail(database_key, table_name)
    return render_template('index.html', **ctx)


@workspace_bp.route('/tools')
def tools_page():
    return render_template('index.html', **_workspace_context('tools'))
