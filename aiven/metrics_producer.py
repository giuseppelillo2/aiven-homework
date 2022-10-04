from logging import Logger

from confluent_kafka import Producer

from aiven.models import Website
from aiven.website_checker import WebsiteChecker


class MetricsProducer:
    website_checker: WebsiteChecker
    logger: Logger
    kafka_topic: str

    def __init__(
        self,
        website_checker: WebsiteChecker,
        logger: Logger,
        kafka_topic: str,
    ):
        self.website_checker = website_checker
        self.logger = logger
        self.kafka_topic = kafka_topic

    def monitor_and_publish(self, website: Website, kafka_producer: Producer):
        """
        Monitors a website and publishes the check into the Kafka topic `self.kafka_topic`.

        :raises WebsiteCheckerException: error while checking the status of website
        :raises KafkaException: error while publishing message
        :raises BufferError: if the internal producer message queue is full
        """
        self.logger.debug("Checking status of: %s", website)
        metric = self.website_checker.check(website)
        message = metric.json()
        kafka_producer.produce(topic=self.kafka_topic, key=metric.url, value=message)
        kafka_producer.flush()
        self.logger.info("Produced metric: %s", metric)
