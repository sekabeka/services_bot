import peewee
import settings

database = peewee.PostgresqlDatabase(
    **settings.DATABASE
)

class BaseModel(peewee.Model):
    class Meta:
        database = database

class Service(BaseModel):
    title = peewee.CharField(max_length=128)
    duration = peewee.IntegerField()
    price = peewee.DecimalField(10, 2)
    description = peewee.TextField(null=True)

class Record(BaseModel):
    client = peewee.BigIntegerField()
    service = peewee.ForeignKeyField(Service, backref='records', on_delete="RESTRICT")
    date = peewee.DateTimeField()
    notified = peewee.BooleanField(default=False)

database.create_tables([
    Service,
    Record
], safe=True)