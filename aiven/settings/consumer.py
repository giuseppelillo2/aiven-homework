from pydantic import BaseSettings, PostgresDsn  # pylint: disable=no-name-in-module

from aiven.settings import LogLevel


class ConsumerSettings(BaseSettings):
    log_level: LogLevel
    kafka_username: str
    kafka_password: str
    kafka_bootstrap_servers: str
    kafka_topic: str
    kafka_consumer_group: str
    kafka_auto_offset_reset: str = "earliest"
    kafka_poll_timeout: float = 1.0
    database_url: PostgresDsn

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

    def kafka_config(self) -> dict:
        return {
            "bootstrap.servers": self.kafka_bootstrap_servers,
            "security.protocol": "SASL_SSL",
            "sasl.mechanism": "PLAIN",
            "sasl.username": self.kafka_username,
            "sasl.password": self.kafka_password,
            "ssl.ca.location": "certificates/ca.pem",
            "group.id": self.kafka_consumer_group,
            "auto.offset.reset": self.kafka_auto_offset_reset,
            "enable.auto.commit": False,
        }
