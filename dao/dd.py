from tortoise import Model, fields

"""数据库当中的表"""


class dd(Model):
    id = fields.IntField(pk=True)
    content = fields.CharField(max_length=500)
    created = fields.DatetimeField(auto_now_add=True)
    updated = fields.DatetimeField(auto_now=True)
