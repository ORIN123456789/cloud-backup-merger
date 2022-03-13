from google_photos_client import GooglePhotosClient
import configurations
from dashboard import Dashboard
from exceptions import InternetException


def main():
    try:
        if configurations.IS_DASHBOARD:
            dashboard = Dashboard()
            dashboard.launch()

        else:
            google_photos_client = GooglePhotosClient(configurations=configurations)
            duplicates = google_photos_client.duplicates()
            for hash, images in duplicates.items():
                print(hash)
                print("Number of occurrences", len(images))
                for image in images:
                    print(image)
                print('-------------')
    except InternetException as e:
        print(e)


if __name__ == "__main__":
    main()