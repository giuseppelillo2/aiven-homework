import psycopg2
import pytest

from aiven.models import WebsiteMetric


class MockDbConnection:
    def cursor(self):
        raise psycopg2.DatabaseError()


@pytest.fixture
def db_connection(settings):
    return psycopg2.connect(dsn=settings.postgres_url)


@pytest.fixture
def mock_db_connection():
    return MockDbConnection()


def clean_table(db_connection):
    cur = db_connection.cursor()
    cur.execute("DELETE FROM metrics")
    db_connection.commit()


def row_to_metric(row: tuple) -> WebsiteMetric:
    return WebsiteMetric(
        name=row[0],
        url=row[1],
        response_time=row[2],
        status_code=row[3],
        regex=row[4],
        regex_check=row[5],
        timestamp=row[6],
    )
