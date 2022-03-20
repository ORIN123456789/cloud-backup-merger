from dash import html, dcc
import plotly.express as px
import pandas as pd
from threading import Timer
from runners.basic_dashboard import BasicDashboard
from google_photos_client import GooglePhotosClient
from configurations import DASHBOARD, ACCOUNTS


class AlbumsDashboard(BasicDashboard):
    def __init__(self):
        super().__init__()
        self.duplicated_photos = self._find_duplicated_photos()

    def refresh_data(self):
        self.duplicated_photos = self._find_duplicated_photos()

    def _find_duplicated_photos(self):
        google_photos_client = GooglePhotosClient(ACCOUNTS[0])
        return google_photos_client.duplicates_between_albums()

    def serve_layout(self):
        self.refresh_data()
        if len(self.duplicated_photos) == 0:
            _html = html.Div(children=[html.Img(src=DASHBOARD["logo"], id='logo'),
                             html.H3('There are no duplicated photos in you account', className='text')])
        else:
            photo_list = self.images_list_to_html_object(self.duplicated_photos.values())
            _html = html.Div(children=[html.Img(src=DASHBOARD["logo"], id='logo'),
                                       dcc.Graph(id='occurrences-graph',
                                                 figure=self._figure()),
                                       html.H4('The following images appear multiple times in your albums:',
                                               className='text'),
                                       html.Div([photo_list], className='table'),
                                       ]
                             )
        return _html

    def _figure(self):
        return px.bar(self._dataframe(), x="Photo", y="Occurrences")

    def _dataframe(self):
        photos_hash = self.duplicated_photos.keys()
        occurrences = [len(self.duplicated_photos[photo_hash]) for photo_hash in photos_hash]
        df = pd.DataFrame({"Photo": photos_hash,
                           "Occurrences": occurrences})
        return df

    def photo_li(self, album_images):
        base_url = next(iter(album_images)).base_url
        link_li = lambda img: html.Li(html.A("Album " + img.album_title,
                                             className='album',
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
