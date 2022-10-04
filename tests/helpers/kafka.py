import json
from dataclasses import dataclass

import pytest
from confluent_kafka import Consumer, Producer
from confluent_kafka.admin import AdminClient


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


@dataclass
class MockKafkaJsonMessage:
    data: dict

    def decode(self, _):
        return json.dumps(self.data)


@dataclass
class MockKafkaMessage:
    message: MockKafkaJsonMessage

    def value(self):
        return self.message
