import os

import asyncpg
from dotenv import load_dotenv

load_dotenv()

class Database:
    _pool = None
    
    @classmethod
    async def get_pool(cls):
        if cls._pool is None:
            cls._pool = await asyncpg.create_pool(
                user=os.getenv('DB_USER'),
                password=os.getenv('DB_PASSWORD'),
                database=os.getenv('DB_NAME'),
                host=os.getenv('DB_HOST', 'localhost'),
                port=os.getenv('DB_PORT', '5432'),
                min_size=1,
                max_size=10
            )
        return cls._pool
    
    @classmethod
    async def close_pool(cls):
        if cls._pool is not None:
            await cls._pool.close()
            cls._pool = None