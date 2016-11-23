import os
import uuid


def _envvar_or_default(key, default_value):
    result = os.environ.get(key)
    if not result:
        result = default_value
    return result


class flask (object):
    secret_key = _envvar_or_default('FLASK_SECRET_KEY', str(uuid.uuid4()))


class google(object):
    class oauth(object):
        client_id = _envvar_or_default('GOOGLE_OAUTH_CLIENT_ID', "410739525249-8e3sh05b5iefqkqijcp4c0mobddmph83.apps.googleusercontent.com")
        client_secret = _envvar_or_default('GOOGLE_OAUTH_CLIENT_SECRET', "kqyH-iHTfUFQYVMNjbYpXzeJ")
    class sheet(object):
        id = _envvar_or_default('GOOGLE_SHEET_ID', '1s_EC5hn-A-yKFUYWKO3RZ768AVW9FL-DKNZ3QBb0tls')
        range_name = _envvar_or_default('GOOGLE_SHEET_RANGE_NAME', 'Job Opportunities')
