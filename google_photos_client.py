from gphotospy.media import Media
from gphotospy.album import Album
from gphotospy import authorize
from image import GoogleImage
from exceptions import InternetException
from common_objects import Account


class GooglePhotosClient:
    def __init__(self, account: Account):
        self.account_name = account.name
        self.google_photos_service = authorize.init(account.credentials)
        if self.google_photos_service is None:
            raise InternetException
        self.media_manager = Media(self.google_photos_service)
        self.albums = Album(self.google_photos_service).list()
        self.media_iterator = self.media_manager.list()

    def duplicates_between_albums(self):
        all_the_images = dict()
        duplicates = dict()

        for album in self.albums:
            album_id = album.get("id")
            album_title = album.get("title")
            album_images = self.media_manager.search_album(album_id)

            for image in album_images:
                try:
                    album_image = GoogleImage(google_photo=image, album_title=album_title)
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
        return duplicates

    @staticmethod
    def duplicates_between_accounts(google_photos_clients):
        all_the_images = dict()
        duplicates = dict()

        for client in google_photos_clients:
            images = client.media_iterator
            for image in images:
                try:
                    album_image = GoogleImage(google_photo=image, account_name=client.account_name)
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

        return duplicates


