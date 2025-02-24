import core.states as states

from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.kbd import (
    Group
)
from aiogram_dialog.widgets.text import (
    Jinja
)

from core.buttons import BUTTON_TO_SERVICES, BUTTON_TO_BOOKINGS, BUTTON_TO_HELP, BUTTON_TO_EXAMPLES
from core.templates import START_TEMPLATE

dialog = Dialog(
    Window(
        Jinja(START_TEMPLATE),
        Group(
            BUTTON_TO_SERVICES,
            BUTTON_TO_BOOKINGS,
            BUTTON_TO_HELP,
            BUTTON_TO_EXAMPLES,
            width=2
        ),
        state=states.StartSG.view,
        parse_mode="HTML"
    )
)