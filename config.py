from pathlib import Path
import json

path = Path()

config = {}
config_path = path.joinpath("config.json")
if config_path.exists():
    with open(config_path.resolve()) as fp:
        config = json.load(fp)


class ConfigBase:
    APP_NAME = config.get("APP_NAME", 'flask-end-base')


class DevelopmentConfig(ConfigBase):
    DEBUG = True

class ProductionConfig(ConfigBase):
    pass


class CONFIGS:
    DEV = DevelopmentConfig
    PRD = ProductionConfig

