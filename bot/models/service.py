from dataclasses import dataclass
from datetime import datetime


@dataclass
class ServiceOffer:
    id: int
    telegram_id: int
    telegram_nick: str
    phone: str
    full_name: str
    service_type: list
    experience: int
    description: str
    created_at: datetime