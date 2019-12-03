import json
from pathlib import Path


path = Path()
root_path = path.parent
setting_path = root_path.joinpath("setting.json")

setting = {"ENV": "dev"}
if setting_path.exists():
    with open(setting_path.resolve()) as fp:
        setting = {**setting, **json.load(fp)}


class ConfigBase(object):
    APP_NAME = setting.get("APP_NAME", 'flask-end-base')
    SECRET_KEY = setting.get("SECRET_KEY", 'YOU_SHOULD_SET_KEY')
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    # Redis
    REDIS_HOST = setting.get("REDIS_HOST", '127.0.0.1')
    REDIS_PORT = setting.get("REDIS_PORT", 6379)
    REDIS_PASSWORD = setting.get("REDIS_PASSWORD", None)
    REDIS_POOL_DB = setting.get("REDIS_POOL_DB", 0)


class DevelopmentConfig(ConfigBase):
    SQLALCHEMY_DATABASE_URI = setting.get('DATABASE_URI', f"sqlite:///{root_path.joinpath('data-dev.db')}")


class ProductionConfig(ConfigBase):
    SQLALCHEMY_DATABASE_URI = setting.get('DATABASE_URI', f"sqlite:///{root_path.joinpath('data-prd.db')}")


class TestConfig(ConfigBase):
    SQLALCHEMY_DATABASE_URI = setting.get('DATABASE_URI', f"sqlite:///{root_path.joinpath('data-test.db')}")


configs = {
    "dev": DevelopmentConfig,
    "prd": ProductionConfig,
    "test": TestConfig
}



