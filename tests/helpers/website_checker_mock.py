from datetime import datetime

from aiven.models import Website, WebsiteMetric


class MockWebsiteMetric(Website):
    status_code: int
    response_time: float
    regex_check: bool
    timestamp: datetime

    def website_metric(self) -> WebsiteMetric:
        return WebsiteMetric(
            name=self.name,
            url=self.url,
            response_time=self.response_time,
            status_code=self.status_code,
            regex=self.regex,
            regex_check=self.regex_check,
            timestamp=self.timestamp,
        )


class WebsiteCheckerMock:
    def check(self, website: MockWebsiteMetric) -> WebsiteMetric:
        return WebsiteMetric(
            name=website.name,
            url=website.url,
            response_time=website.response_time,
            status_code=website.status_code,
            regex=website.regex,
            regex_check=website.regex_check,
            timestamp=website.timestamp,
        )
