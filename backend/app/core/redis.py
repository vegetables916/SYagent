import redis
from app.core.config import settings

# Redis 客户端（同步版本，用于限流等场景）
redis_client = redis.Redis(
    host=settings.REDIS_HOST,
    port=settings.REDIS_PORT,
    db=settings.REDIS_DB,
    decode_responses=True
)


def get_redis() -> redis.Redis:
    """获取 Redis 客户端"""
    return redis_client
