from google_photos_client import GooglePhotosClient
import configurations


def main():
    google_photos_client = GooglePhotosClient(configurations=configurations)
    google_photos_client.duplicates()


if __name__ == "__main__":
    main()