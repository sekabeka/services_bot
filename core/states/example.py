from aiogram.filters.state import State, StatesGroup

class ExampleSG(StatesGroup):
    about = State()
    notify_for_user = State()
    notify_for_employee = State()
    notify_for_employee_morning = State()