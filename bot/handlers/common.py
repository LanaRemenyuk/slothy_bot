from aiogram import Router

from . import (find_service, offer_service, start, help_command,
                support_command, my_offers)

router = Router()

router.include_router(start.router)
router.include_router(offer_service.router)
router.include_router(find_service.router)
router.include_router(help_command.router)
router.include_router(support_command.router)
router.include_router(my_offers.router)