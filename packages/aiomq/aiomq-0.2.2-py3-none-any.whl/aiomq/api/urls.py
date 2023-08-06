from aiomq.api.views import *
from aiohttp import web
import os.path

STATIC_ROOT = os.path.join(os.path.dirname(__file__), 'build')

urlpatterns = [
    web.post('/client/ws', client_ws),  # 注册机器设备
    # web.post('/client/loop', client_loop),  # 注册机器设备
    web.get('/client/send', send),  # 手动触发任务
    web.get('/aiomq/dashboard/ws', websocket_handler),
]

if os.path.exists(STATIC_ROOT):
    async def dashboard(request):
        return web.FileResponse(os.path.join(STATIC_ROOT, 'index.html'))


    urlpatterns += [
        web.get('/', dashboard),
        web.static('/', STATIC_ROOT, show_index=True),
    ]
