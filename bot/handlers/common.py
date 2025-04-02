from aiogram import Router
from . import start, offer_service, find_service

router = Router()

router.include_router(start.router)
router.include_router(offer_service.router)
router.include_router(find_service.router)