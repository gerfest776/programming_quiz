import aioredis

from app.config import get_config

redis = aioredis.from_url(get_config().redis.REDIS_URI)
