from src.utils.json_utils import json_loads
from src.utils.logging import log
from src.redis_store.utils import Redis
from src.db.helpers import get_service_resources
from src.config.base import BaseConfig
from src.constants.redis_keys import GPT_RESOURCE_CACHE_KEY, GPT_RESOURCE_INDEX_KEY


def get_llm_resource_round_robin(
    brand_id: int,
    brand_settings_id: int,
    resource_type: str,
    bot_db=None,
) -> dict:
    """
    Get LLM resource using round-robin selection.
    """
    cache_key = GPT_RESOURCE_CACHE_KEY.format(
        project_env=BaseConfig.APP_ENV,
        brand_id=brand_id,
        brand_settings_id=brand_settings_id,
    )

    index_key = GPT_RESOURCE_INDEX_KEY.format(
        GPT_RESOURCE_CACHE_KEY=cache_key,
    )

    log("resource_service.fetch", cache_key=cache_key, index_key=index_key)

    redis_client = Redis.get_redis_client()

    resources = Redis.get_value_from_redis(redis_client=redis_client, key= cache_key)
    index = Redis.get_value_from_redis(redis_client=redis_client, key= index_key)

    if not resources:
        log("resource_service.cache_miss", cache_key=cache_key, index_key=index_key)
        resources = []

        rows = get_service_resources(
            brand_id=brand_id,
            resource_type=resource_type,
            cursor=bot_db,
        )

        for row in rows:
            resources.append(dict(row))

        Redis.insert_into_redis(redis_client=redis_client, key=cache_key, data=resources, redis_expiry=900)
        Redis.insert_into_redis(redis_client=redis_client, key=index_key, data=0, redis_expiry=900)
        index = 0
    else:
        log("resource_service.cache_hit", cache_key=cache_key, index_key=index_key)
        resources = json_loads(resources)
        index = int(index or 0)

    if not resources:
        return {}

    resource = resources[index % len(resources)]
    next_index = (index + 1) % len(resources)

    Redis.insert_into_redis(redis_client=redis_client, key=index_key, data=next_index, redis_expiry=900)

    log(
        "resource_service.selected",
        resource_id=resource.get("id"),
        model=resource.get("model_name"),
    )

    return resource
