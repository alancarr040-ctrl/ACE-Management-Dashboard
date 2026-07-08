from flask import Blueprint, redirect, render_template, request, url_for
from routes.context import backup_service, common_context

backup_bp = Blueprint('backups', __name__)

@backup_bp.route('/backups')
def backups_page():
    message = None
    result = request.args.get('result')
    msg = request.args.get('message')
    detail = request.args.get('detail')
    if result and msg:
        message = {'type': result, 'text': msg, 'detail': detail}
    return render_template('index.html', **common_context('backups', message=message))

@backup_bp.post('/backups/create-runtime')
def create_runtime_backup():
    result = backup_service.create_runtime_backup()
    return redirect(url_for('backups.backups_page', result=('success' if result.ok else 'error'), message=result.message, detail=result.output) + '#backups')
