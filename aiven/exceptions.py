from aiven.models import Website


class CustomException(Exception):
    pass


class WebsiteCheckerException(CustomException):
    def __init__(self, website: Website):
        self.message = f"Error while checking website: {website}"
        super().__init__(self.message)


class DatabaseException(CustomException):
    def __init__(self) -> None:
        self.message = "Database error"
        super().__init__(self.message)
