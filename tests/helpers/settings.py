from pydantic import BaseSettings, PostgresDsn

from aiven.settings import LogLevel


class TestSettings(BaseSettings):
    log_level: LogLevel = LogLevel.INFO
    kafka_bootstrap_servers: str
    kafka_username: str
    kafka_password: str
    kafka_topic: str
    kafka_consumer_group: str = "test"
    postgres_url: PostgresDsn

    __test__ = False

    class Config:
        env_file = "./tests/.env"
        env_file_encoding = "utf-8"

    def kafka_config(self) -> dict:
        return {
            "bootstrap.servers": self.kafka_bootstrap_servers,
            "ssl.ca.location": "certificates/ca.pem",
            "security.protocol": "SASL_SSL",
            "sasl.mechanism": "PLAIN",
            "sasl.username": self.kafka_username,
            "sasl.password": self.kafka_password,
        }

    def kafka_consumer_config(self) -> dict:
        return {
            **self.kafka_config(),
            "group.id": self.kafka_consumer_group,
            "auto.offset.reset": "earliest",
            "enable.auto.commit": True,
        }

    def kafka_producer_config(self) -> dict:
        return {
            **self.kafka_config(),
            "acks": "1",
        }
