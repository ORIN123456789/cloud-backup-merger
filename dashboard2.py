from dash import Dash, html, dcc
import plotly.express as px
import pandas as pd
import webbrowser
from threading import Timer

from google_photos_client import GooglePhotosClient
import configurations
import configurations2

from configurations2 import DASHBOARD
from image import AlbumImage


def duplicates(gp1, gp2):
    all_the_images = dict()
    duplicates = dict()
    it1 = gp1.media_iterator
    it2 = gp2.media_iterator
    count1 = 0
    count2 = 0

    for image in it1:
        if count1 == 20:
            break
        try:
            album_image = AlbumImage(google_photo=image, album_title=configurations.ACCOUNT_NAME)
            all_the_images[album_image.hash] = album_image
            count1 += 1
        except ValueError:
            pass
    for image in it2:
        if count2 == 20:
            break
        try:
            count2 += 1
            album_image = AlbumImage(google_photo=image, album_title=configurations2.ACCOUNT_NAME)
            hash = album_image.hash
            if hash in all_the_images:
                if hash not in duplicates:
                    duplicates[hash] = set()
                duplicates[hash].add(album_image)
                duplicates[hash].add((all_the_images[hash]))
            else:
                all_the_images[album_image.hash] = album_image
        except ValueError:
            pass
    print("count1: " + str(count1) + " count2: " + str(count2))
    return duplicates


class Dashboard:
    def __init__(self):
        self.duplicated_photos = self._find_duplicated_photos()
        self.app = Dash(DASHBOARD["app_name"])
        self.port = DASHBOARD["app_port"]
        self.app.title = DASHBOARD["app_name"]
        self.app.layout = self.serve_layout

    def launch(self):
        Timer(1, self._open_browser).start()
        self.app.run_server(port=self.port, use_reloader=False)

    def refresh_data(self):
        self.duplicated_photos = self._find_duplicated_photos()

    def _open_browser(self):
        webbrowser.open_new(f"http://localhost:{self.port}")

    def _find_duplicated_photos(self):
        google_photos_client1 = GooglePhotosClient(configurations=configurations)
        google_photos_client2 = GooglePhotosClient(configurations=configurations2)
        return duplicates(google_photos_client1, google_photos_client2)
        # google_photos_client = GooglePhotosClient(configurations=configurations)
        # return google_photos_client.duplicates()

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
        link_li = lambda img: html.Li(html.A(img.album_title,
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
