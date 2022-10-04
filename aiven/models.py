from datetime import datetime

from pydantic import BaseModel, HttpUrl  # pylint: disable=no-name-in-module


class Website(BaseModel):
    name: str
    url: HttpUrl
    regex: str


class WebsiteMetric(BaseModel):
    name: str
    url: HttpUrl
    response_time: float  # milliseconds
    status_code: int
    regex_check: bool
    timestamp: datetime  # iso
