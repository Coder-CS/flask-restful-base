import json
from pathlib import Path


def get_config(config_path: Path) -> dict:
    if config_path.exists():
        with open(str(config_path.resolve())) as fp:
            return json.load(fp)
    return {}


path = Path()
root_path = path.parent
config = get_config(root_path.joinpath("config.json"))


class ConfigBase:
    APP_NAME = config.get("APP_NAME", 'flask-end-base')
    SQLALCHEMY_TRACK_MODIFICATIONS = True


class DevelopmentConfig(ConfigBase):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = config.get('DATABASE_URI', f"sqlite:///{root_path.joinpath('data-dev.db')}")


class ProductionConfig(ConfigBase):
    SQLALCHEMY_DATABASE_URI = config.get('DATABASE_URI', f"sqlite:///{root_path.joinpath('data-prd.db')}")


configs = {
    "dev": DevelopmentConfig,
    "prd": ProductionConfig
}



