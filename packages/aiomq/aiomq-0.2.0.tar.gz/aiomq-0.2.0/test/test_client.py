import asyncio
import unittest
from aiomq.client import *

mq = AioMq('测试机一号', 'http://127.0.0.1:8080', 3, 10)


class TestClient(unittest.TestCase):
    def test_echo(self):
        @mq.register()
        async def echo(a, c, b='1', d='2', *args, **kwargs):
            import asyncio
            print('echo')
            await asyncio.sleep(10)
            print(a, c, b, d)

        @mq.register()
        async def echo2(a, c, b='1', d='2', *args, **kwargs):
            raise RuntimeError

        mq.forever()


if __name__ == '__main__':
    unittest.main()
