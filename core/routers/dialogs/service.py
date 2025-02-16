import operator
import core.states as states

from aiogram import F, types
from datetime import date, datetime

from aiogram_dialog import Dialog, Window, DialogManager
from aiogram_dialog.widgets.text import (
    Const,
    Format,
    Multi,
    List, Jinja,
)
from aiogram_dialog.widgets.kbd import (
    Button,
    Calendar,
    CalendarConfig,
    Select,
    Row,
    Group,
    NextPage,
    PrevPage,
    SwitchTo,
)
from core.models import Service, Record
from core.utils import Booking
from core.celery_app.tasks import send_to_owner
from core.buttons import BUTTON_TO_MENU, BUTTON_TO_SERVICES, BUTTON_TO_BACK
from core.templates import (
    SERVICE_TEMPLATE_LIST,
    SERVICE_TEMPLATE_DATE,
    SERVICE_TEMPLATE_TIME,
    SERVICE_TEMPLATE_CONFIRM,
    SERVICE_TEMPLATE_COMPLETE
)



calendar_config = CalendarConfig(
    min_date=date.today(),
    max_date=date(date.today().year + 1, 12, 30),
    years_per_page=2,
)


async def getter_services_list(**kwargs):
    return {"services": Service.select()}


async def getter_free_intervals(dialog_manager: DialogManager, **kwargs):
    return {"intervals": dialog_manager.dialog_data["intervals"]}


async def on_click_booking_service(
    callback: types.CallbackQuery, button: Button, dialog_manager: DialogManager
):
    page = await dialog_manager.find("list_scroll").get_page()
    service = list(Service.select())[page]
    dialog_manager.dialog_data["service"] = service


async def on_click_date_selected(
    callback: types.CallbackQuery, widget, manager: DialogManager, selected_date: date
):
    service = manager.dialog_data["service"]
    duration = service.duration
    booking = Booking(selected_date, duration)
    manager.dialog_data["selected_date"] = selected_date
    free_intervals = booking.get_available_bookings()
    intervals = []
    for i, (start, end) in enumerate(free_intervals):
        _start = start.time().strftime("%H:%M")
        end = end.time().strftime("%H:%M")
        intervals.append((f"{_start}-{end}", i, start.time()))
    manager.dialog_data["intervals"] = intervals
    await manager.switch_to(states.ServiceSG.booking_detail)


async def on_click_to_confirm(
    callback: types.CallbackQuery, widget, manager: DialogManager, item_id: str
):
    manager.dialog_data["selected_time"] = manager.dialog_data["intervals"][
        int(item_id)
    ][-1]
    await manager.switch_to(states.ServiceSG.booking_confirm)


async def on_click_save_booking(
    callback: types.CallbackQuery, button: Button, dialog_manager: DialogManager
):
    service = dialog_manager.dialog_data["service"]
    selected_time = dialog_manager.dialog_data["selected_time"]
    selected_date = dialog_manager.dialog_data["selected_date"]
    user = dialog_manager.event.from_user
    record = Record.create(
        service=service,
        client=user.id,
        date=datetime.combine(selected_date, selected_time),
    )
    dialog_manager.dialog_data["record"] = record
    await dialog_manager.switch_to(states.ServiceSG.booking_complete)
    send_to_owner.delay(
        id=record.id,
        title=record.service.title,
        date=record.date
    )


dialog = Dialog(
    Window(
        List(
            Jinja(
                text=SERVICE_TEMPLATE_LIST
            ),
            items="services",
            page_size=1,
            id="list_scroll",
        ),
        Row(
            PrevPage(scroll="list_scroll", text=Const("⬅️")),
            NextPage(scroll="list_scroll", text=Const("➡️")),
        ),
        SwitchTo(
            text=Const("Записаться"),
            id="service_booking",
            state=states.ServiceSG.booking,
            on_click=on_click_booking_service,
        ),
        BUTTON_TO_MENU,
        getter=getter_services_list,
        state=states.ServiceSG.view,
        parse_mode="HTML",
    ),
    Window(
        Jinja(
            text=SERVICE_TEMPLATE_DATE,
        ),
        Calendar(
            id="calendar", on_click=on_click_date_selected, config=calendar_config
        ),
        BUTTON_TO_BACK,
        state=states.ServiceSG.booking,
        parse_mode="HTML"
    ),
    Window(
        Jinja(
            text=SERVICE_TEMPLATE_TIME,
            when=F["intervals"]
        ),
        Group(
            Select(
                text=Format("{item[0]}"),
                id="select_booking_intervals",
                items="intervals",
                item_id_getter=operator.itemgetter(1),
                on_click=on_click_to_confirm,
            ),
            width=3,
            when=F["intervals"],
        ),
        Const(
            text="К сожалению, свободного времени на эту дату нет.",
            when=~F["intervals"],
        ),
        BUTTON_TO_BACK,
        state=states.ServiceSG.booking_detail,
        getter=getter_free_intervals,
        parse_mode="HTML"
    ),
    Window(
        Jinja(
            text=SERVICE_TEMPLATE_CONFIRM
        ),
        Button(
            text=Const("Подтвердить"),
            id="confirm_booking",
            on_click=on_click_save_booking,
        ),
        BUTTON_TO_BACK,
        state=states.ServiceSG.booking_confirm,
        parse_mode="HTML"
    ),
    Window(
        Jinja(
            text=SERVICE_TEMPLATE_COMPLETE
        ),
        BUTTON_TO_MENU,
        BUTTON_TO_SERVICES,
        state=states.ServiceSG.booking_complete,
        parse_mode="HTML"
    ),
)
