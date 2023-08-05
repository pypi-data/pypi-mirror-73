from aiohttp import web
import aiohttp, asyncio
from aiohttp.http_websocket import WSMessage
from datetime import datetime
from aiomq.api.models import TaskErrorLogs
from aiomq.core.worker_queue import WORKERQUEUE


async def websocket_handler(request):
    from aiomq.core import payload
    ws = web.WebSocketResponse()
    await ws.prepare(request)
    pool = payload.RegisterFuncPool.instance()
    async for msg in ws:
        if isinstance(msg, WSMessage) and msg.type == aiohttp.WSMsgType.TEXT:
            while True:
                print(WORKERQUEUE.cron_job.qsize())
                await ws.send_json({
                    'ready': WORKERQUEUE.cron_job.qsize(),
                    'pedding': len(pool.locks),
                    'error': await TaskErrorLogs.all().count(),
                    'ts': datetime.now().strftime('%H:%M:%S')
                })
                await asyncio.sleep(5)
        elif msg.type == aiohttp.WSMsgType.ERROR:
            print('ws connection closed with exception %s' % ws.exception())
    print('websocket connection closed')
    return ws




