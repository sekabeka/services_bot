import pytest

from datetime import datetime, timedelta

from core.models import Record, Service
from core.database import get_records_on_date, get_records_for_notifications


@pytest.mark.usefixtures("test_db")
class TestDB:
    def test_get_records_for_notifications(self):
        service = Service.create(title="test_service", duration=60, price=1000)
        record1 = Record.create(
            service=service, client=1, date=datetime.now() + timedelta(hours=4)
        )
        record2 = Record.create(
            service=service, client=2, date=datetime.now() + timedelta(days=2)
        )
        record3 = Record.create(
            service=service, client=3, date=datetime.now() - timedelta(hours=1)
        )
        record4 = Record.create(
            service=service,
            client=4,
            date=datetime.now() + timedelta(hours=3),
            notified=True,
        )
        expected_records = [record1]
        result_records = get_records_for_notifications()
        assert expected_records == result_records

        record5 = Record.create(
            service=service, client=3, date=datetime.now() + timedelta(hours=5)
        )
        result_records = get_records_for_notifications()
        assert len(result_records) == 2
        assert record5 in list(result_records)
