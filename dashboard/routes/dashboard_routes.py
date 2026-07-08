from flask import Blueprint, render_template
from routes.context import common_context

dashboard_bp = Blueprint('dashboard', __name__)

@dashboard_bp.route('/')
def index():
    return render_template('index.html', **common_context('dashboard'))
