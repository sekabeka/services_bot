import pytest

from datetime import datetime, date, time

from core.utils import Booking
from core.models import Record, Service


@pytest.mark.usefixtures("test_db")
class TestBooking:
    def test_get_available_bookings(self):
        test_date = date.today()
        service_test_data_1 = {
            "title": "service_test_1",
            "duration": 60,
            "price": 1000.0,
        }
        service_test_data_2 = {
            "title": "service_test_2",
            "duration": 90,
            "price": 1000.0,
        }
        service_test_data_3 = {
            "title": "service_test_3",
            "duration": 30,
            "price": 1000.0,
        }
        service1 = Service.create(**service_test_data_1)
        service2 = Service.create(**service_test_data_2)
        service3 = Service.create(**service_test_data_3)

        record_test_data_1 = {
            "client": 1,
            "service": service1,
            "date": datetime.combine(test_date, time(9, 0)),
        }
        record_test_data_2 = {
            "client": 1,
            "service": service2,
            "date": datetime.combine(test_date, time(13, 30)),
        }
        record_test_data_3 = {
            "client": 1,
            "service": service3,
            "date": datetime.combine(test_date, time(17, 30)),
        }
        record1 = Record.create(**record_test_data_1)
        record2 = Record.create(**record_test_data_2)
        record3 = Record.create(**record_test_data_3)

        booking_for_service_1 = Booking(test_date, record1.service.duration)
        available_bookings_for_service_1 = (
            booking_for_service_1.get_available_bookings()
        )
        expected_result_for_service_1 = [
            (
                datetime.combine(test_date, time(10, 0)),
                datetime.combine(test_date, time(11, 0)),
            ),
            (
                datetime.combine(test_date, time(11, 0)),
                datetime.combine(test_date, time(12, 0)),
            ),
            (
                datetime.combine(test_date, time(12, 0)),
                datetime.combine(test_date, time(13, 0)),
            ),
            (
                datetime.combine(test_date, time(15, 0)),
                datetime.combine(test_date, time(16, 0)),
            ),
            (
                datetime.combine(test_date, time(16, 0)),
                datetime.combine(test_date, time(17, 0)),
            ),
            (
                datetime.combine(test_date, time(18, 0)),
                datetime.combine(test_date, time(19, 0)),
            ),
            (
                datetime.combine(test_date, time(19, 0)),
                datetime.combine(test_date, time(20, 0)),
            ),
            (
                datetime.combine(test_date, time(20, 0)),
                datetime.combine(test_date, time(21, 0)),
            ),
        ]
        assert len(available_bookings_for_service_1) == len(
            expected_result_for_service_1
        )
        for i, (start, end) in enumerate(available_bookings_for_service_1):
            assert start == expected_result_for_service_1[i][0]
            assert end == expected_result_for_service_1[i][1]

        booking_for_service_2 = Booking(test_date, record2.service.duration)
        available_bookings_for_service_2 = (
            booking_for_service_2.get_available_bookings()
        )
        expected_result_for_service_2 = [
            (
                datetime.combine(test_date, time(10, 0)),
                datetime.combine(test_date, time(11, 30)),
            ),
            (
                datetime.combine(test_date, time(11, 30)),
                datetime.combine(test_date, time(13, 0)),
            ),
            (
                datetime.combine(test_date, time(15, 0)),
                datetime.combine(test_date, time(16, 30)),
            ),
            (
                datetime.combine(test_date, time(18, 0)),
                datetime.combine(test_date, time(19, 30)),
            ),
            (
                datetime.combine(test_date, time(19, 30)),
                datetime.combine(test_date, time(21, 0)),
            ),
        ]
        assert len(available_bookings_for_service_2) == len(
            expected_result_for_service_2
        )
        for i, (start, end) in enumerate(available_bookings_for_service_2):
            assert start == expected_result_for_service_2[i][0]
            assert end == expected_result_for_service_2[i][1]

        booking_for_service_3 = Booking(test_date, record3.service.duration)
        available_bookings_for_service_3 = (
            booking_for_service_3.get_available_bookings()
        )
        expected_result_for_service_3 = [
            (
                datetime.combine(test_date, time(10, 0)),
                datetime.combine(test_date, time(10, 30)),
            ),
            (
                datetime.combine(test_date, time(10, 30)),
                datetime.combine(test_date, time(11, 0)),
            ),
            (
                datetime.combine(test_date, time(11, 0)),
                datetime.combine(test_date, time(11, 30)),
            ),
            (
                datetime.combine(test_date, time(11, 30)),
                datetime.combine(test_date, time(12, 0)),
            ),
            (
                datetime.combine(test_date, time(12, 0)),
                datetime.combine(test_date, time(12, 30)),
            ),
            (
                datetime.combine(test_date, time(12, 30)),
                datetime.combine(test_date, time(13, 0)),
            ),
            (
                datetime.combine(test_date, time(13, 0)),
                datetime.combine(test_date, time(13, 30)),
            ),
            (
                datetime.combine(test_date, time(15, 0)),
                datetime.combine(test_date, time(15, 30)),
            ),
            (
                datetime.combine(test_date, time(15, 30)),
                datetime.combine(test_date, time(16, 0)),
            ),
            (
                datetime.combine(test_date, time(16, 0)),
                datetime.combine(test_date, time(16, 30)),
            ),
            (
                datetime.combine(test_date, time(16, 30)),
                datetime.combine(test_date, time(17, 0)),
            ),
            (
                datetime.combine(test_date, time(17, 0)),
                datetime.combine(test_date, time(17, 30)),
            ),
            (
                datetime.combine(test_date, time(18, 0)),
                datetime.combine(test_date, time(18, 30)),
            ),
            (
                datetime.combine(test_date, time(18, 30)),
                datetime.combine(test_date, time(19, 0)),
            ),
            (
                datetime.combine(test_date, time(19, 0)),
                datetime.combine(test_date, time(19, 30)),
            ),
            (
                datetime.combine(test_date, time(19, 30)),
                datetime.combine(test_date, time(20, 0)),
            ),
            (
                datetime.combine(test_date, time(20, 0)),
                datetime.combine(test_date, time(20, 30)),
            ),
            (
                datetime.combine(test_date, time(20, 30)),
                datetime.combine(test_date, time(21, 00)),
            ),
        ]
        assert len(available_bookings_for_service_3) == len(
            expected_result_for_service_3
        )
        for i, (start, end) in enumerate(available_bookings_for_service_3):
            assert start == expected_result_for_service_3[i][0]
            assert end == expected_result_for_service_3[i][1]
