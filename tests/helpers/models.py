import json
from dataclasses import dataclass


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
