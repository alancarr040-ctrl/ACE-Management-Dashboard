from __future__ import annotations

from flask import Blueprint, jsonify, render_template
from routes.context import health_service, project_service

health_bp = Blueprint('health', __name__)


@health_bp.route('/health')
def health_page():
    return render_template(
        'index.html',
        active_tab='health',
        project=project_service.get_info(),
        message=None,
        health=health_service.get_health(),
    )


@health_bp.route('/api/health')
def health_api():
    return jsonify(health_service.get_health())
