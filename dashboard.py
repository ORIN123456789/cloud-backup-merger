import random

from dash import Dash, html, dcc
import plotly.express as px
import pandas as pd
from google_photos_client import GooglePhotosClient
import configurations
from configurations import DASHBOARD


def save_duplicates(duplicates):
    res = []
    for hash in duplicates:
        image = duplicates[hash].pop()
        res.append(image)
    return res

def photo_li(img_set):
    base_url = None
    for img in img_set:
        base_url = img.base_url
        break
    link_li = lambda img: html.Li(html.A("Albume: " + img.album_title, href=img.url, target="_blank"))
    links = html.Ul(children=[link_li(img) for img in img_set])
    li = html.Li(html.Div(children=[html.P("photo-1"),
                      html.Img(src=base_url, style={'width': '90px', 'height': '100px'}),
                           links
                           ]))
    return li

def create_list_of_photos(duplicates):
    photo_list = html.Ul(
        id='my-list', children=[photo_li(img_set) for img_set in duplicates],
        style={'display': 'inline', 'float' : 'left'}
    )
    return photo_list


class Dashboard:
    def __init__(self):
        self.app = Dash(DASHBOARD["appName"])
        self.dataframe = self._dataframe()
        self.figure = self._figure()
        self.app.layout = self._html()
        self.photos = []

        self.app.run_server(debug=True)

    def _html(self):
        photo_li = lambda img: html.Li(children = [html.P("photo-1"),
            html.Img(src=img.base_url, style={'width': '90px', 'height': '100px'})])
        photo_list = create_list_of_photos(self.photos)
            # html.Ul(
            # id = 'my-list', children = [photo_li(img) for img in self.photos],
            # style={'display': 'inline-block'})

        # for p in self.photos:
        #     photo_list += [html.Li([
        #         'photo1',
        #         html.Img(src='https://raw.githubusercontent.com/michaelbabyn/plot_data/master/bridge.jpg',
        #                  style={'width': '500px', 'height': '600px'})
        #     ])]
        html_code = html.Div(children=[
            html.H1(children='Cloud Backup Merger'),
            dcc.Graph(
                id='occurrences-graph',
                figure=self.figure
            ),
            html.Div([photo_list
                # html.Img(src='https://raw.githubusercontent.com/michaelbabyn/plot_data/master/bridge.jpg'),
                #       html.Img(src='https://raw.githubusercontent.com/michaelbabyn/plot_data/master/bridge.jpg')
                      ])
        ])
        return html_code

    def _figure(self):
        return px.bar(self.dataframe, x="Photo", y="Occurrences")

    def _dataframe(self):
        google_photos_client = GooglePhotosClient(configurations=configurations)
        duplicates = google_photos_client.duplicates()
        self.photos = duplicates.values() #save_duplicates(duplicates)
        photos = duplicates.keys()
        occurences = [len(duplicates[photo]) for photo in photos]

        df = pd.DataFrame({
            "Photo": photos,
            "Occurrences": occurences
        })
        return df




