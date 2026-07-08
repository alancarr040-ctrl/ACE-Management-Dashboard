from flask import Blueprint, render_template
from routes.context import common_context

about_bp = Blueprint('about', __name__)

@about_bp.route('/about')
def about_page():
    return render_template('index.html', **common_context('about'))
