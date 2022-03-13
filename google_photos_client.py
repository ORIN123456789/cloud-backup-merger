from gphotospy.media import Media
from gphotospy.album import Album
from gphotospy import authorize
from image import AlbumImage
from exceptions import InternetException


class GooglePhotosClient:
    def __init__(self, configurations):
            self.configurations = configurations
            self.google_photos_service = authorize.init(self.configurations.CREDENTIALS_PATH)
            if self.google_photos_service is None:
                raise InternetException
            self.media_manager = Media(self.google_photos_service)
            self.albums = Album(self.google_photos_service).list()

    def duplicates(self):
        all_the_images = dict()
        duplicates = dict()

        for album in self.albums:
            album_id = album.get("id")
            album_title = album.get("title")
            album_images = self.media_manager.search_album(album_id)

            for image in album_images:
                try:
                    album_image = AlbumImage(google_photo=image, album_title=album_title)
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

