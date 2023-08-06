import asyncio, logging
from uuid import uuid1
from aiomq.core.common import *


class QBlock(object):
    def __init__(self, data, ttype):
        self.data = data
        self.ttype = ttype
        self.status = ITEM_STATUS_READY

    @classmethod
    def call_function(cls, name, args, kwargs, **other):
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
                        if job.rf:
                            try:
                                await job.rf.ws.send_bytes(
                                    payload.ClientRPCOnceEvent.form_server(job.pk, **job.data).to_binary())
                            except AttributeError:
                                pass
                            pool.locks[job.pk] = job.rf
                            self.jobs[job.pk] = job
                        else:
                            logging.warning(f'选择不到机器, 任务先丢弃 job_name: {job.data}')

            await asyncio.sleep(0.1)

    async def push(self, obj):
        if isinstance(obj, QBlock):
            await self.cron_job.put(obj)
        else:
            raise RuntimeError('WORKERQUEUE.push(obj); obj 的对象必须为 QBlock')

    async def priority_push(self, obj):
        if isinstance(obj, QBlock):
            await self.cron_job.put(obj)
            while obj in self.cron_job._queue:
                await asyncio.sleep(0.1)
        else:
            raise RuntimeError('WORKERQUEUE.push(obj); obj 的对象必须为 QBlock')


WORKERQUEUE = BasicQueue()
