import settings

from intervaltree import IntervalTree, Interval
from datetime import timedelta, datetime, date, time

from settings import START_TIME_OF_WORK, END_TIME_OF_WORK
from core.database import get_records_on_date


class Booking:
    def __init__(self, booking_date: date, duration: int):
        self.booking_date = booking_date
        self.duration = duration

    def get_available_bookings(
        self,
        start_time_of_work: time = START_TIME_OF_WORK,
        end_time_of_work: time = END_TIME_OF_WORK,
    ):
        start = datetime.combine(self.booking_date, start_time_of_work)
        end = datetime.combine(self.booking_date, end_time_of_work)

        occupied_tree = IntervalTree()

        records = get_records_on_date(self.booking_date)
        for record in records:
            occupied_tree.add(
                Interval(
                    record.date.timestamp(),
                    (
                        record.date + timedelta(minutes=record.service.duration)
                    ).timestamp(),
                )
            )

        free_bookings = []
        current_start = start.timestamp()
        end_timestamp = end.timestamp()
        duration_seconds = self.duration * 60
        while current_start + duration_seconds <= end_timestamp:
            current_end = current_start + duration_seconds
            overlapping_intervals = occupied_tree.overlap(current_start, current_end)
            if not overlapping_intervals:
                free_bookings.append(
                    (
                        datetime.fromtimestamp(current_start),
                        datetime.fromtimestamp(current_end),
                    )
                )
                current_start += duration_seconds
            else:
                last_end = max(interval.end for interval in overlapping_intervals)
                current_start = last_end

        return free_bookings

def is_owner(user_id):
    return user_id in [settings.OWNER]
