import logging

import pydantic

from aiven.exceptions import DatabaseException
from aiven.metrics_writer import MetricsWriter
from tests.helpers.db import *
from tests.helpers.kafka import *


@pytest.fixture
def metrics_writer_mock_db(mock_db_connection):
    return MetricsWriter(
        db_connection=mock_db_connection,
        logger=logging.getLogger(),
    )


def test_db_error(
    metrics_writer_mock_db,
):
    kafka_message = MockKafkaMessage(
        MockKafkaJsonMessage(
            {
                "name": "aiven",
                "url": "https://aiven.io",
                "response_time": 20,
                "status_code": 200,
                "regex_check": True,
                "timestamp": "2022-10-04T06:48:49Z",
            }
        )
    )
    with pytest.raises(DatabaseException):
        metrics_writer_mock_db.write(kafka_message)


def test_schema_error(
    metrics_writer_mock_db,
):
    kafka_message = MockKafkaMessage(
        MockKafkaJsonMessage(
            {
                "name": "aiven",
                "response_time": 20,
                "status_code": 200,
                "regex_check": True,
                "timestamp": "2022-10-04T06:48:49Z",
            }
        )
    )
    with pytest.raises(pydantic.ValidationError):
        metrics_writer_mock_db.write(kafka_message)
