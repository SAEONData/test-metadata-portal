from flask import render_template, Blueprint
from flask_login import login_required

bp = Blueprint('portal', __name__)


def init_app(app):
    app.register_blueprint(bp)


@bp.route('/')
def index():
    return render_template('home.html')


@bp.route('/list')
@login_required
def search():
    return render_template('search.html')


@bp.route('/create')
@login_required
def create():
    return render_template('create.html')
