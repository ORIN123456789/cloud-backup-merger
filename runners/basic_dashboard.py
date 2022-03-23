from dash import Dash
import webbrowser
from threading import Timer
from configurations import DASHBOARD



class BasicDashboard:

    def __init__(self):
        self.app = Dash(DASHBOARD["app_name"])
        self.port = DASHBOARD["app_port"]
        self.app.title = DASHBOARD["app_name"]

    def launch(self):
        Timer(1, self._open_browser).start()
        self.app.layout = self.serve_layout
        self.app.run_server(port=self.port, use_reloader=False)

    def refresh_data(self):
        raise NotImplementedError

    def serve_layout(self):
        raise NotImplementedError

    def _open_browser(self):
        webbrowser.open_new(f"http://localhost:{self.port}")
