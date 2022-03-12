import pickle
import urllib.request
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from PIL import Image
# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/photoslibrary.readonly']

creds = None
# The file token.pickle stores the user's access and refresh tokens, and is
# created automatically when the authorization flow completes for the first
# time.

if os.path.exists('token.pickle'):
    with open('credentials/token.pickle', 'rb') as token:
        creds = pickle.load(token)
        print(type(creds))
# If there are no (valid) credentials available, let the user log in.
if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
    else:
        flow = InstalledAppFlow.from_client_secrets_file(
            'credentials/credentials.json', SCOPES)
        creds = flow.run_local_server(port=0)
    # Save the credentials for the next run
    with open('token.pickle', 'wb') as token:
        pickle.dump(creds, token)


google_photos = build('photoslibrary', 'v1', credentials=creds, static_discovery=False)


items = []
nextpagetoken = None
# The default number of media items to return at a time is 25. The maximum pageSize is 100.
while nextpagetoken != '':
    print(f"Number of items processed:{len(items)}", end='\r')
    results = google_photos.mediaItems().list(pageSize=100, pageToken=nextpagetoken).execute()
    items += results.get('mediaItems', [])
    nextpagetoken = results.get('nextPageToken', '')

print(type(items[0]))
import pandas as pd

# Convert the list of dict into a dataframe.
df = pd.DataFrame(items)

# Taking the column mediaMetadata and splitting it into individual columns
dfmeta = df.mediaMetadata.apply(pd.Series)

# Combining all the different columns into one final dataframe
photos = pd.concat(
    [
        df.drop('mediaMetadata', axis=1),
        dfmeta.drop('photo', axis=1),
        dfmeta.photo.apply(pd.Series, dtype=object)
    ], axis=1
)

# Convert the creation time to a datetime dtype
photos.creationTime = pd.to_datetime(photos.creationTime)

# Convert other numeric data into numeric dtypes
#for c in ['width', 'height']:
#    photos[c] = pd.to_numeric(photos[c])

#photos.to_hdf('google_photo_data.hdf', key='photos')

print(photos.mimeType.value_counts())
print(photos.loc[0]["baseUrl"])

