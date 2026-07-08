from __future__ import annotations

from flask import Blueprint, jsonify, redirect, render_template, request, url_for
from routes.context import automation_service, common_context, event_service

automation_bp = Blueprint('automation', __name__)


@automation_bp.route('/automation')
def automation_page():
    ctx = common_context('automation')
    ctx['automation'] = automation_service.get_status(run_due=True)
    ctx['event_summary'] = event_service.get_summary()
    ctx['recent_events'] = event_service.get_recent_events(limit=5, source='automation')
    return render_template('index.html', **ctx)


@automation_bp.route('/api/automation')
def automation_api():
    return jsonify(automation_service.get_status(run_due=True))


@automation_bp.route('/automation/run', methods=['POST'])
def automation_run():
    job_id = request.form.get('job_id', '').strip()
    automation_service.run_job(job_id, manual=True)
    return redirect(url_for('automation.automation_page') + '#automation')
