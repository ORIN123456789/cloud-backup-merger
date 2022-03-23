from concurrent.futures import as_completed
from concurrent.futures.thread import ThreadPoolExecutor

from gphotospy.media import Media
from gphotospy.album import Album
from gphotospy import authorize

from image import GoogleImage, create_google_image
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

    def get_google_images_list(self):
        images = self.media_iterator
        processes = []
        google_images = []
        with ThreadPoolExecutor(max_workers=None) as executor:
            for image in images:
                processes.append(executor.submit(create_google_image, google_photo=image, account_name=self.account_name))
            for _ in as_completed(processes):
                google_images.append(_.result())
        return google_images

    def get_google_images_list_by_album_id(self, album_id, album_title):
        images = self.media_manager.search_album(album_id)
        processes = []
        google_images = []
        with ThreadPoolExecutor(max_workers=None) as executor:
            for image in images:
                processes.append(executor.submit(create_google_image, google_photo=image, album_title=album_title))
            for _ in as_completed(processes):
                google_images.append(_.result())
        return google_images





