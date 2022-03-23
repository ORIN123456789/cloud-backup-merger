from PIL import Image
import imagehash
import requests
from io import BytesIO
from configurations import LOOK_FOR_ROTATIONS


class GoogleImage:

    def __init__(self, google_photo, account_name=None, album_title=None, enrich_image_info=False):
        self._validate(google_photo)
        self.url = google_photo["productUrl"]
        self.base_url = google_photo["baseUrl"]
        self.hash = google_photo["baseUrl"]
        self.album_title = album_title
        self.account_name = account_name
        if enrich_image_info:
            self.id_ = google_photo["id"]
            self.filename = google_photo["filename"]
            self.metadata = google_photo["mediaMetadata"]

    def _validate(self, google_photo):
        if "photo" not in google_photo["mediaMetadata"]:
            raise ValueError("this item is not a photo")

    def _pil_image(self, base_url):
        response = requests.get(base_url)
        return Image.open(BytesIO(response.content))

    def _rotations(self, image: Image):
        return [image.rotate(90), image.rotate(180), image.rotate(270)]

    @property
    def url(self):
        return self._url

    @url.setter
    def url(self, _url):
        self._url = _url

    @property
    def hash(self):
        return self._hash

    @hash.setter
    def hash(self, base_url):
        hashes = []
        hash_function = imagehash.average_hash
        image = self._pil_image(base_url)
        hashes.append(str(hash_function(image)))
        # hashes.append(h1)
        # image = image.rotate(180)
        # h2 = str(hash_function(image))
        # hashes.append(h2)
        for angle in [90, 180, 270]:
            image = image.rotate(angle)
            hashes.append(str(hash_function(image)))
        hashes.sort()
        # _hash = h1 if h1 < h2 else h2
        _hash = hashes[0]
        #_hash = str(hash_function(image)) # todo - make it a list
        if LOOK_FOR_ROTATIONS:
            _hash += [hash_function(rotation) for rotation in self._rotations(image)]
        self._hash = _hash

    def rotate(self):
        pass

    def __str__(self):
        return f"Image: \n   -Album: {self.album_title}\n   -URL: {self.url}   \n   -Hash: {self.hash}"

