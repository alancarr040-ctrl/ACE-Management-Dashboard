from flask import Flask

from routes.about_routes import about_bp
from routes.backup_routes import backup_bp
from routes.dashboard_routes import dashboard_bp
from routes.docker_routes import docker_bp
from routes.log_routes import logs_bp
from routes.management_routes import management_bp
from routes.health_routes import health_bp
from routes.event_routes import events_bp
from routes.automation_routes import automation_bp
from routes.metrics_routes import metrics_bp
from routes.notification_routes import notifications_bp


def create_app() -> Flask:
    app = Flask(__name__)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(docker_bp)
    app.register_blueprint(backup_bp)
    app.register_blueprint(logs_bp)
    app.register_blueprint(management_bp)
    app.register_blueprint(health_bp)
    app.register_blueprint(events_bp)
    app.register_blueprint(automation_bp)
    app.register_blueprint(metrics_bp)
    app.register_blueprint(notifications_bp)
    app.register_blueprint(about_bp)
    return app


app = create_app()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
