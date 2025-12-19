from redis.asyncio import from_url

from src.core.config import settings

redis_client = from_url(url=settings.REDIS_DSN, encoding="utf-8", decode_responses=True)
