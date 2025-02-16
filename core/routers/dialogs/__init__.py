from aiogram import Router

from .service import dialog as service_dialog
from .booking import dialog as booking_dialog
from .start import dialog as start_dialog
from .help import dialog as help_dialog

router = Router()

router.include_routers(
    service_dialog,
    booking_dialog,
    start_dialog,
    help_dialog
)