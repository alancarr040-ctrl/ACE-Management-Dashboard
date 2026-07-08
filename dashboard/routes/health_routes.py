from __future__ import annotations

from flask import Blueprint, jsonify, render_template
from routes.context import health_service, event_service, project_service

health_bp = Blueprint('health', __name__)


@health_bp.route('/health')
def health_page():
    health = health_service.get_health()
    event_service.observe_health(health)
    return render_template(
        'index.html',
        active_tab='health',
        project=project_service.get_info(),
        message=None,
        health=health,
        recent_events=event_service.get_recent_events(limit=5),
        event_summary=event_service.get_summary(),
    )


@health_bp.route('/api/health')
def health_api():
    health = health_service.get_health()
    event_service.observe_health(health)
    health['recent_events'] = event_service.get_recent_events(limit=10)
    health['event_summary'] = event_service.get_summary()
    return jsonify(health)
