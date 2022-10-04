from pydantic import (  # pylint: disable=no-name-in-module
    BaseSettings,
    DirectoryPath,
    PostgresDsn,
)

from aiven.settings import LogLevel


class ConsumerSettings(BaseSettings):
    log_level: LogLevel
    certificates_folder: DirectoryPath
    kafka_bootstrap_servers: str
    kafka_topic: str
    kafka_consumer_group: str
    kafka_auto_offset_reset: str = "earliest"
    kafka_poll_timeout: float = 1.0
    postgres_url: PostgresDsn

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

    def kafka_config(self) -> dict:
        return {
            "bootstrap.servers": self.kafka_bootstrap_servers,
            "security.protocol": "SSL",
            "ssl.ca.location": f"{self.certificates_folder}/ca.pem",
            "ssl.key.location": f"{self.certificates_folder}/service.key",
            "ssl.certificate.location": f"{self.certificates_folder}/service.cert",
            "group.id": self.kafka_consumer_group,
            "auto.offset.reset": self.kafka_auto_offset_reset,
            "enable.auto.commit": False,
        }
