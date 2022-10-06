import logging

import psycopg2
import pytest
from confluent_kafka import Consumer, Producer
from confluent_kafka.admin import AdminClient

from aiven.metrics_writer import MetricsWriter
from tests.helpers.db import MockDbConnection
from tests.helpers.website_checker_mock import WebsiteCheckerMock


@pytest.fixture
def db_connection(settings):
    return psycopg2.connect(dsn=settings.database_url)


@pytest.fixture
def mock_db_connection():
    return MockDbConnection()


@pytest.fixture
def kafka_producer(settings):
    return Producer(settings.kafka_producer_config())


@pytest.mark.timeout(10)
@pytest.fixture
def kafka_consumer(settings):
    return Consumer(settings.kafka_consumer_config())


@pytest.fixture
def kafka_admin(settings):
    return AdminClient(settings.kafka_config())


@pytest.fixture
def website_checker_mock():
    return WebsiteCheckerMock()


@pytest.fixture
def metrics_writer_mock_db(mock_db_connection):
    return MetricsWriter(
        db_connection=mock_db_connection,
        logger=logging.getLogger(),
    )
