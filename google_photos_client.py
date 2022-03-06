import pickle
from pathlib import Path
import os.path
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
import pandas as pd
from image import AlbumImage
import configurations

SCOPES = configurations.SCOPES
TOKEN_PATH = configurations.TOKEN_PATH
CREDENTIALS_PATH = configurations.CREDENTIALS_PATH


def get_creds():
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.

    if os.path.exists(TOKEN_PATH):
        with open(TOKEN_PATH, 'rb') as token:
            creds = pickle.load(token)
        with open(TOKEN_PATH, 'wb') as token:
            pickle.dump(creds, token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                CREDENTIALS_PATH, SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open(TOKEN_PATH, 'wb') as token:
            pickle.dump(creds, token)
    return creds

def google_photo_to_AlbumImage(google_photo):
    id_ = google_photo["id"]
    filename = google_photo["filename"]
    url = google_photo["productUrl"]
    metadata = google_photo["mediaMetadata"]
    return AlbumImage(id_, filename, url, metadata)

def scan_galery(google_photos):
    items = []
    nextpagetoken = None
    # The default number of media items to return at a time is 25. The maximum pageSize is 100.
    while nextpagetoken != '':
        print(f"Number of items processed:{len(items)}", end='\r')
        results = google_photos.mediaItems().list(pageSize=100, pageToken=nextpagetoken).execute()
        items += results.get('mediaItems', [])
        nextpagetoken = results.get('nextPageToken', '')
    images = [google_photo_to_AlbumImage(i) for i in items]
    return images

def main():
    creds = get_creds()
    google_photos = build('photoslibrary', 'v1', credentials=creds, static_discovery=False)
    images = scan_galery(google_photos)
    print(len(images))
    for i in images:
        print(i)

if __name__ == "__main__":
    main()

# class GooglePhotosClient:
#     def __init__(self):
#         scopes = ['https://www.googleapis.com/auth/photoslibrary.readonly']
#         token_file = Path(r'credentials\token.pickle')
#         credentials_file = Path(r'credentials\credentials.json')
#         self.credentials = {'scopes': scopes,
#                             'token_file': token_file,
#                             'credentials_file': credentials_file}
#
#     @property
#     def credentials(self):
#         return self._credentials
#
#     @credentials.setter
#     def credentials(self, args):
#         credentials = None
#         if args["token_file"].exists():
#             with open(args["token_file"], 'rb') as token:
#                 credentials = pickle.load(token)
#
#         if not credentials or not credentials.valid:
#             if credentials and credentials.expired and credentials.refresh_token:
#                 credentials.refresh(Request())
#             else:
#                 flow = InstalledAppFlow.from_client_secrets_file(args["credentials_file"], args["scopes"])
#                 credentials = flow.run_local_server(port=0)
#             with open(args["token_file"], 'wb') as token:
#                 pickle.dump(credentials, token)
#         self._credentials = credentials
#
#     def google_photos_resource(self):
#         google_photos = build('photoslibrary', 'v1', credentials=self.credentials, static_discovery=False)



