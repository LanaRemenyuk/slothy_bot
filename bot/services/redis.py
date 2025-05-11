import json
import logging
import random
from datetime import datetime
from typing import Any, Dict, Optional
from redis.asyncio import Redis

logger = logging.getLogger(__name__)

class RedisSessionManager:
    def __init__(self, redis_client: Redis, session_ttl: int = 3600):
        self.redis = redis_client
        self.session_ttl = session_ttl

    async def session_exists(self, user_id: int, tag: str) -> bool:
        session = await self.get_session(user_id)
        return bool(session and session.get('tag') == tag)

    async def init_session(self, user_id: int, tag: str, offers: list) -> bool:
        try:
            session_data = {
                'tag': tag,
                'all_offers': [self._serialize_offer(of) for of in offers],
                'current_idx': 0
            }
            await self._save_session(user_id, session_data)
            return True
        except Exception as e:
            logger.error(f'Error initializing session {e}')
            return False

    async def get_current_offer(self, user_id: int, tag: str) -> Optional[Dict[str, Any]]:
        session = await self.get_session(user_id)
        if not session or session.get('tag') != tag:
            return None
        return session['all_offers'][session['current_idx']]

    async def get_current_index(self, user_id: int, tag: str) -> int:
        session = await self.get_session(user_id)
        if not session or session.get('tag') != tag:
            return -1
        return session['current_idx']

    async def get_total_offers(self, user_id: int, tag: str) -> int:
        session = await self.get_session(user_id)
        if not session or session.get('tag') != tag:
            return 0
        return len(session['all_offers'])

    async def increment_index(self, user_id: int, tag: str) -> None:
        session = await self.get_session(user_id)
        if session and session.get('tag') == tag:
            if session['current_idx'] < len(session['all_offers']) - 1:
                session['current_idx'] += 1
                await self._save_session(user_id, session)

    async def decrement_index(self, user_id: int, tag: str) -> None:
        session = await self.get_session(user_id)
        if session and session.get('tag') == tag:
            if session['current_idx'] > 0:
                session['current_idx'] -= 1
                await self._save_session(user_id, session)

    async def get_active_tag(self, user_id: int) -> Optional[str]:
        session = await self.get_session(user_id)
        return session.get('tag') if session else None

    async def get_session(self, user_id: int) -> Optional[Dict[str, Any]]:
        try:
            session_data = await self.redis.get(f'user:{user_id}:search_session')
            return json.loads(session_data) if session_data else None
        except Exception as e:
            logger.error(f'Error getting session for user {user_id}: {e}')
            return None

    async def _save_session(self, user_id: int, session_data: Dict[str, Any]):
        await self.redis.setex(
            f'user:{user_id}:search_session',
            self.session_ttl,
            json.dumps(session_data)
            )
    
    @staticmethod
    def _serialize_offer(offer) -> Dict[str, Any]:
        if isinstance(offer, dict):
            return offer
        elif hasattr(offer, 'to_dict'):
            return offer.to_dict()
        elif hasattr(offer, '__dict__'):
            result = offer.__dict__.copy()
            if 'created_at' in result and isinstance(result['created_at'], datetime):
                result['created_at'] = result['created_at'].isoformat()
            return result
        raise ValueError('Unsupported offer type')