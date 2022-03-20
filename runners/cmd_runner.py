from google_photos_client import GooglePhotosClient
import configurations


class CMD:

    def launch(self):
        google_photos_client = GooglePhotosClient(configurations=configurations)
        duplicates = google_photos_client.duplicates_between_albums()
        for hash, images in duplicates.items():
            print(hash)
            print("Number of occurrences", len(images))
            for image in images:
                print(image)
            print('-------------')
