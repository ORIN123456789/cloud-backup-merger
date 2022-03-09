from google_photos_client import GooglePhotosClient
import configurations
from dashboard import Dashboard


def main():
    if configurations.IS_DASHBOARD:
        Dashboard()

    else:
        google_photos_client = GooglePhotosClient(configurations=configurations)
        duplicates = google_photos_client.duplicates()
        for hash, images in duplicates.items():
            print(hash)
            print("Number of occurrences", len(images))
            for image in images:
                print(image)
            print('-------------')


if __name__ == "__main__":
    main()