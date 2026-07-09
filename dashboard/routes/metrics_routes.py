from __future__ import annotations

from flask import Blueprint, jsonify, render_template
from routes.context import common_context, metrics_service, event_service

metrics_bp = Blueprint('metrics', __name__)


@metrics_bp.route('/metrics')
def metrics_page():
    ctx = common_context('metrics')
    ctx['metrics'] = metrics_service.get_metrics()
    ctx['recent_events'] = event_service.get_recent_events(limit=5)
    return render_template('index.html', **ctx)


@metrics_bp.route('/api/metrics')
def metrics_api():
    return jsonify(metrics_service.get_metrics())
