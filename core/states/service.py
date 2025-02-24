from aiogram.filters.state import State, StatesGroup

class ServiceSG(StatesGroup):
    view = State()
    booking = State()
    booking_staff = State()
    booking_detail = State()
    booking_confirm = State()
    booking_complete = State()