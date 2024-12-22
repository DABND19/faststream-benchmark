import logging

import aiomisc
from faststream import confluent

from faststream_bench import common, dependencies

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def subscribe_handler(broker: confluent.KafkaBroker, settings: common.Settings) -> None:
    @broker.subscriber(
        settings.topic_name,
        batch=True,
        auto_commit=False,
        auto_offset_reset="earliest",
        group_id=settings.group_id,
    )
    async def handler(events: list[common.Event]) -> None:
        logger.info("Received events: %s", events)


class KafkaConsumer(aiomisc.Service):
    async def start(self) -> None:
        settings = dependencies.get_settings()
        self._broker = await dependencies.get_broker()
        subscribe_handler(self._broker, settings)
        await self._broker.start()

    async def stop(self, exception: Exception | None = None) -> None:
        await self._broker.close()


if __name__ == "__main__":
    with aiomisc.entrypoint(
        KafkaConsumer(),
        common.MetricServer(host="0.0.0.0", port=8001),
        common.ResourceUsageCollector(interval=1),
        log_config=False,
    ) as loop:
        try:
            loop.run_forever()
        finally:
            loop.run_until_complete(dependencies.aclose())
