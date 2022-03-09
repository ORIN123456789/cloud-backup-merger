from PIL import Image
import imagehash
import requests
from io import BytesIO


class AlbumImage:

    def __init__(self, google_photo, use_url_only=True):
        self._validate(google_photo)
        self.url = google_photo["baseUrl"]
        if not use_url_only:
            self.id_ = google_photo["id"]
            self.filename = google_photo["filename"]
            self.metadata = google_photo["mediaMetadata"]

    def _validate(self,google_photo):
        if "photo" not in google_photo["mediaMetadata"]:
            raise ValueError("this item is not a photo")

    def _pil_image(self):
        response = requests.get(self.url)
        return Image.open(BytesIO(response.content))

    @property
    def url(self):
        return self._url

    @url.setter
    def url(self, _url):
        self._url = _url
        self.hash = _url

    @property
    def hash(self):
        return self._hash

    @hash.setter
    def hash(self, url):
        image = self._pil_image()
        self._hash = str(imagehash.average_hash(image))

    def __str__(self):
        return f"Image: \n   -URL: {self.url}   \n   -hash: {self.hash}"

