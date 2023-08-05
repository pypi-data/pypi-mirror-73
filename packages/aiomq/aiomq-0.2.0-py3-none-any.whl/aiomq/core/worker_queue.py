import asyncio
from uuid import uuid1
from aiomq.core.common import *


class QBlock(object):
    def __init__(self, data, ttype):
        self.data = data
        self.ttype = ttype
        self.status = ITEM_STATUS_READY

    @classmethod
    def call_function(cls, name, args, kwargs):
        return cls({
            'name': name,
            'args': args,
            'kwargs': kwargs,
        }, 'call_function')


class BasicQueue(object):
    """工作队列"""

    def __init__(self):
        self.cron_job = asyncio.Queue()
        self.loop = None
        self.jobs = {}

    async def next(self):
        if self.cron_job.qsize():
            return await self.cron_job.get()
        return None

    async def runtime(self, loop):
        from aiomq.core import payload
        self.loop = loop
        pool = payload.RegisterFuncPool.instance()
        while True:
            if pool.available:
                if job := await self.next():
                    # todo  选择机器，检查机器是否存活，分发任务
                    if job.ttype == 'call_function':
                        job.pk = str(uuid1()).replace('-', '')
                        job.rf = pool.choice(job.data['name'])
                        await job.rf.ws.send_bytes(
                            payload.ClientRPCOnceEvent.form_server(job.pk, **job.data).to_binary())
                        pool.locks[job.pk] = job.rf
                        self.jobs[job.pk] = job
            await asyncio.sleep(0.1)

    async def push(self, obj):
        if isinstance(obj, QBlock):
            await self.cron_job.put(obj)
        else:
            raise RuntimeError('WORKERQUEUE.push(obj); obj 的对象必须为 QBlock')


WORKERQUEUE = BasicQueue()
