import json

from flask import render_template, Blueprint, request, current_app, flash
from flask_login import login_required
from flask.helpers import get_env

from odpapi import ODPAPIClient, ODPAPIError
from .hydra import get_access_token

bp = Blueprint('portal', __name__)


def init_app(app):
    app.register_blueprint(bp)


@bp.route('/')
def index():
    return render_template('home.html')


@bp.route('/list', methods=('GET', 'POST'))
@login_required
def list_records():
    results = []
    if request.method == 'POST':
        institution_key = request.form['institution_key']
        odpapi_url = current_app.config['ODP_API_URL']
        ckanapi_key = current_app.config['CKAN_API_KEY']
        access_token = ckanapi_key or get_access_token()
        read_timeout = None if get_env() == 'development' else 10
        try:
            with ODPAPIClient(odpapi_url, access_token, read_timeout=read_timeout) as odpapi_client:
                results = odpapi_client.get(f'/{institution_key}/metadata/')
                results = [json.dumps(result, indent=4) for result in results]
        except ODPAPIError as e:
            flash('{code} Error: {detail}'.format(code=e.status_code, detail=e.error_detail), category='error')

    return render_template('list.html', records=results)


@bp.route('/add', methods=('GET', 'POST'))
@login_required
def add_record():
    doi = None
    if request.method == 'POST':
        odpapi_url = current_app.config['ODP_API_URL']
        access_token = get_access_token()
        read_timeout = None if get_env() == 'development' else 10
        try:
            with ODPAPIClient(odpapi_url, access_token, read_timeout=read_timeout) as odpapi_client:
                result = odpapi_client.get('/doi/new')
                doi = result['doi']
        except ODPAPIError as e:
            flash('{code} Error: {detail}'.format(code=e.status_code, detail=e.error_detail), category='error')

    return render_template('add.html', doi=doi)
