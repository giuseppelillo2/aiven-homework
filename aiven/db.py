import psycopg2
from psycopg2._psycopg import connection  # pylint: disable=no-name-in-module

from aiven.exceptions import DatabaseException
from aiven.models import WebsiteMetric


def db_connect(url: str):
    return psycopg2.connect(dsn=url)


def insert_record(db_connection: connection, metric: WebsiteMetric) -> None:
    """
    Insert a metric into the `metrics` table.

    :param db_connection:
    :param metric: metric to insert
    :raises DatabaseException: error while interacting with the database
    """
    try:
        cur = db_connection.cursor()
        cur.execute(
            "INSERT INTO metrics (name, url, response_time, status_code, regex, regex_check, timestamp) "
            "VALUES (%s, %s, %s, %s, %s, %s, %s)",
            (
                metric.name,
                metric.url,
                metric.response_time,
                metric.status_code,
                metric.regex,
                metric.regex_check,
                metric.timestamp,
            ),
        )
        db_connection.commit()
    except psycopg2.Error as db_error:
        raise DatabaseException() from db_error
