import pytest

from aiven.exceptions import WebsiteCheckerException
from aiven.models import Website
from aiven.website_checker import WebsiteChecker


@pytest.fixture
def website_checker():
    return WebsiteChecker(timeout=2)


@pytest.fixture
def aiven_website():
    return Website(name="aiven", url="https://aiven.io", regex="aiven")


@pytest.fixture
def google_fake_website():
    return Website(name="google", url="https://google.com:81", regex="google")


def test_200_regex_ok(requests_mock, website_checker, aiven_website):
    requests_mock.get(aiven_website.url, text="aiven.com")
    metric = website_checker.check(aiven_website)
    assert metric.status_code == 200
    assert metric.regex_check


def test_200_regex_ko(requests_mock, website_checker, aiven_website):
    requests_mock.get(aiven_website.url, text="example")
    metric = website_checker.check(aiven_website)
    assert metric.status_code == 200
    assert not metric.regex_check


def test_500(requests_mock, website_checker, aiven_website):
    requests_mock.get(aiven_website.url, text="aiven.com", status_code=500)
    metric = website_checker.check(aiven_website)
    assert metric.status_code == 500
    assert metric.regex_check


def test_timeout(website_checker, google_fake_website):
    with pytest.raises(WebsiteCheckerException):
        website_checker.check(google_fake_website)
