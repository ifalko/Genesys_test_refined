from peewee import *

db = SqliteDatabase('sqlite.db')

class Record(Model):
    name = CharField()
    phone = IntegerField()
    birthday = DateField(null=True)

    class Meta:
        database = db      