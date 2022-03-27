from dash import html
from concurrent.futures import ThreadPoolExecutor, as_completed

import configurations
from calculate_duplications import duplicates_between_accounts
from runners.basic_dashboard import BasicDashboard
from google_photos_client import GooglePhotosClient
from configurations import DASHBOARD


class AccountsDashboard(BasicDashboard):

    def __init__(self):
        self.google_photos_clients = self.get_google_photos_clients()
        super().__init__()
        self.duplicated_photos = None
        self.accounts_counter = dict()

    def refresh_data(self):
        self.duplicated_photos = self._find_duplicated_photos()

    def get_google_photos_clients(self):
        create_clients_processes = []
        _google_photos_clients = []
        with ThreadPoolExecutor(max_workers=None) as executor:
            for account in configurations.ACCOUNTS:
                create_clients_processes.append(executor.submit(GooglePhotosClient, account))
            for _ in as_completed(create_clients_processes):
                _google_photos_clients.append(_.result())
        return _google_photos_clients

    def _find_duplicated_photos(self):
        #return duplicates_between_accounts(_google_photos_clients)
        return duplicates_between_accounts(self.get_google_photos_clients())
        #return duplicates_between_accounts(self.google_photos_clients) -  todo : check why this command doesnt work

    def serve_layout(self):
        self.refresh_data()
        if len(self.duplicated_photos) == 0:
            _html = html.Div(children=[html.Img(src=DASHBOARD["logo"], id='logo'),
                                       html.Img(src=DASHBOARD["no_duplicates"], id='message')])
        else:
            photo_list = self.images_list_to_html_object(self.duplicated_photos.values())
            _html = html.Div(children=[html.Img(src=DASHBOARD["logo"], id='logo'),
                                       html.Img(src=DASHBOARD["instruction"], id='instruction'),
                                       html.Img(src=DASHBOARD["account_text"], id='message'),
                                       html.Div([photo_list], className='table'),
                                       ])
        return _html

    def get_account_counter(self, account_name):
        counter = self.accounts_counter.get(account_name, 0) + 1
        self.accounts_counter[account_name] = counter
        str_counter = str(counter) if counter > 1 else ""
        return account_name + " " + str_counter


    def photo_li(self, album_images):
        self.accounts_counter.clear()
        base_url = next(iter(album_images)).base_url
        link_li = lambda img: html.A(self.get_account_counter(img.account_name),
                                             className='account',
                                             href=img.url,
                                             target="_blank")
        links = html.Div(children=[link_li(img) for img in album_images], className="links")

        li = html.Li(children=[html.Img(src=base_url,
                                        className='image'),
                               links],
                     className='photo_li')
        return li

    def images_list_to_html_object(self, photos):
        photo_list = html.Ul(className='duplicated_photos',
                             children=[self.photo_li(image) for image in photos])
        return photo_list
