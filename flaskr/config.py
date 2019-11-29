import json
from pathlib import Path


path = Path()
root_path = path.parent
config_path = root_path.joinpath("config.json")

env = {"ENV": "dev"}
if config_path.exists():
    with open(str(config_path.resolve())) as fp:
        env = {**env, **json.load(fp)}


class ConfigBase:
    APP_NAME = env.get("APP_NAME", 'flask-end-base')
    SECRET_KEY = env.get("SECRET_KEY", 'YOU_SHOULD_SET_KEY')
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    # Redis
    REDIS_HOST = env.get("REDIS_HOST", '127.0.0.1')
    REDIS_PORT = env.get("REDIS_PORT", 6379)
    REDIS_PASSWORD = env.get("REDIS_PASSWORD", None)
    REDIS_POOL_DB = env.get("REDIS_POOL_DB", 0)


class DevelopmentConfig(ConfigBase):
    SQLALCHEMY_DATABASE_URI = env.get('DATABASE_URI', f"sqlite:///{root_path.joinpath('data-dev.db')}")


class ProductionConfig(ConfigBase):
    SQLALCHEMY_DATABASE_URI = env.get('DATABASE_URI', f"sqlite:///{root_path.joinpath('data-prd.db')}")


configs = {
    "dev": DevelopmentConfig,
    "prd": ProductionConfig
}



