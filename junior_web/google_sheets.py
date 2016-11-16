import httplib2
from apiclient import discovery
from oauth2client import client


def get_sheets_auth_scope():
    return 'https://www.googleapis.com/auth/spreadsheets.readonly'


## https://developers.google.com/sheets/samples/reading
def get_sheet_values(spreadsheetId, rangeName, credentials_json):
    http = client.OAuth2Credentials.from_json(credentials_json).authorize(httplib2.Http())
    discoveryUrl = ('https://sheets.googleapis.com/$discovery/rest?'
                   'version=v4')
    service = discovery.build('sheets', 'v4', http=http,
                             discoveryServiceUrl=discoveryUrl)

    result = service.spreadsheets().values().get(
        spreadsheetId=spreadsheetId, range=rangeName).execute()
    return result.get('values', [])
