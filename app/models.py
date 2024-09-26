from peewee import SqliteDatabase, Model, CharField, BooleanField, ForeignKeyField

db = SqliteDatabase('database/fletmvc.db')

# Models Module
#
# This module defines the data models for the application using Peewee ORM.
# Each model typically represents a table in the database.
#
# Key Components:
#
# - BaseModel:
#   A base class for all models, providing common functionality and database connection.
#
# - User:
#   A sample model representing user data.
#
# - Task:
#   A sample model representing task data, with a foreign key to User.
#
# Custom Models:
# To add a new model, follow this pattern:
#
# class YourModel(BaseModel):
#     field1 = CharField()
#     field2 = IntegerField()
#     # Add more fields as needed
#
# Remember to add your new model to the create_tables() call at the end of this file.

class BaseModel(Model):
    class Meta:
        database = db

class User(BaseModel):
    username = CharField(unique=True)
    password = CharField()
    salt = CharField()
    
class Task(BaseModel):
    title = CharField(100)
    description = CharField(255)
    is_done = BooleanField(default=False)
    created_by = ForeignKeyField(User, backref='tasks')

class Summoner(BaseModel):
    region = CharField()
    summoner_name = CharField()
    tag = CharField()
    player_icon = CharField()
    rank = CharField()
    lp = CharField()
    score = CharField()
    is_active = BooleanField(default=True)
    
db.connect()
db.create_tables([User, Task, Summoner])