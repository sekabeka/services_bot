import core.states as states

from aiogram_dialog.widgets.text import Const
from aiogram_dialog.widgets.kbd import Start, Back, Next

BUTTON_TO_MENU = Start(
    text=Const("К меню"),
    id="go_to_menu",
    state=states.StartSG.view
)
BUTTON_TO_SERVICES = Start(
    text=Const("К услугам"),
    id="go_to_services",
    state=states.ServiceSG.view
)
BUTTON_TO_BOOKINGS = Start(
    text=Const("К бронированиями"),
    id="go_to_bookings",
    state=states.BookingViewSG.view
)
BUTTON_TO_BACK = Back(
    text=Const("Назад")
)
BUTTON_TO_HELP = Start(
    text=Const("Помощь"),
    id="go_to_help",
    state=states.HelpSG.view
)
BUTTON_TO_EXAMPLES = Start(
    text=Const("Уведомления"),
    id="go_to_notify",
    state=states.ExampleSG.about
)