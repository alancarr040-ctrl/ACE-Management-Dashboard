from flask import Blueprint, redirect, render_template, request, url_for
from routes.context import common_context, management_service, event_service

management_bp = Blueprint('management', __name__)


@management_bp.route('/management')
def management_page():
    ctx = common_context('management')
    ctx['management'] = management_service.get_status()
    return render_template('index.html', **ctx)


@management_bp.route('/management/run', methods=['POST'])
def management_run():
    action_id = request.form.get('action_id', '').strip()
    dry_run = request.form.get('dry_run') == '1'
    result = management_service.run_action(action_id, dry_run=dry_run)
    event_service.record_management_result(result)
    message = {
        'type': 'success' if result.get('success') else 'error',
        'title': result.get('label', 'Management Action'),
        'text': f"{result.get('command')} exited with code {result.get('exit_code')}.",
        'result': result,
    }
    ctx = common_context('management', message=message)
    ctx['management'] = management_service.get_status()
    return render_template('index.html', **ctx)
