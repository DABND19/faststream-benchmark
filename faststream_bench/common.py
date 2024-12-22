import typing as tp

import aiomisc.service.periodic
import aiomisc.service.uvicorn
import prometheus_client
import psutil
import pydantic
import pydantic_settings

from faststream_bench import metrics


class Event(pydantic.BaseModel):
    message: str


class Settings(pydantic_settings.BaseSettings):
    kafka_hosts: str = "127.0.0.1:9092,127.0.0.1:9093,127.0.0.1:9094"
    topic_name: str = "test-topic"
    group_id: str = "test-group-id"


class MetricServer(aiomisc.service.uvicorn.UvicornService):
    async def create_application(self) -> tp.Any:
        return prometheus_client.make_asgi_app(disable_compression=True)


class ResourceUsageCollector(aiomisc.service.periodic.PeriodicService):
    async def callback(self) -> None:
        metrics.CPU_USAGE.set(psutil.cpu_percent())
