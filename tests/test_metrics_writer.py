import pydantic
import pytest

from aiven.exceptions import DatabaseException
from tests.helpers.models import *


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
                "regex": "ai",
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
