import core.states as states

from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.text import (
    Jinja
)

from core.buttons import BUTTON_TO_MENU
from core.templates import HELP_TEMPLATE

dialog = Dialog(
    Window(
        Jinja(HELP_TEMPLATE),
        BUTTON_TO_MENU,
        state=states.HelpSG.view,
        parse_mode="HTML"
    )
)