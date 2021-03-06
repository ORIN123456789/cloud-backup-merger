from dash import html

from calculate_duplications import duplicates_between_albums
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
        return duplicates_between_albums(google_photos_client)

    def serve_layout(self):
        self.refresh_data()
        if len(self.duplicated_photos) == 0:
            _html = html.Div(children=[html.Img(src=DASHBOARD["logo"], id='logo'),
                             html.Img(src=DASHBOARD["no_duplicates"], className='message')])
        else:
            photo_list = self.images_list_to_html_object(self.duplicated_photos.values())
            _html = html.Div(children=[html.Img(src=DASHBOARD["logo"], id='logo'),
                                       html.Img(src=DASHBOARD["instruction"], id='instruction'),
                                       html.Img(src=DASHBOARD["album_text"], id='message'),
                                       html.Div([photo_list], className='table'),
                                       ]
                             )
        return _html

    def photo_list(self, album_images):
        base_url = next(iter(album_images)).base_url
        link_li = lambda img: html.Li(html.A("Album " + img.album_title,
                                             className='album',
                                             href=img.url,
                                             target="_blank"),
                                      className='list')
        links = html.Ul(children=[link_li(img) for img in album_images])

        photos_list = html.Li(children=[html.Img(src=base_url,
                                        className='image'),
                               links],
                     className='photo_li')
        return photos_list

    def images_list_to_html_object(self, photos):
        photo_list = html.Ul(className='duplicated_photos',
                             children=[self.photo_list(image) for image in photos])
        return photo_list
