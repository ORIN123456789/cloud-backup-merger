from PIL import Image
import imagehash
import requests
from io import BytesIO


class AlbumImage:
    def __init__(self, url):
        self.url = url

    def pil_image(self):
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
        print(f"Calculating a hash for {url}")
        image = self.pil_image()
        self._hash = imagehash.average_hash(image)

    def __str__(self):
        return f"Image: \nURL: {self.url},\n hash: {self.hash}"