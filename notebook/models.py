from peewee import *
from datetime import date

db = SqliteDatabase('sqlite.db')

class Record(Model):
    name = CharField()
    phone = IntegerField()
    birthday = DateField()

    class Meta:
        database = db


#Record.create_table()
#Record.create(name='Falko Alexey', phone=9992097253, birthday=date(1935, 3, 25))
#Record.create(name='Raskin', phone=9992097253, birthday=date(1995, 4, 25))
#Record.create(name='Veselov', phone=9992097253, birthday=date(1994, 5, 25))