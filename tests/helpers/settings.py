from pydantic import BaseSettings, DirectoryPath, PostgresDsn

from aiven.settings import LogLevel


class TestSettings(BaseSettings):
    log_level: LogLevel
    certificates_folder: DirectoryPath
    kafka_bootstrap_servers: str
    kafka_topic: str
    kafka_consumer_group: str
    postgres_url: PostgresDsn

    __test__ = False

    class Config:
        env_file = "./tests/.env"
        env_file_encoding = "utf-8"

    def kafka_config(self) -> dict:
        return {
            "bootstrap.servers": self.kafka_bootstrap_servers,
            "security.protocol": "SSL",
            "ssl.ca.location": f"{self.certificates_folder}/ca.pem",
            "ssl.key.location": f"{self.certificates_folder}/service.key",
            "ssl.certificate.location": f"{self.certificates_folder}/service.cert",
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
