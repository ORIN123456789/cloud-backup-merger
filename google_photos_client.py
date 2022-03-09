from gphotospy.media import Media
from gphotospy.album import Album
from gphotospy import authorize
from image import AlbumImage


class GooglePhotosClient:
    def __init__(self, configurations):
        self.configurations = configurations
        self.google_photos_service = authorize.init(self.configurations.CREDENTIALS_PATH)
        self.media_manager = Media(self.google_photos_service)
        self.albums = list(Album(self.google_photos_service).list())

    def duplicates(self):
        all_the_images = dict()
        duplicates = dict()
        for album in self.albums:
            album_id = album.get("id")
            album_images = self.media_manager.search_album(album_id)
            for image in album_images:
                album_image = AlbumImage(image)
                if album_image.hash in all_the_images:
                    print("duplicated")
                else:
                    all_the_images[album_image.hash] = album_image.url
                    print("unique")

        return duplicates

