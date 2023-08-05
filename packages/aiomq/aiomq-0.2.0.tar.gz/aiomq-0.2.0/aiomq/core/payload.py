import json
import logging
import struct
import inspect
import traceback
from time import time

from aiomq.core.common import ITEM_STATUS_READY, ITEM_STATUS_PENDING, ITEM_STATUS_DONE, ITEM_STATUS_ERROR
from aiomq.core.pool import BasicPool
from aiomq.utils.network import get_mac_address, get_host_ip, get_host_name
from aiomq.api.models import Running, TaskErrorLogs


class RegisterFunc(object):
    def __init__(self, name, help_text, source_code='', call_back=None, ws=None):
        self.ws = ws
        self.name = name
        self.help_text = help_text
        self.source_code = source_code
        if callable(call_back):
            self.call_back = call_back
            self.source_code = inspect.getsource(call_back)
            self.args = inspect.getfullargspec(call_back)
        else:
            self.call_back = None
            self.args = None

    @property
    def active(self):
        return True


class RegisterFuncPool(BasicPool):
    @classmethod
    def instance(cls):
        if not hasattr(RegisterFuncPool, "_instance"):
            RegisterFuncPool._instance = RegisterFuncPool()
        return RegisterFuncPool._instance

    data = []
    locks = {}

    def list(self):
        return set([i.name for i in self.data])

    @property
    def available(self):
        a = set([i.ws.mac_address for i in self.data])
        b = set([i.ws.mac_address for i in self.locks.values()])
        return a - b

    def choice(self, name):
        # todo 要处理多机器的情况
        for i in self.data:
            if i in self.locks.values():
                continue
            if i.name == name:
                if i.ws:
                    print(i.ws.mac_address)
                return i


class Event:
    def __init__(self, event_name, body):
        self.data = dict(event_name=event_name, body=body)
        self.body = body
        self.event_name = event_name

    def __repr__(self):
        return json.dumps(self.data)

    def to_binary(self):
        return self.serialize(self.__repr__())

    @staticmethod
    def serialize(text):
        # type: (str) -> bytes
        msg = text.encode()
        return struct.pack("!i%ss" % len(msg), len(msg), msg)

    @staticmethod
    def deserialize(byte_array):
        # type: (bytes) -> dict
        try:
            length = int.from_bytes(byte_array[:4], 'big')
            _text = byte_array[4: 4 + length]
            text = _text.decode()
            return json.loads(text)
        except (IndexError, json.decoder.JSONDecodeError):
            logging.getLogger('daq').error(f"Cannot decode the original bytes: {byte_array}")
            return {}


class ClientHeartBeatEvent(Event):
    async def to_service(self, ws):
        running_obj = await Running.get_or_none(mac_address=self.body['mac_address'])
        if not hasattr(ws, 'mac_address'):
            ws.mac_address = self.body['mac_address']
        if running_obj:
            running_obj.ts = self.body['ts']
            await running_obj.save()
        else:
            await Running.create(mode='ws', **self.body)

    @classmethod
    def form_client(cls, name, ):
        return cls(cls.__name__, {
            'name': name,
            'mac_address': f'{get_mac_address()}_{name}',
            'host_ip': get_host_ip(),
            'ts': int(time() * 1000),
            'host_name': get_host_name(),
        })


class ClientActionRegisterEvent(Event):
    async def to_service(self, ws):
        # 服务端池 注册
        RegisterFuncPool.instance().data.append(RegisterFunc(ws=ws, **self.body))

    @classmethod
    def form_client(cls, register_func):
        if not isinstance(register_func, RegisterFunc):
            raise TypeError('register_func  必须是 RegisterFunc')
        # 本地池 注册
        RegisterFuncPool.instance().data.append(register_func)
        return cls(cls.__name__, {
            'name': register_func.name,
            'help_text': register_func.help_text,
            'source_code': register_func.source_code,
        })


class ClientRPCOnceEvent(Event):
    async def to_client(self, ws):
        await ws.send_bytes(ClientCheckEvent.form_client(self.body['task_id'],
                                                         self.event_name, ITEM_STATUS_PENDING).to_binary())
        fc = RegisterFuncPool.instance().choice(self.body['name'])

        try:
            await fc.call_back(*self.body['args'], **self.body['kwargs'])
            await ws.send_bytes(ClientCheckEvent.form_client(self.body['task_id'],
                                                             self.event_name, ITEM_STATUS_DONE).to_binary())
        except Exception:
            await ws.send_bytes(ClientCheckEvent.form_client(self.body['task_id'],
                                                             self.event_name, ITEM_STATUS_ERROR,
                                                             traceback.format_exc()
                                                             ).to_binary())

    @classmethod
    def form_server(cls, pk, name, args, kwargs):
        return cls(cls.__name__, {
            'task_id': pk,
            'name': name,
            'args': args,
            'kwargs': kwargs,
        })


class ClientCheckEvent(Event):
    async def to_service(self, ws):
        from aiomq.core.worker_queue import WORKERQUEUE
        pool = RegisterFuncPool.instance()
        if self.body['name'] in WORKERQUEUE.jobs:
            job = WORKERQUEUE.jobs[self.body['name']]
            job.status = self.body['status']
            if job.status == ITEM_STATUS_ERROR:
                if running := await Running.get_or_none(mac_address=ws.mac_address):
                    print(running)
                    await TaskErrorLogs.create(
                        name=job.rf.name,
                        source_data=json.dumps(job.data),
                        source_code=job.rf.source_code,
                        client_ip=running.host_ip,
                        client_host_name=running.host_name,
                        error_content=self.body['error_exception'],
                        ts=int(time() * 1000),
                    )
            if job.status in [ITEM_STATUS_DONE, ITEM_STATUS_ERROR]:
                del pool.locks[job.pk]
                del WORKERQUEUE.jobs[self.body['name']]

    @classmethod
    def form_client(cls, name, event, status, error_exception=''):
        return cls(cls.__name__, {'name': name, 'event': event, 'status': status, 'error_exception': error_exception})
