import re
from datetime import datetime, timezone

import requests
from requests import RequestException

from aiven.exceptions import WebsiteCheckerException
from aiven.models import Website, WebsiteMetric


class WebsiteChecker:
    def __init__(self, timeout: int):
        self.timeout = timeout

    def check(self, website: Website) -> WebsiteMetric:
        """
        Performs a GET on `website.url` and checks its response against `website.regex`.

        :raises WebsiteCheckerException: error while checking the status of website
        """
        try:
            resp = requests.get(website.url, timeout=self.timeout)
        except RequestException as req_ex:
            raise WebsiteCheckerException(website) from req_ex
        return WebsiteMetric(
            name=website.name,
            url=website.url,
            response_time=resp.elapsed.total_seconds() * 1000,
            status_code=resp.status_code,
            regex=website.regex,
            regex_check=self._check_regex(resp.text, website.regex),
            timestamp=datetime.now(timezone.utc),
        )

    @staticmethod
    def _check_regex(body: str, regex: str) -> bool:
        return bool(re.search(regex, body))
