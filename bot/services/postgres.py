import uuid

from typing import Dict, List, Optional

import asyncpg

from .base import Database
from models.service import ServiceOffer

async def save_to_db(data: dict):
    pool = await Database.get_pool()
    async with pool.acquire() as conn:
        offer_id = str(uuid.uuid4())
        await conn.execute('''
            INSERT INTO service_offers (
                id, telegram_id, telegram_nick, phone, 
                full_name, service_type, experience, description
            ) VALUES ($1, $2, $3, $4, $5, $6, $7, $8)
        ''', 
            offer_id,
            data['telegram_id'],
            data['telegram_nick'],
            data['phone'],
            data['full_name'],
            data['service_type'],
            data['experience'],
            data['description']
        )


async def get_popular_tags(limit: int = 15) -> List[str]:
    """Получаем самые популярные теги из БД"""
    pool = await Database.get_pool()
    async with pool.acquire() as conn:
        records = await conn.fetch('''
            SELECT tag, COUNT(*) AS count
            FROM (
              SELECT unnest(service_type) as tag
              FROM service_offers
            ) AS t
            GROUP BY tag
            ORDER BY count DESC
            LIMIT $1
        ''', limit)
        return [r['tag'] for r in records]


async def check_tag_exists(tag: str) -> bool:
    """Проверяем существование тега в БД"""
    pool = await Database.get_pool()
    async with pool.acquire() as conn:
        return await conn.fetchval("""
            SELECT EXISTS(
                SELECT 1 FROM serice_offers
                WHERE $1 = ANY(service_type)
                LIMIT 1
            )
        """, tag)
    

async def get_offers_by_tag(tag: str) -> List[ServiceOffer]:
    """Получаем все объявления с указанным тегом"""
    pool = await Database.get_pool()
    async with pool.acquire() as conn:
        records = await conn.fetch("""
          SELECT * FROM service_offers
          WHERE $1 = ANY(service_type)
        """, tag)
        return [ServiceOffer(**r) for r in records]
    

async def get_user_offers(user_id: int) -> list[dict]:
    """Получение всех объявлений пользователя из БД"""
    pool = await Database.get_pool()
    query = "SELECT * FROM service_offers WHERE telegram_id = $1 ORDER BY created_at DESC"
    async with pool.acquire() as conn:
        return await conn.fetch(query, user_id)
    

async def get_offer_by_id(offer_id: uuid.UUID) -> Optional[Dict]:
    """Получение объявления по ID"""
    pool = await Database.get_pool()
    query = "SELECT * FROM service_offers WHERE id = $1"
    async with pool.acquire() as conn:
        return await conn.fetchrow(query, offer_id)
    

async def delete_offer_by_id(offer_id: uuid.UUID) -> bool:
    """Удаление объявления по ID"""
    pool = await Database.get_pool()
    query = "DELETE FROM service_offers WHERE id = $1"
    async with pool.acquire() as conn:
        await conn.execute(query, offer_id)
    return True