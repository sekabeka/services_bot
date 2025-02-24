from datetime import datetime, timedelta

from random import choice

import core.states as states

from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.text import (
    Const,
    Jinja
)
from aiogram_dialog.widgets.kbd import (
    Group, SwitchTo
)

from core.buttons import BUTTON_TO_MENU, BUTTON_TO_EXAMPLES
from core.templates import (
    NOTIFY_TEMPLATE_FOR_USER,
    NOTIFY_TEMPLATE_FOR_EMPLOYEE_MORNING,
    NOTIFY_TEMPLATE_FOR_EMPLOYEE
)

async def getter_morning_employee(**kwargs):
    bookings = [
        {"date" : (datetime.now() + timedelta(hours=i)).replace(second=0, microsecond=0, minute=30)}
        for i in range (5)
    ]
    return {
        "bookings": bookings
    }

ABOUT_TEMPLATE = """
Здесь Вы можете посмотреть шаблоны уведомлений, которые включены в бота 📋

Реализованы 3 типа уведомлений:
- для мастера после записи клиента
- для мастера каждое утро в 9 часов
- для клиента, когда до записи остается меньше 24 часов

Ниже Вы можете выбрать интересующий Вас пример ✏️
"""

dialog = Dialog(
    Window(
        Jinja(
            ABOUT_TEMPLATE
        ),
        BUTTON_TO_MENU,
        Group(
            SwitchTo(
                text=Const("Утро"),
                id="morning_notify",
                state=states.ExampleSG.notify_for_employee_morning
            ),
            SwitchTo(
                text=Const("После бронирования"),
                id="after_booking_notify",
                state=states.ExampleSG.notify_for_employee
            ),
            SwitchTo(
                text=Const("Для клиента"),
                id="user_notify",
                state=states.ExampleSG.notify_for_user
            ),
            width=2
        ),
        state=states.ExampleSG.about,
        parse_mode="HTML"
    ),
    Window(
        Jinja(
            NOTIFY_TEMPLATE_FOR_EMPLOYEE_MORNING
        ),
        BUTTON_TO_MENU,
        BUTTON_TO_EXAMPLES,
        getter=getter_morning_employee,
        state=states.ExampleSG.notify_for_employee_morning,
        parse_mode="HTML"
    ),
    Window(
        Jinja(
            NOTIFY_TEMPLATE_FOR_EMPLOYEE.format(
                id=87,
                title="Чистка лица",
                date=(datetime.now() + timedelta(days=10)) \
                    .replace(
                        hour=10,
                        minute=30,
                        second=0,
                        microsecond=0
                    )

            )
        ),
        BUTTON_TO_MENU,
        BUTTON_TO_EXAMPLES,
        state=states.ExampleSG.notify_for_employee,
        parse_mode="HTML"
    ),
    Window(
        Jinja(
            NOTIFY_TEMPLATE_FOR_USER.format(
                id = 87,
                title="Чистка лица",
                date=(datetime.now() + timedelta(hours=choice(range(1, 20)))) \
                .replace(
                    second=30,
                    microsecond=0,
                    minute=45
                )
            )
        ),
        BUTTON_TO_MENU,
        BUTTON_TO_EXAMPLES,
        state=states.ExampleSG.notify_for_user,
        parse_mode="HTML"
    ),
)

