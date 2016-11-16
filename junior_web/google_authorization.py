from oauth2client import client
from apiclient import discovery
import httplib2


def build_auth_context(client_secret_filename, scope_uri, redirect_uri, user_agent):
    flow = client.flow_from_clientsecrets(
        client_secret_filename,
        scope = scope_uri,
        redirect_uri = redirect_uri)
    flow.user_agent = user_agent
    return flow


def build_auth_uri(context):
    return context.step1_get_authorize_url()


def process_auth_response(context, auth_code):
    return context.step2_exchange(auth_code).to_json()


def credentials_are_current(credentials_json):
    try:
        credentials = client.OAuth2Credentials.from_json(credentials_json)
    except Exception as e:
        raise Exception("Invalid credentials.", e)
    return not credentials.access_token_expired
