import contextlib
import http
import typing as tp

import fastapi
from faststream import confluent

from faststream_bench import common, dependencies


@contextlib.asynccontextmanager
async def app_lifespan(_) -> tp.AsyncIterator[None]:
    async with contextlib.aclosing(dependencies):
        yield


app = fastapi.FastAPI(lifespan=app_lifespan)


@app.post(
    "/publishEvent",
    status_code=http.HTTPStatus.NO_CONTENT,
    response_class=fastapi.Response,
)
async def publish_event(
    event: common.Event,
    broker: confluent.KafkaBroker = fastapi.Depends(dependencies.get_broker),
    settings: common.Settings = fastapi.Depends(dependencies.get_settings),
) -> None:
    await broker.publish(event, topic=settings.topic_name)
