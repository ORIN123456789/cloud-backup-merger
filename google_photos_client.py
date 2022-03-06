import pickle
from pathlib import Path
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build


class GooglePhotosClient:
    def __init__(self):
        scopes = ['https://www.googleapis.com/auth/photoslibrary.readonly']
        token_file = Path(r'credentials\token.pickle')
        credentials_file = Path(r'credentials\credentials.json')
        self.credentials = {'scopes': scopes,
                            'token_file': token_file,
                            'credentials_file': credentials_file}

    @property
    def credentials(self):
        return self._credentials

    @credentials.setter
    def credentials(self, args):
        credentials = None
        if args["token_file"].exists():
            with open(args["token_file"], 'rb') as token:
                credentials = pickle.load(token)

        if not credentials or not credentials.valid:
            if credentials and credentials.expired and credentials.refresh_token:
                credentials.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(args["credentials_file"], args["scopes"])
                credentials = flow.run_local_server(port=0)
            with open(args["token_file"], 'wb') as token:
                pickle.dump(credentials, token)
        self._credentials = credentials

    def google_photos_resource(self):
        google_photos = build('photoslibrary', 'v1', credentials=self.credentials, static_discovery=False)

    def scan():
        pass

