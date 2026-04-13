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
        table = "user"

class Category(Model):
    id = fields.IntField(pk=True)
    user = fields.ForeignKeyField('models.User', related_name='categories', on_delete=fields.CASCADE)
    category_id = fields.IntField(validators=[MinValueValidator(1), MaxValueValidator(24)])
    category_name = fields.CharField(max_length=6, validators=[MaxLengthValidator(6)])
    class Meta:
        table = "categories"