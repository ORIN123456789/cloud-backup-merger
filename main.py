from google_photos_client import GooglePhotosClient
import configurations


def main():
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