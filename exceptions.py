
class InternetException(Exception):
    def __init__(self):
        super().__init__("Make sure your computer has an active internet connection")


class NoSuchRunner(Exception):
    def __init__(self):
        super().__init__("There is no such runner, check your configurations")


class NotAnImage(ValueError):
    def __init__(self):
        super().__init__("This item is not an image")