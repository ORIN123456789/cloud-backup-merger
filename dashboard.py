from dash import Dash, html, dcc
import plotly.express as px
import pandas as pd
from google_photos_client import GooglePhotosClient
import configurations
from configurations import DASHBOARD

class Dashboard:
    def __init__(self):
        self.app = Dash(DASHBOARD["appName"])
        self.dataframe = self._dataframe()
        self.figure = self._figure()
        self.app.layout = self._html()

        self.app.run_server(debug=True)

    def _html(self):
        html_code = html.Div(children=[
            html.H1(children='Cloud Backup Merger'),
            dcc.Graph(
                id='occurrences-graph',
                figure=self.figure
            )
        ])
        return html_code

    def _figure(self):
        return px.bar(self.dataframe, x="Photo", y="Occurrences")

    def _dataframe(self):
        google_photos_client = GooglePhotosClient(configurations=configurations)
        duplicates = google_photos_client.duplicates()
        photos = duplicates.keys()
        occurences = [len(duplicates[photo]) for photo in photos]

        df = pd.DataFrame({
            "Photo": photos,
            "Occurrences": occurences
        })
        return df


