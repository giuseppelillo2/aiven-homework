from logging import Logger

import pydantic
from confluent_kafka import Message
from psycopg2._psycopg import connection  # pylint: disable=no-name-in-module

from aiven.db import insert_record
from aiven.exceptions import DatabaseException
from aiven.models import WebsiteMetric


class MetricsWriter:
    def __init__(self, db_connection: connection, logger: Logger):
        self.db_connection = db_connection
        self.logger = logger

    def write(self, kafka_message: Message):
        """
        Deserializes a Kafka message into an aiven.WebsiteMetric and inserts it into the `metrics` table.

        :param kafka_message: message to deserialize
        :raises pydantic.ValidationError: error while interacting with the database
        :raises DatabaseException: error while interacting with the database
        """
        try:
            metric = WebsiteMetric.parse_raw(kafka_message.value().decode("utf-8"))
            insert_record(db_connection=self.db_connection, metric=metric)
            self.logger.info("Processed message: %s", metric)
        except pydantic.ValidationError as validation_error:
            self.logger.error("Wrong message schema")
            raise validation_error
        except DatabaseException as db_error:
            self.logger.error("Error while inserting record on database")
            raise db_error
