import logging
from datetime import datetime

from aiven.metrics_producer import MetricsProducer
from aiven.metrics_writer import MetricsWriter
from tests.helpers.db import *
from tests.helpers.kafka import *
from tests.helpers.settings import TestSettings
from tests.helpers.website_checker_mock import *


@pytest.fixture
def settings():
    return TestSettings()


@pytest.fixture
def metrics_writer(db_connection):
    return MetricsWriter(
        db_connection=db_connection,
        logger=logging.getLogger(),
    )


@pytest.fixture
def metrics_producer(website_checker_mock, settings):
    return MetricsProducer(
        website_checker=website_checker_mock,
        logger=logging.getLogger(),
        kafka_topic=settings.kafka_topic,
    )


@pytest.fixture
def mock_metrics(kafka_admin, db_connection, settings):
    kafka_admin.delete_topics([settings.kafka_topic])
    clean_table(db_connection)
    yield [
        MockWebsiteMetric(
            name="aiven",
            url="https://aiven.io",
            regex="c",
            status_code=200,
            response_time=12.7,
            regex_check=True,
            timestamp=datetime.now(),
        ),
        MockWebsiteMetric(
            name="google",
            url="https://google.com",
            regex="a",
            status_code=500,
            response_time=23,
            regex_check=False,
            timestamp=datetime.now(),
        ),
    ]
    kafka_admin.delete_topics([settings.kafka_topic])
    clean_table(db_connection)


@pytest.mark.timeout(30)
def test_end_to_end(
    mock_metrics,
    metrics_producer,
    kafka_producer,
    kafka_consumer,
    metrics_writer,
    db_connection,
    settings,
):
    for w in mock_metrics:
        metrics_producer.monitor_and_publish(w, kafka_producer)

    processed = 0

    kafka_consumer.subscribe([settings.kafka_topic])
    while processed < len(mock_metrics):
        kafka_message = kafka_consumer.poll(0.5)

        if kafka_message is None:
            continue
        if kafka_message.error():
            pytest.fail("Kafka consumer error")
        metrics_writer.write(kafka_message)
        processed += 1

    cur = db_connection.cursor()
    cur.execute(
        f"SELECT * FROM metrics",
    )
    db_metrics = [row_to_metric(row) for row in cur.fetchall()]
    assert db_metrics == [m.website_metric() for m in mock_metrics]
