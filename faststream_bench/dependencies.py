import contextlib

import prometheus_client
from faststream import confluent
from faststream.confluent import prometheus as confluent_prom

from faststream_bench import common

_exit_stack = contextlib.AsyncExitStack()
_settings: common.Settings | None = None
_broker: confluent.KafkaBroker | None = None


def get_settings() -> common.Settings:
    global _settings
    if not _settings:
        _settings = common.Settings()
    return _settings


async def get_broker() -> confluent.KafkaBroker:
    global _broker
    if not _broker:
        settings = get_settings()
        _broker = confluent.KafkaBroker(settings.kafka_hosts)
        _broker.add_middleware(confluent_prom.KafkaPrometheusMiddleware(registry=prometheus_client.REGISTRY))
        await _broker.connect()
        _exit_stack.push_async_callback(_broker.close)
    return _broker


async def aclose() -> None:
    await _exit_stack.aclose()
