from src.config.env import get_env
from src.constants.redis_keys import (
    DEFAULT_CONNECTION_TTL_SECONDS,
    DEFAULT_SESSION_TTL_SECONDS_SECONDS
)
from src.constants.aws import DEFAULT_AWS_REGION
from src.utils.json_utils import json_dumps, json_loads
from src.utils.logging import log
from urllib.parse import unquote
import base64
import boto3


SECRET_CACHE = {}

class BaseConfig:
    # Runtime
    APP_ENV = get_env("APP_ENV", "dev")
    AWS_REGION = get_env("AWS_REGION", DEFAULT_AWS_REGION)
    LOG_LEVEL = get_env("LOG_LEVEL", "INFO")

    # Redis
    REDIS_HOST = get_env("REDIS_HOST", "localhost")
    REDIS_PORT = int(get_env("REDIS_PORT", 6379))
    REDIS_SSL = get_env("REDIS_SSL", "false").lower() == "true"
    REDIS_DATABASE_INDEX = int(get_env("REDIS_DATABASE_INDEX", 0))

    # TTLs
    CONNECTION_TTL_SECONDS = int(get_env("CONNECTION_TTL_SECONDS", DEFAULT_CONNECTION_TTL_SECONDS))
    SESSION_TTL_SECONDS = int(get_env("SESSION_TTL_SECONDS", DEFAULT_SESSION_TTL_SECONDS_SECONDS))
    REDIS_ENABLED = get_env("REDIS_ENABLED", "false").lower() == "true"
    SECRET_KEY = get_env("SECRET_KEY", "")
    JWT_ALGORITHM = get_env("JWT_ALGORITHM", "HS256")

    @staticmethod
    def init_secret_manager(service_name='secretsmanager', region_name="us-west-1"):
        session = boto3.session.Session()
        client = session.client(service_name=service_name, region_name=region_name)

        return client

    @staticmethod
    def get_secret_value(db_name:str="main"):
        try:
            secret_host_name = BaseConfig.get_full_env()
            secret_name = f"{secret_host_name}" + '/db/' + db_name

            # Check if secret already exists in cache
            if secret_name in SECRET_CACHE:
                return SECRET_CACHE[secret_name]
            print(f"secret_name: {secret_name}")

            client = BaseConfig.init_secret_manager()
            get_secret_value_response = client.get_secret_value(SecretId=secret_name)

            
            if 'SecretString' in get_secret_value_response:
                secret = get_secret_value_response['SecretString']
            else:
                secret = base64.b64decode(get_secret_value_response['SecretBinary'])

            if isinstance(secret, str):
                secret = json_loads(secret)

            secret['secret_name'] = secret_name
            
            SECRET_CACHE[secret_name] = json_dumps(secret)

            return SECRET_CACHE[secret_name]

        except Exception as e:
            log("get_secret_value failed", level="ERROR", error=str(e))
            raise e
    
    @staticmethod
    def get_db_configuration_details(db_name="main", db_type="mysql"):
        try:
            db_data = {}

            if db_type == "mysql":
                secret = BaseConfig.get_secret_value(db_name=db_name)
                data = json_loads(secret)
                
                db_data['username'] = str(data.get('username'))
                db_data['password'] = str(unquote(data.get('password')))
                db_data['host'] = str(data.get('host'))
                db_data['port'] = str(data.get('port'))
                db_data["dbname"] = str(data.get('dbname'))
                db_data["secret_name"] = str(data.get('secret_name'))
            
            elif db_type == "redis":
                db_data['host'] = BaseConfig.REDIS_HOST
                db_data['port'] = BaseConfig.REDIS_PORT
                db_data['ssl'] = BaseConfig.REDIS_SSL

            return db_data

        except Exception as e:
            log("get_db_configuration_details failed", level="ERROR", error=str(e))
            return db_data
    
    @staticmethod
    def get_full_env(prefix: str = "zenarate/"):
        try:
            env = BaseConfig.APP_ENV
            if not prefix in env:
                env = prefix + env
            log("get_full_env success", env=env)
            return env
        except Exception as e:
            log("get_full_env failed", level="ERROR", error=str(e))
            return ""