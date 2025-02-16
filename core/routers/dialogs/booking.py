import core.states as states

from aiogram import F
from aiogram_dialog import Dialog, Window, DialogManager
from aiogram_dialog.widgets.text import (
    Const,
    Format,
    Multi,
    List, Jinja,
)
from aiogram_dialog.widgets.kbd import (
    Row,
    NextPage,
    PrevPage,
)

from core.buttons import BUTTON_TO_MENU
from core.database import get_records_for_owner, get_records_for_user
from core.utils import is_owner
from core.templates import NO_BOOKINGS_TEMPLATE, BOOKINGS_TEMPLATE

async def getter_bookings(**kwargs):
    dialog_manager: DialogManager = kwargs.get("dialog_manager")
    user_id = dialog_manager.event.from_user.id
    data = {}
    if is_owner(user_id):
        data["bookings"] = get_records_for_owner()
    else:
        data["bookings"] = get_records_for_user(user_id)
    return data

dialog = Dialog(
    Window(
        List(
            Jinja(
                text=BOOKINGS_TEMPLATE,
            ),
            items="bookings",
            page_size=1,
            id="list_scroll",
            when=F["bookings"]
        ),
        Jinja(
            NO_BOOKINGS_TEMPLATE,
            when=~F["bookings"]
        ),
        Row(
            PrevPage(scroll="list_scroll", text=Const("⬅️")),
            NextPage(scroll="list_scroll", text=Const("➡️")),
            when=F["bookings"]
        ),
        BUTTON_TO_MENU,
        getter=getter_bookings,
        state=states.BookingViewSG.view,
        parse_mode="HTML"
    ),
)
