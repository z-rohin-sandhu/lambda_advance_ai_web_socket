
def check_token_blacklisted_status(env:str, token: str):
    blacklisted_token_key = "blacklisted_token_"+env+"_"+token;
    flag = get_value_from_redis(key=blacklisted_token_key)
    return flag is not None