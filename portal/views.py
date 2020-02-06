import json

from flask import render_template, Blueprint, request, current_app, flash, abort
from flask_login import login_required
from flask.helpers import get_env
import requests

from .hydra import get_access_token
from .forms import MetadataRecordForm

bp = Blueprint('portal', __name__)


def init_app(app):
    app.register_blueprint(bp)


@bp.route('/')
def index():
    return render_template('home.html')


@bp.route('/institutions/')
@login_required
def list_institutions():
    results = _accountsapi_request('GET', '/institution/')
    return render_template('institutions.html', institutions=results or [])


@bp.route('/<institution_key>/list_records')
@login_required
def list_records(institution_key: str):
    results = _odpapi_request('GET', f'/{institution_key}/metadata/')
    return render_template('list_records.html', institution_key=institution_key, records=results or [])


@bp.route('/<institution_key>/view_record/<record_id>')
@login_required
def view_record(institution_key: str, record_id: str):
    result = _odpapi_request('GET', f'/{institution_key}/metadata/{record_id}')
    if result:
        result = json.dumps(result, indent=4)
    return render_template('view_record.html', institution_key=institution_key, record=result)


@bp.route('/<institution_key>/add_record', methods=('GET', 'POST'))
@login_required
def add_record(institution_key: str):
    result = None
    form = MetadataRecordForm()
    if request.method == 'POST':
        if form.validate():
            result = _odpapi_request('POST', f'/{institution_key}/metadata/', json={
                'collection_key': form.collection_key.data,
                'schema_key': form.schema_key.data,
                'metadata': json.loads(form.metadata.data),
                'doi': form.doi.data,
                'auto_assign_doi': form.auto_assign_doi.data,
            })
            if result:
                result = json.dumps(result, indent=4)

    return render_template('edit_record.html', institution_key=institution_key, record=result, form=form, new=True)


@bp.route('/<institution_key>/edit_record/<record_id>', methods=('GET', 'POST'))
@login_required
def edit_record(institution_key: str, record_id: str):
    result = None
    if request.method == 'GET':
        record = _odpapi_request('GET', f'/{institution_key}/metadata/{record_id}')
        if not record:
            abort(404)
        record['metadata'] = json.dumps(record['metadata'], indent=4)
        form = MetadataRecordForm(**record)
    else:
        form = MetadataRecordForm()
        if form.validate():
            result = _odpapi_request('PUT', f'/{institution_key}/metadata/{record_id}', json={
                'collection_key': form.collection_key.data,
                'schema_key': form.schema_key.data,
                'metadata': json.loads(form.metadata.data),
                'doi': form.doi.data,
                'auto_assign_doi': form.auto_assign_doi.data,
            })
            if result:
                result = json.dumps(result, indent=4)

    return render_template('edit_record.html', institution_key=institution_key, record=result, form=form, new=False)


def _odpapi_request(method, endpoint, **kwargs):
    return _request(current_app.config['ODP_API_URL'], 'ODP API', method, endpoint, **kwargs)


def _accountsapi_request(method, endpoint, **kwargs):
    return _request(current_app.config['ACCOUNTS_API_URL'], 'Accounts API', method, endpoint, **kwargs)


def _request(api_url, api_name, method, endpoint, **kwargs):
    ckanapi_key = current_app.config['CKAN_API_KEY']
    access_token = ckanapi_key or get_access_token()
    verify_tls = get_env() != 'development'
    timeout = None if get_env() == 'development' else 10
    headers = {
        'Accept': 'application/json',
        'Authorization': 'Bearer ' + access_token,
    }
    if method in ('POST', 'PUT'):
        headers['Content-Type'] = 'application/json'
    headers.update(kwargs.pop('headers', {}))
    try:
        r = requests.request(method, api_url + endpoint, **kwargs,
                             headers=headers,
                             verify=verify_tls,
                             timeout=timeout,
                             )
        r.raise_for_status()
        return r.json()

    except requests.HTTPError as e:
        try:
            detail = e.response.json()
        except ValueError:
            detail = e.response.reason
        flash(f"{e.response.status_code} error from {api_name}: {detail}", category='error')

    except requests.RequestException as e:
        flash(f"Error sending request to {api_name}: {e}", category='error')
