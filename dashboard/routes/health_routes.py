from __future__ import annotations

from flask import Blueprint, jsonify, render_template
from routes.context import common_context, health_service, event_service

health_bp = Blueprint('health', __name__)


@health_bp.route('/health')
def health_page():
    health = health_service.get_health()
    event_service.observe_health(health)
    ctx = common_context('health')
    ctx['health'] = health
    ctx['recent_events'] = event_service.get_recent_events(limit=5)
    ctx['event_summary'] = event_service.get_summary()
    return render_template('index.html', **ctx)


@health_bp.route('/api/health')
def health_api():
    health = health_service.get_health()
    event_service.observe_health(health)
    health['recent_events'] = event_service.get_recent_events(limit=10)
    health['event_summary'] = event_service.get_summary()
    return jsonify(health)
