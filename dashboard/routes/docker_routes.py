from flask import Blueprint, redirect, render_template, request, url_for
from routes.context import common_context, docker_service

docker_bp = Blueprint('docker', __name__)

@docker_bp.route('/docker')
def docker_page():
    return render_template('index.html', **common_context('docker'))

@docker_bp.route('/docker/logs/<name>')
def docker_logs(name):
    lines = int(request.args.get('lines', 100))
    ctx = common_context('docker')
    ctx['selected_container'] = name
    ctx['selected_logs'] = docker_service.get_container_logs(name, lines=lines)
    ctx['selected_log_lines'] = lines
    return render_template('index.html', **ctx)

@docker_bp.post('/docker/restart/<name>')
def docker_restart(name):
    ok, msg = docker_service.restart_container(name)
    return redirect(url_for('docker.docker_page', result=('success' if ok else 'error'), message=msg) + '#docker')
