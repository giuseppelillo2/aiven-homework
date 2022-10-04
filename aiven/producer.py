import logging
import threading
import time

from confluent_kafka import Producer

from aiven.exceptions import WebsiteCheckerException
from aiven.metrics_producer import MetricsProducer
from aiven.models import Website
from aiven.settings.producer import ProducerSettings
from aiven.website_checker import WebsiteChecker


def process_website(website: Website, producer: Producer):
    try:
        metrics_producer.monitor_and_publish(website, producer)
    except WebsiteCheckerException as request_ex:
        logging.error("Error while checking website: %s", request_ex)


settings = ProducerSettings()
logging.basicConfig(level=settings.log_level.value)

kafka_producer = Producer(settings.kafka_config())
website_checker = WebsiteChecker(timeout=settings.request_timeout)
websites: list[Website] = [
    Website(name=w.name, url=w.url, regex=w.regex) for w in settings.websites
]
metrics_producer = MetricsProducer(
    website_checker=website_checker,
    logger=logging.getLogger(),
    kafka_topic=settings.kafka_topic,
)

logging.info("Starting the Kafka Producer:\n\ttopic: %s", settings.kafka_topic)


start_time = time.time()
while True:
    for w in websites:
        threading.Thread(target=process_website, args=(w, kafka_producer)).start()
    time.sleep(
        settings.check_interval - ((time.time() - start_time) % settings.check_interval)
    )
