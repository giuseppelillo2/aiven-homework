from pydantic import BaseSettings, HttpUrl  # pylint: disable=no-name-in-module

from aiven.settings import LogLevel


class WebsiteSetting(BaseSettings):
    name: str
    url: HttpUrl
    regex: str


class ProducerSettings(BaseSettings):
    log_level: LogLevel = LogLevel.INFO
    kafka_username: str
    kafka_password: str
    kafka_bootstrap_servers: str
    kafka_producer_acks: str = "1"
    kafka_topic: str
    request_timeout: int
    websites: list[WebsiteSetting]
    check_interval: float = 5.0

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
            "acks": self.kafka_producer_acks,
        }
