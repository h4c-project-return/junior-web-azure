from flask import Flask, url_for, json, make_response, request, session, redirect, abort
from flask_cors import CORS
from google_authorization import *
from google_sheets import get_sheet_values
from opportunity_parsing import parse_opportunities, get_opportunities_criteria
from opportunity_filtering import filter_opportunities
import uuid
import os


SESSION_CREDENTIALS_KEY = "credentials"


def get_session_value(key):
    try:
        return session[key]
    except Exception as e:
        raise Exception("Session not initialized.", e)


def get_opportunities_sheet():
    sheet_id = os.environ.get('JUNIOR_SHEET_ID')
    if not sheet_id:
        sheet_id = '1s_EC5hn-A-yKFUYWKO3RZ768AVW9FL-DKNZ3QBb0tls'

    range_name = os.environ.get('JUNIOR_RANGE_NAME')
    if not range_name:
        range_name = 'Job Opportunities'

    return get_sheet_values(
        sheet_id,
        range_name,
        get_session_value(SESSION_CREDENTIALS_KEY))


def get_all_opportunities():
    return parse_opportunities(get_opportunities_sheet())


def build_json_response_success(data, request_body, request_method, request_url):
    return json.dumps({
        "data": data,
        "request": {
            "body": request_body,
            "method": request_method,
            "url": request_url
        },
        "exception": None
    })


def build_json_response_failure(exception, request_body, request_method, request_url):
    return json.dumps({
        "data": None,
        "request": {
            "body": request_body,
            "method": request_method,
            "url": request_url
        },
        "exception": exception
    })


app = Flask(__name__)
app.secret_key = str(uuid.uuid4())
CORS(app)


def auth_is_ready():
    return (SESSION_CREDENTIALS_KEY in session
        and credentials_are_current(session[SESSION_CREDENTIALS_KEY]))


@app.route('/', methods=['GET'])
def root():
    if not auth_is_ready():
        return redirect(url_for('login'))
    else:
        return "Authenticated!"


@app.route('/login', methods=['GET'])
def login():
    context = build_auth_context(
        "junior_web/client_secret.json",
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
    resp = make_response(build_json_response_success(
        list(get_all_opportunities()),
        None,
        "GET",
        url_for('api_opportunities')))
    resp.headers['Content-Type'] = 'application/json'
    return resp


@app.route('/opportunities/search', methods=['POST'])
# E.g.,  {"convictions":[{"type":"Sex","year":2004}],"partTimeOnly":False,"hasDriversLicense":True,
# "industries":["Building Construction/Skilled Trade"],"abilities":['Standing for 8hrs',
# '_Heavy Lifting', 'capable with tools and machinery', 'Attention to Detail']}
def api_opportunities_search():
    require_auth()
    resp = make_response(build_json_response_success(
        list(filter_opportunities(request.json, get_all_opportunities())),
        request.data,
        "POST",
        url_for('api_opportunities_search')))
    resp.headers['Content-Type'] = 'application/json'
    return resp


@app.route('/opportunities/criteria', methods=['GET'])
def api_opportunities_criteria():
    require_auth()
    resp = make_response(build_json_response_success(
        get_opportunities_criteria(get_opportunities_sheet()),
        None,
        "GET",
        url_for('api_opportunities_criteria')))
    resp.headers['Content-Type'] = 'application/json'
    return resp


if __name__ == '__main__':
    app.run(host="0.0.0.0", port="80")
