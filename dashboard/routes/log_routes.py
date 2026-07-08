from flask import Blueprint, render_template, request
from routes.context import ace_log_service, common_context

logs_bp = Blueprint('logs', __name__)

@logs_bp.route('/logs')
def logs_page():
    source = request.args.get('source', 'ace-server')
    try:
        lines = int(request.args.get('lines', 150))
    except ValueError:
        lines = 150
    severity = request.args.get('severity', 'all')
    search = request.args.get('search', '')

    ctx = common_context('logs')
    ctx['log_view'] = ace_log_service.get_view(source, lines=lines, severity=severity, search=search)
    return render_template('index.html', **ctx)
