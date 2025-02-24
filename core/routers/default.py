import core.states as states

from aiogram import Router, types
from aiogram.filters.command import Command
from aiogram_dialog import DialogManager, StartMode

from core.routers.dialogs import router as dialogs_routers
from core.models import User

router = Router()
router.include_router(dialogs_routers)

@router.message(Command("start"))
async def start_dialog(message: types.Message, dialog_manager: DialogManager):
    user = message.from_user
    await User.get_or_create(
        tg_id=user.id,
        firstname=user.first_name,
        lastname=user.last_name,
        username=user.username
    )

    await dialog_manager.start(
        state=states.StartSG.view,
        mode=StartMode.RESET_STACK
    )

@router.message(Command("services"))
async def services_dialog(message: types.Message, dialog_manager: DialogManager):
    await dialog_manager.start(
        state=states.ServiceSG.view,
        mode=StartMode.RESET_STACK
    )

@router.message(Command("bookings"))
async def bookings_dialog(message: types.Message, dialog_manager: DialogManager):
    await dialog_manager.start(
        state=states.BookingViewSG.view,
        mode=StartMode.RESET_STACK,
    )

@router.message(Command("help"))
async def help_dialog(message: types.Message, dialog_manager: DialogManager):
    await dialog_manager.start(
        state=states.HelpSG.view,
        mode=StartMode.RESET_STACK
    )

