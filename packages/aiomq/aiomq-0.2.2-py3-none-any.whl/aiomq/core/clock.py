import asyncio
from time import time

from aiomq.core.worker_queue import WORKERQUEUE, QBlock

CRON_TIMER = [
    {
        'name': 'echo',
        'args': ('1', '2'),
        'kwargs': {},
        'every': 60,
    },
    {
        'name': 'echo30',
        'args': ('1', '2'),
        'kwargs': {},
        'every': 120,
    }
]


class Clock:
    """定时任务"""

    def __init__(self):
        self.cron_job = {}
        self.loop = None
        self.last_time = time()
        self.interval = 0.1

    async def create_cron_task(self, config):
        while True:
            await asyncio.sleep(config['every'])
            await WORKERQUEUE.priority_push(QBlock.call_function(**config))

    async def runtime(self, loop):
        for cron in CRON_TIMER:
            loop.create_task(self.create_cron_task(cron))


GLOBAL_CLOCK = Clock()
