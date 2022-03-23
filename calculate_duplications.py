from exceptions import NotAnImage

from image import GoogleImage


def duplicates_between_accounts(google_photos_clients):
    all_the_images = dict()
    duplicates = dict()

    for client in google_photos_clients:
        for image in client.get_google_images_list():
            if image is None:
                continue
            _hash = image.hash
            if _hash in all_the_images:
                if _hash not in duplicates:
                    duplicates[_hash] = set()
                duplicates[_hash].add(image)
                duplicates[_hash].add((all_the_images[_hash]))
            else:
                all_the_images[image.hash] = image

    return duplicates


def duplicates_between_albums(google_photos_client):
    all_the_images = dict()
    duplicates = dict()

    for album in google_photos_client.albums:
        album_id = album.get("id")
        album_title = album.get("title")

        for image in google_photos_client.get_google_images_list_by_album_id(album_id, album_title):
            if image is None:
                continue
            hash = image.hash
            if hash in all_the_images:
                if hash not in duplicates:
                    duplicates[hash] = set()
                duplicates[hash].add(image)
                duplicates[hash].add((all_the_images[hash]))
            else:
                all_the_images[image.hash] = image

    return duplicates
