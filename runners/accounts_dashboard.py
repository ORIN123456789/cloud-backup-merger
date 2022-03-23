from dash import html, dcc
import plotly.express as px
import pandas as pd
import configurations
from runners.basic_dashboard import BasicDashboard
from google_photos_client import GooglePhotosClient
from configurations import DASHBOARD


class AccountsDashboard(BasicDashboard):

    def __init__(self):
        super().__init__()
        self.duplicated_photos = self._find_duplicated_photos()

    def refresh_data(self):
        self.duplicated_photos = self._find_duplicated_photos()

    def _find_duplicated_photos(self):
        google_photos_clients = [GooglePhotosClient(account) for account in configurations.ACCOUNTS]
        return GooglePhotosClient.duplicates_between_accounts(google_photos_clients)

    def serve_layout(self):
        self.refresh_data()
        if len(self.duplicated_photos) == 0:
            _html = html.Div(children=[html.Img(src=DASHBOARD["logo"], id='logo'),
                                       html.Img(src=DASHBOARD["no_duplicates"], className='message')])
        else:
            photo_list = self.images_list_to_html_object(self.duplicated_photos.values())
            _html = html.Div(children=[html.Img(src=DASHBOARD["logo"], id='logo'),
                                       html.Img(src=DASHBOARD["instruction"], id='instruction'),
                                       html.Img(src=DASHBOARD["account_text"], classname='message'),
                                       html.Div([photo_list], className='table'),
                                       ]
                             )
        return _html


    def photo_li(self, album_images):
        base_url = next(iter(album_images)).base_url
        link_li = lambda img: html.Li(html.A(img.account_name,
                                             className='account',
                                             href=img.url,
                                             target="_blank"),
                                      className='list')
        links = html.Ul(children=[link_li(img) for img in album_images])

        li = html.Li(children=[html.Img(src=base_url,
                                        className='image'),
                               links],
                     className='photo_li')
        return li

    def images_list_to_html_object(self, photos):
        photo_list = html.Ul(className='duplicated_photos',
                             children=[self.photo_li(image) for image in photos])
        return photo_list
