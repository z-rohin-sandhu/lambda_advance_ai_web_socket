from src.redis_store.utils import Redis
from src.utils.logging import log
from src.config.base import BaseConfig

def check_token_blacklisted_status(token: str="", redis_client= None) -> bool:
    try:
        env = BaseConfig.APP_ENV
        blacklisted_token_key = "blacklisted_token_"+env+"_"+token;
        flag = Redis.get_value_from_redis(redis_client=redis_client, key=blacklisted_token_key)
        log("check token blacklisted status success", blacklisted_token_key=blacklisted_token_key, flag=flag)
        return flag is not None
    except Exception as e:
        log("check_token_blacklisted_status failed", level="ERROR", error=str(e))
        return False


def get_resource_type_column_name(ai_type: str) -> str:
    match ai_type:
        case "gpt":
            return "Open AI Prediction"     
        case "claude":
            raise ValueError("Claude is not supported")
        case "gemini":
            raise ValueError("Gemini is not supported")
        case _:
            raise ValueError(f"Unsupported AI type: {ai_type}")