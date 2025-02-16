from datetime import datetime, timedelta

from core.models import Record, Service

class UserFunc:
    def __init__(self, event):
        self.user_id = event.from_user.id
        self.is_owner = self.is_owner()

    def is_owner(self):
        return self.user_id == 22222

def get_records_for_notifications():
    now = datetime.now()
    return Record.select().where(
        (Record.date > now)
        & (Record.date <= now + timedelta(days=1))
        & (Record.notified == False)
    )

def get_records_for_user(user_id):
    return (
        Record
        .select()
        .join(Service)
        .where(
            (Record.client == user_id) &
            (Record.date >= datetime.now())
        )
        .order_by(Record.date.asc())
    )

def get_records_for_owner():
    return (
        Record
        .select()
        .where(Record.date >= datetime.now())
        .order_by(Record.date.asc())
    )


def get_records_on_date(date=datetime.today()):
    return (
        Record
        .select()
        .join(Service)
        .where(
            (Record.date.month == date.month)
            & (Record.date.day == date.day)
            & (Record.date.year == date.year)
        )
        .order_by(Record.date.asc())
    )

