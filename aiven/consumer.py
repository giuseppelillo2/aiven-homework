import logging

from confluent_kafka import Consumer

from aiven.db import db_connect
from aiven.metrics_writer import MetricsWriter
from aiven.settings.consumer import ConsumerSettings


def run_consumer() -> None:
    settings = ConsumerSettings()
    logging.basicConfig(level=settings.log_level.value)

    db_connection = db_connect(settings.postgres_url)
    consumer = Consumer(settings.kafka_config())
    metrics_writer = MetricsWriter(
        db_connection=db_connection, logger=logging.getLogger()
    )
    consumer.subscribe([settings.kafka_topic])

    logging.info(
        "Starting the Kafka Consumer:\n\ttopic: %s\n\tconsumer group: %s",
        settings.kafka_topic,
        settings.kafka_consumer_group,
    )

    while True:
        logging.debug("Polling...")
        kafka_message = consumer.poll(settings.kafka_poll_timeout)

        if kafka_message is None:
            continue
        if kafka_message.error():
            logging.error("Error during polling: %s", kafka_message.error())
            continue
        metrics_writer.write(kafka_message)
        logging.debug(
            "Consuming message: partition=%s, offset=%s",
            kafka_message.partition(),
            kafka_message.offset(),
        )

        consumer.commit(kafka_message, asynchronous=True)
