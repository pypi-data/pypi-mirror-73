from tortoise import Tortoise, Model, fields
from time import time
from aiomq.utils.translation import ugettext_lazy as _


async def init_db():
    # Here we connect to a SQLite DB file.
    # also specify the app name of "models"
    # which contain models from "app.models"
    await Tortoise.init(
        # db_url='sqlite://db.sqlite3',
        db_url='mysql://root:sun851010@localhost:3306/aiomq',
        modules={'models': ['aiomq.api.models']}
    )
    # global rdb
    # rdb = await aioredis.create_redis_pool('redis://:123456@localhost/0?encoding=utf-8', maxsize=100)
    # Generate the schema
    await Tortoise.generate_schemas()


class MQ(Model):
    id = fields.IntField(pk=True)
    name = fields.TextField()

    # class Meta:
    #     table = 'cust_user'

    def __str__(self):
        return self.name


class Running(Model):
    """运行客户端 或 消费者"""
    name = fields.CharField(description=_("Alias"), max_length=100, blank=True, null=True, default='')
    mac_address = fields.CharField(description=_("User Mac"), max_length=255)
    host_ip = fields.CharField(description=_("Public IP"), max_length=128, blank=True, null=True)
    host_name = fields.CharField(description=_("Public IP"), max_length=128, blank=True, null=True)
    mode = fields.CharField(description=_('Mode'), max_length=12, default='ws')  # ws/loop ｜ 长链接或轮训
    ts = fields.FloatField(description=_("Alive Date"), default=time)

    class Meta:
        verbose_name_plural = verbose_name = _("Clients")

    def __str__(self):
        if self.name:
            return "{}({})".format(self.name, self.mac_address)
        else:
            return self.mac_address

    @property
    def alive_datetime(self):
        import time
        return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(float(self.ts)))


class TaskErrorLogs(Model):
    name = fields.CharField(description=_("Name"), max_length=100, blank=True, null=True, default='')
    client_ip = fields.CharField(description=_("Public IP"), max_length=128, blank=True, null=True)
    client_host_name = fields.CharField(description=_("Public IP"), max_length=128, blank=True, null=True)
    source_data = fields.TextField()
    source_code = fields.TextField()
    error_content = fields.TextField()
    ts = fields.FloatField(description=_("Running Date"), default=time)
