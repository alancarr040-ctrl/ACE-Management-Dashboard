from __future__ import annotations

from flask import Blueprint, jsonify, redirect, render_template, request, url_for
from routes.context import common_context, notification_service

notifications_bp = Blueprint('notifications', __name__)


@notifications_bp.route('/notifications')
def notifications_page():
    ctx = common_context('notifications')
    ctx['notifications'] = notification_service.get_center(refresh=True)
    return render_template('index.html', **ctx)


@notifications_bp.route('/api/notifications')
def notifications_api():
    refresh = request.args.get('refresh', '1') != '0'
    return jsonify(notification_service.get_center(refresh=refresh))


@notifications_bp.post('/notifications/acknowledge')
def acknowledge_notification():
    notification_id = request.form.get('notification_id', '').strip()
    if notification_id:
        notification_service.acknowledge(notification_id)
    return redirect(url_for('notifications.notifications_page') + '#notifications')


@notifications_bp.post('/notifications/resolve')
def resolve_notification():
    notification_id = request.form.get('notification_id', '').strip()
    if notification_id:
        notification_service.resolve(notification_id)
    return redirect(url_for('notifications.notifications_page') + '#notifications')
