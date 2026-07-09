from __future__ import annotations

from flask import Blueprint, render_template
from routes.context import common_context, workspace_service

workspace_bp = Blueprint('workspace', __name__)


@workspace_bp.route('/operations')
def operations_page():
    ctx = common_context('operations')
    ctx['workspace'] = workspace_service.get_workspace('operations')
    return render_template('index.html', **ctx)


@workspace_bp.route('/monitoring')
def monitoring_page():
    ctx = common_context('monitoring')
    ctx['workspace'] = workspace_service.get_workspace('monitoring')
    return render_template('index.html', **ctx)


@workspace_bp.route('/administration')
def administration_page():
    ctx = common_context('administration')
    ctx['workspace'] = workspace_service.get_workspace('administration')
    return render_template('index.html', **ctx)


@workspace_bp.route('/tools')
def tools_page():
    ctx = common_context('tools')
    ctx['workspace'] = workspace_service.get_workspace('tools')
    return render_template('index.html', **ctx)
