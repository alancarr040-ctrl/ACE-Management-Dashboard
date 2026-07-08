from __future__ import annotations

from flask import Blueprint, jsonify, render_template, request
from routes.context import common_context, event_service, project_service

events_bp = Blueprint('events', __name__)


@events_bp.route('/events')
def events_page():
    severity = request.args.get('severity', '').strip() or None
    source = request.args.get('source', '').strip() or None
    limit = request.args.get('limit', '50').strip()
    try:
        limit_int = max(10, min(int(limit), 200))
    except ValueError:
        limit_int = 50
    ctx = common_context('events')
    ctx['events'] = event_service.get_recent_events(limit=limit_int, severity=severity, source=source)
    ctx['event_summary'] = event_service.get_summary()
    ctx['event_filters'] = {'severity': severity or '', 'source': source or '', 'limit': limit_int}
    return render_template('index.html', **ctx)


@events_bp.route('/api/events')
def events_api():
    severity = request.args.get('severity', '').strip() or None
    source = request.args.get('source', '').strip() or None
    limit = request.args.get('limit', '50').strip()
    try:
        limit_int = max(1, min(int(limit), 200))
    except ValueError:
        limit_int = 50
    return jsonify({
        'summary': event_service.get_summary(),
        'events': event_service.get_recent_events(limit=limit_int, severity=severity, source=source),
    })
