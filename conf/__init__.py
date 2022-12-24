from typing import Any
from conf import config


class Config:
    def __init__(self):
        for setting in dir(config):
            if setting.isupper():
                setattr(self, setting, getattr(config, setting))


settings: Any = Config()
