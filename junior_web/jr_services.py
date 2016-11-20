from flask import Flask, url_for, json, make_response, request, session, redirect, abort
from flask_cors import CORS
from google_authorization import *
from google_sheets import get_sheet_values
from opportunity_parsing import parse_opportunities, get_opportunities_criteria
from opportunity_filtering import filter_opportunities
import uuid
import os
import jsonschema
import werkzeug.exceptions


SESSION_CREDENTIALS_KEY = "credentials"


def envvar_or_default(key, default_value):
    result = os.environ.get(key)
    if not result:
        result = default_value
    return result


def get_session_value(key):
    try:
        return session[key]
    except Exception as e:
        raise Exception("Session not initialized.", e)


def get_opportunities_sheet():
    return get_sheet_values(
        envvar_or_default('JUNIOR_SHEET_ID', '1s_EC5hn-A-yKFUYWKO3RZ768AVW9FL-DKNZ3QBb0tls'),
        envvar_or_default('JUNIOR_RANGE_NAME', 'Job Opportunities'),
        get_session_value(SESSION_CREDENTIALS_KEY))


def get_all_opportunities():
    return parse_opportunities(get_opportunities_sheet())


def make_json_response_success(data, request_body, request_method, request_url):
    result = make_response(json.dumps({
        "data": data,
        "request": {
            "body": request_body,
            "method": request_method,
            "url": request_url
        },
        "exception": None
    }))
    result.headers['Content-Type'] = 'application/json'
    return result


def make_json_response_failure(status, exception, request_body, request_method, request_url):
    result = make_response(json.dumps({
        "data": None,
        "request": {
            "body": request_body,
            "method": request_method,
            "url": request_url
        },
        "exception": exception
    }), status)
    result.headers['Content-Type'] = 'application/json'
    return result


def load_schema(schema_filename):
    jr_services_path = os.path.realpath(os.path.dirname(__file__))
    full_schema_filename = os.path.join(jr_services_path, "schema", schema_filename)
    with open(full_schema_filename) as schema_file:
        return json.load(schema_file)


def format_json_path(path_elements):
    return "/" + "/".join(map(lambda o: str(o), path_elements))


def try_get_valid_request_json(request, schema_path):
    schema = load_schema(schema_path)
    try:
        result = request.json
        jsonschema.validate(result, schema)
        return result, None
    except werkzeug.exceptions.BadRequest as e:
        return None, make_json_response_failure(
            400,
            { "message": "JSON parsing failed." },
            request.data,
            "POST",
            url_for('api_opportunities_search'))
    except jsonschema.ValidationError as e:
        return None, make_json_response_failure(
            400,
            { "message": "JSON validation failed at {}: {}".format(format_json_path(e.path), e.message) },
            request.data,
            "POST",
            url_for('api_opportunities_search'))


app = Flask(__name__)
app.secret_key = envvar_or_default('FLASK_SECRET_KEY', str(uuid.uuid4()))
CORS(app)


def auth_is_ready():
    return (SESSION_CREDENTIALS_KEY in session
        and credentials_are_current(session[SESSION_CREDENTIALS_KEY]))


@app.route('/', methods=['GET'])
def root():
    if not auth_is_ready():
        return redirect(url_for('login'))
    else:
        return redirect('static/index.html')


@app.route('/login', methods=['GET'])
def login():
    context = build_auth_context_raw(
        envvar_or_default('GOOGLE_CLIENT_ID', "410739525249-8e3sh05b5iefqkqijcp4c0mobddmph83.apps.googleusercontent.com"),
        envvar_or_default('GOOGLE_CLIENT_SECRET', "kqyH-iHTfUFQYVMNjbYpXzeJ"),
        "https://www.googleapis.com/auth/spreadsheets.readonly",
        url_for('login', _external=True),
        "Project Return JR Web Layer")

    if 'code' not in request.args:
        return redirect(build_auth_uri(context))
    else:
        auth_code = request.args.get('code')
        credentials = process_auth_response(context, auth_code)
        session[SESSION_CREDENTIALS_KEY] = credentials
        return redirect(url_for('root'))


def require_auth():
    if not auth_is_ready():
        abort(401)


@app.route('/opportunities', methods=['GET'])
def api_opportunities():
    require_auth()
    return make_json_response_success(
        list(get_all_opportunities()),
        None,
        "GET",
        url_for('api_opportunities'))


@app.route('/opportunities/search', methods=['POST'])
# E.g.,  {"convictions":[{"type":"Sex","year":2004}],"partTimeOnly":False,"hasDriversLicense":True,
# "industries":["Building Construction/Skilled Trade"],"abilities":['Standing for 8hrs',
# '_Heavy Lifting', 'capable with tools and machinery', 'Attention to Detail']}
def api_opportunities_search():
    require_auth()
    request_json, json_error_response = (
        try_get_valid_request_json(request, "opportunity/search.schema.json"))
    return (json_error_response or
        make_json_response_success(
            list(filter_opportunities(request_json, get_all_opportunities())),
            request.data,
            "POST",
            url_for('api_opportunities_search')))


@app.route('/opportunities/criteria', methods=['GET'])
def api_opportunities_criteria():
    require_auth()
    return make_json_response_success(
        get_opportunities_criteria(get_opportunities_sheet()),
        None,
        "GET",
        url_for('api_opportunities_criteria'))


@app.after_request
def disable_caching(response):
    response.headers['Cache-Control'] = 'public, max-age=0'
    response.headers['Pragma'] = 'no-cache'
    return response


if __name__ == '__main__':
    app.run(host="0.0.0.0", port="80")
