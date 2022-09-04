import json

import aioredis
from fastapi import HTTPException

from app.config import get_config

redis = aioredis.from_url(get_config().redis.REDIS_URI)


async def check_token(token: str):
    token_data = await redis.get(token)
    if token_data is None:
        raise HTTPException(status_code=400, detail="Token not valid")
    return json.loads(token_data)
