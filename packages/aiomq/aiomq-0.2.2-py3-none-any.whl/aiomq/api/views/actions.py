from aiohttp import web
import aiohttp
from aiohttp.http_websocket import WSMessage

from aiomq.utils.response import JsonResponse, CustomJsonResponse
from aiomq.api.models import Running
from aiomq.core.worker_queue import QBlock, WORKERQUEUE
from aiomq.core import payload


async def client_ws(request):
    ws = web.WebSocketResponse()
    await ws.prepare(request)

    async for msg in ws:
        if isinstance(msg, WSMessage):
            if msg.type == aiohttp.WSMsgType.BINARY:
                data = payload.Event.deserialize(msg.data)
                event_obj = getattr(payload, data['event_name'])(**data)
                if callable(getattr(event_obj, 'to_service')):
                    await event_obj.to_service(ws)
            elif msg.type == aiohttp.WSMsgType.PING:
                await ws.pong()
    # 'websocket connection closed'
    return ws


async def send(request):
    name = request.query.get('name')
    pool = payload.RegisterFuncPool.instance()
    if name in pool.list():
        args, kwargs = [], {}
        if 'args' in request.query:
            args = request.query.getall('args')
        kwargs = {i: v for i, v in request.query.items() if i not in ['name', 'args']}
        await WORKERQUEUE.push(QBlock.call_function(name, args, kwargs))  # 将任务推入队列
        return JsonResponse('ok')
    return CustomJsonResponse({

    })
