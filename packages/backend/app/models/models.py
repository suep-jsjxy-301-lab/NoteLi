# app/models/models.py
from tortoise.models import Model
from tortoise import fields


class User(Model):
    id= fields.UUIDField(primary_key=True) 
    username= fields.CharField(max_length=64, unique=True)
    password= fields.CharField(max_length=128)
    role= fields.CharField(max_length=32, default="user")
