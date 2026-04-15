# app/models/models.py
from tortoise.models import Model
from tortoise import fields
from tortoise.validators import MinValueValidator, MaxValueValidator, MaxLengthValidator


class User(Model):
    id= fields.UUIDField(primary_key=True) 
    username= fields.CharField(max_length=64, unique=True)
    password= fields.CharField(max_length=128)
    email= fields.CharField(max_length=255, unique=True)
    phone= fields.CharField(max_length=16, unique=True, null=True)
    class Meta:
        table = "users"

class Category(Model):
    id = fields.IntField(pk=True)
    user = fields.ForeignKeyField('models.User', related_name='categories', on_delete=fields.CASCADE)
    category_id = fields.IntField(validators=[MinValueValidator(1), MaxValueValidator(24)])
    category_name = fields.CharField(max_length=6, validators=[MaxLengthValidator(6)])
    class Meta:
        table = "categories"

class Note(Model):
    id = fields.IntField(pk=True, generated=True, description="笔记ID")
    user = fields.ForeignKeyField(
        "models.User",
        related_name="notes",
        on_delete=fields.CASCADE,
        description="所属用户",
    )
    category = fields.ForeignKeyField(
        "models.Category",
        related_name="notes",
        on_delete=fields.SET_NULL,
        null=True,
        description="所属分类",
    )
    title = fields.CharField(max_length=255, description="笔记标题")
    content = fields.TextField(description="笔记内容")
    category_name = fields.CharField(max_length=6, null=True, description="分类名称")
    tags = fields.JSONField(default=list, description="标签列表")
    starred = fields.BooleanField(default=False, description="是否星标")
    created_at = fields.DatetimeField(auto_now_add=True, description="创建时间")
    updated_at = fields.DatetimeField(auto_now=True, description="更新时间")

    class Meta:
        table = "notes"
        ordering = ["-updated_at"]
        description = "笔记表"