import json
from datetime import datetime

from fennel import models
from fennel.client.aio.utils import aioclient
from fennel.exceptions import JobNotFound
from fennel.job import Job


@aioclient
async def get_status(app, uuid) -> Job:
    resp = await app.aioclient.hget(app.keys.status_prefix + f":{uuid}", "status")
    if not resp:
        raise JobNotFound(uuid)
    return resp


@aioclient
async def get_job(app, uuid) -> Job:
    resp = await app.aioclient.hgetall(app.keys.status_prefix + f":{uuid}")
    if not resp:
        raise JobNotFound(uuid)
    return Job(**resp)


@aioclient
async def count_jobs(app):
    return len(
        [x async for x in app.aioclient.iscan(match=app.keys.status_prefix + ":*")]
    )


@aioclient
async def get_messages(app, key, n=100):
    messages = await app.aioclient.xrevrange(key, count=n)
    return [models.Message(id=id, uuid=fields["uuid"]) for id, fields in messages]


@aioclient
async def get_info(app, key):
    info = await app.aioclient.xinfo_stream(key)
    return models.Info(**{k.replace("-", "_"): v for k, v in info.items()})


@aioclient
async def get_groups(app, key):
    groups = await app.aioclient.xinfo_groups(key)
    return [
        models.Group(**{k.replace("-", "_"): v for k, v in d.items()}) for d in groups
    ]


@aioclient
async def get_stream(app, key, n=100):
    return models.Stream(
        key=key,
        info=await get_info(app, key),
        groups=await get_groups(app, key),
        messages=await get_messages(app, key, n=n),
    )


@aioclient
async def get_result(app, key):
    value = json.loads(await app.aioclient.lrange(key, 0, 1)[0])
    return models.Result(
        return_value=value["return_value"], exception=value["exception"]
    )


@aioclient
async def count_results(app):
    return len(
        [x async for x in app.aioclient.iscan(match=app.keys.result_prefix + ":*")]
    )


@aioclient
async def get_heartbeats(app):
    beats = await app.aioclient.hgetall(app.keys.heartbeats)
    return [
        models.Heartbeat(executor_id=k, timestamp=datetime.fromtimestamp(float(v)))
        for k, v in zip(beats.keys(), beats.values())
    ]


@aioclient
async def get_schedule(app):
    return [
        models.ScheduledJob(eta=datetime.fromtimestamp(int(v)), uuid=k)
        async for k, v in app.aioclient.izscan(app.keys.schedule)
    ]


@aioclient
async def get_state(app, messages=100):
    return models.State(
        queue=await get_stream(app, app.keys.queue, n=messages),
        dead=await get_stream(app, app.keys.dead, n=messages),
        heartbeats=await get_heartbeats(app),
        schedule=await get_schedule(app),
    )
