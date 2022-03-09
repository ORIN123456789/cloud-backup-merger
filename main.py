from google_photos_client import GooglePhotosClient
import configurations


def main():
    google_photos_client = GooglePhotosClient(configurations=configurations)
    duplicates = google_photos_client.duplicates()
    for hash, urls in duplicates.items():
        print(hash)
        print(len(urls))
        for url in urls:
            print(url)
        print('-----')


if __name__ == "__main__":
    main()