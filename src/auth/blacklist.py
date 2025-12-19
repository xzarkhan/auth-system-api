from datetime import datetime, timezone

from src.core.redis import redis_client


class TokensRedisBlacklist:
    PREFIX = "auth:blacklist:"

    def __get_key(self, jti: str) -> str:
        return f"{self.PREFIX}{jti}"

    async def revoke_token(self, jti: str, expire_at: int) -> None:
        ttl = expire_at - int(datetime.now(timezone.utc).timestamp())
        if ttl <= 0:
            return
        key = self.__get_key(jti=jti)
        await redis_client.setex(name=key, value="1", time=ttl)

    async def is_revoked(self, jti: str) -> bool:
        key = self.__get_key(jti=jti)
        is_revoked = await redis_client.get(name=key) is not None
        return is_revoked
