import os
from typing import List

import asyncpg
from dotenv import load_dotenv

from models.service import ServiceOffer

load_dotenv()

async def save_to_db(data: dict):
    conn = await asyncpg.connect(
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASSWORD'),
        database=os.getenv('DB_NAME'),
        host=os.getenv('DB_HOST', 'localhost'),
        port=os.getenv('DB_PORT', '5432')
    )
    
    try:
        await conn.execute('''
            INSERT INTO service_offers (
                telegram_id, telegram_nick, phone, 
                full_name, service_type, experience, description
            ) VALUES ($1, $2, $3, $4, $5, $6, $7)
        ''', 
            data['telegram_id'],
            data['telegram_nick'],
            data['phone'],
            data['full_name'],
            data['service_type'],
            data['experience'],
            data['description']
        )
    finally:
        await conn.close()