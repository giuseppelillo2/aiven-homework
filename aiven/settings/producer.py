from pydantic import (  # pylint: disable=no-name-in-module
    BaseSettings,
    DirectoryPath,
    HttpUrl,
)

from aiven.settings import LogLevel


class WebsiteSetting(BaseSettings):
    name: str
    url: HttpUrl
    regex: str


class ProducerSettings(BaseSettings):
    log_level: LogLevel = LogLevel.INFO
    certificates_folder: DirectoryPath
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
            "security.protocol": "SSL",
            "ssl.ca.location": f"{self.certificates_folder}/ca.pem",
            "ssl.key.location": f"{self.certificates_folder}/service.key",
            "ssl.certificate.location": f"{self.certificates_folder}/service.cert",
            "acks": self.kafka_producer_acks,
        }
