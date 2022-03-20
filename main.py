from google_photos_client import GooglePhotosClient
import configurations
from dashboard2 import Dashboard
from exceptions import InternetException
from image import AlbumImage


def duplicates(gp1, gp2):
    all_the_images = dict()
    duplicates = dict()
    it1 = gp1.media_iterator
    it2 = gp2.media_iterator

    for image in it1:
        try:
            album_image = AlbumImage(google_photo=image, album_title="album_title")
            all_the_images[album_image.hash] = album_image
        except ValueError:
            pass
        for image in it2:
            try:
                album_image = AlbumImage(google_photo=image, album_title="album_title")
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