from datetime import datetime

from pydantic import BaseModel, HttpUrl  # pylint: disable=no-name-in-module


class Website(BaseModel):
    """
    Represents a website to check.
    - name: name of the website
    - url: url of the website
    - regex: regex for checking the response content
    """

    name: str
    url: HttpUrl
    regex: str


class WebsiteMetric(Website):
    """
    Represents a check performed on a `aiven.Website`.
    - name: name of the website
    - url: url of the website
    - response_time: how many milliseconds it took to respond
    - regex: regex used for checking the response content
    - regex_check: True if the regex matched the content of the response, False otherwise
    - timestamp: timestamp of when the check was performed
    """

    name: str
    url: HttpUrl
    response_time: float  # milliseconds
    status_code: int
    regex: str
    regex_check: bool
    timestamp: datetime
