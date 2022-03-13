
class InternetException(Exception):
    def __init__(self):
        super().__init__("Make sure your computer has an active internet connection")