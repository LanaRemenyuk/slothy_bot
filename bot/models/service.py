from dataclasses import dataclass

@dataclass
class ServiceOffer:
    telegram_id: int
    telegram_nick: str
    phone: str
    full_name: str
    service_type: list
    experience: int
    description: str