from common_objects import Account, RunTypeEnum


RUN_TYPE = RunTypeEnum.ACCOUNTS

LOOK_FOR_ROTATIONS = False

SCOPES = ['https://www.googleapis.com/auth/photoslibrary.readonly']

ACCOUNTS = [Account(name="Alice's Cats", credentials='credentials/credentials1/credentials1.json'),
            Account(name="Alice's trips", credentials='credentials/credentials2/credentials2.json')]

DASHBOARD = {"app_name": "photos",
             "app_port": 8050,
             "logo": "assets/logo.png",
             "instruction": "assets/instruction.png",
             "account_text": "assets/account_text.png",
             "album_text": "assets/album_text.png",
             "no_duplicates": "assets/no_duplicates.png"}