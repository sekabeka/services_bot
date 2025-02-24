import core.states as states

from aiogram import F
from aiogram_dialog import Dialog, Window, DialogManager
from aiogram_dialog.widgets.text import (
    Const,
    List, Jinja,
)
from aiogram_dialog.widgets.kbd import (
    Row,
    NextPage,
    PrevPage,
)

from core.buttons import BUTTON_TO_MENU
from core.templates import NO_BOOKINGS_TEMPLATE, BOOKINGS_TEMPLATE
from core.utils import fetch_bookings

async def getter_bookings(**kwargs):
    dialog_manager: DialogManager = kwargs.get("dialog_manager")
    user_id = dialog_manager.event.from_user.id
    bookings = await fetch_bookings(user_id)
    return {
        "bookings": bookings
    }

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
