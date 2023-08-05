import asyncio
import logging

import aiohttp
import aiohttp.client_exceptions
from aiohttp import WSMessage

from aiomq.core.payload import ClientHeartBeatEvent, RegisterFunc, ClientActionRegisterEvent, ClientCheckEvent


class AioWebsocket(object):
    logging = logging.getLogger('aiomq.client')

    def __init__(self, prefix, tasks, max_reconnection=3, cycle_time=10,
                 ping_interval_by_seconds: int = 20):
        self.prefix = prefix
        self.reconnection = 1  # 当前试连接次数
        self.max_reconnection = max_reconnection  # 最大连接次数
        self.cycle_time = cycle_time
        self.ping_interval_by_seconds = ping_interval_by_seconds
        self.loop = asyncio.get_event_loop()

        self.logging.setLevel(logging.DEBUG)
        self.tasks = tasks

    async def websocket_startup(self):
        session = aiohttp.ClientSession()
        try:
            async with session.ws_connect(f'{self.prefix}/client/ws', method='POST') as ws:
                await asyncio.gather(*[
                    asyncio.ensure_future(func(ws)) for func in self.tasks
                ])
        except (ConnectionRefusedError, asyncio.TimeoutError, aiohttp.client_exceptions.ClientConnectorError):
            if self.reconnection < self.max_reconnection:
                self.reconnection += 1
                self.logging.warning(f'TCP 连接失败. url: {self.prefix}/client/ws {self.cycle_time}秒后重试')
                await asyncio.sleep(self.cycle_time)
                return await self.websocket_startup()
            raise ConnectionError(f'TCP 重试超过{self.max_reconnection}次，关闭链接')

    def forever(self):
        try:
            self.loop.run_until_complete(self.websocket_startup())
        except KeyboardInterrupt:
            pass


class AioMq(AioWebsocket):
    def __init__(self, name, prefix, max_reconnection=3, cycle_time=10):
        super().__init__(prefix,
                         tasks=[self.on_init, self.on_msg, self.on_ping],
                         max_reconnection=max_reconnection,
                         cycle_time=cycle_time)
        self.on_funcs = {}
        self.alias = name
        self.stop_sign = self.loop.create_future()  # type: asyncio.Future[None]  # add a stop sign to control the loop
        self.inputs = asyncio.Queue(loop=self.loop)

    async def on_ping(self, ws):
        while not self.stop_sign.done():
            await asyncio.sleep(self.ping_interval_by_seconds)
            await ws.send_bytes(ClientHeartBeatEvent.form_client(
                name=self.alias
            ).to_binary())  # 记录客户端心跳

    async def on_msg(self, ws):
        from aiomq.core import payload
        async for msg in ws:
            if isinstance(msg, WSMessage):
                if msg.type == aiohttp.WSMsgType.BINARY:
                    data = payload.Event.deserialize(msg.data)
                    event_obj = getattr(payload, data['event_name'])(**data)
                    if hasattr(event_obj, 'to_client') and callable(getattr(event_obj, 'to_client')):
                        await event_obj.to_client(ws)
            elif msg.type == aiohttp.WSMsgType.CLOSED:
                break
            elif msg.type == aiohttp.WSMsgType.ERROR:
                break
        self.loop.call_soon_threadsafe(self.stop_sign.set_result, None)  # break the event loop

    async def on_init(self, ws):
        await ws.send_bytes(ClientHeartBeatEvent.form_client(
            name=self.alias
        ).to_binary())  # 首次上报客户端
        for name, rf in self.on_funcs.items():
            await ws.send_bytes(ClientActionRegisterEvent.form_client(rf).to_binary())

    def register(self, name=None, help_text=''):
        def wraps(func):
            func_name = name or func.__name__
            self.on_funcs[func_name] = RegisterFunc(func_name, help_text, call_back=func)
            return func

        return wraps
