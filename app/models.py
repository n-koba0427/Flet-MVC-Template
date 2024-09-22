from peewee import *

db = SqliteDatabase('database/fletmvc.db')

class BaseModel(Model):
    class Meta:
        database = db

class User(BaseModel):
    username = CharField(unique=True)
    password = CharField()
    
class Task(BaseModel):
    title = CharField(100)
    description = CharField(255)
    is_done = BooleanField(default=False)
    created_by = ForeignKeyField(User, backref='tasks')

db.connect()
db.create_tables([User, Task])