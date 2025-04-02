from aiogram import Router

from . import find_service, offer_service, start

router = Router()

router.include_router(start.router)
router.include_router(offer_service.router)
router.include_router(find_service.router)