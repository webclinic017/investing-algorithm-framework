import logging
import os
from enum import Enum

from .constants import RESOURCE_DIRECTORY, BACKTEST_DATA_DIRECTORY_NAME
from .exceptions import OperationalException

logger = logging.getLogger("investing_algorithm_framework")


class Environment(Enum):
    """
    Class TimeUnit: Enum for data_provider base type
    """
    DEV = 'DEV'
    PROD = 'PROD'
    TEST = 'TEST'

    # Static factory method to convert
    # a string to environment
    @staticmethod
    def from_string(value: str):

        if isinstance(value, str):

            for entry in Environment:

                if value.upper() == entry.value:
                    return entry

            raise OperationalException(
                "Could not convert value to a environment type"
            )

        else:
            raise OperationalException(
                "Could not convert non string value to a environment type"
            )

    def equals(self, other):

        if isinstance(other, Enum):
            return self.value == other.value
        else:

            try:
                data_base_type = Environment.from_string(other)
                return data_base_type == self
            except OperationalException:
                pass

            return other == self.value


class Config(dict):
    ENVIRONMENT = Environment.PROD.value
    LOG_LEVEL = 'DEBUG'
    APP_DIR = os.path.abspath(os.path.dirname(__file__))
    PROJECT_ROOT = os.path.abspath(os.path.join(APP_DIR, os.pardir))
    DEBUG_TB_INTERCEPT_REDIRECTS = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    CACHE_TYPE = 'simple'  # Can be "memcached", "redis", etc.
    CORS_ORIGIN_WHITELIST = [
        'http://0.0.0.0:4100',
        'http://localhost:4100',
        'http://0.0.0.0:8000',
        'http://localhost:8000',
        'http://0.0.0.0:4200',
        'http://localhost:4200',
        'http://0.0.0.0:4000',
        'http://localhost:4000',
    ]
    RESOURCE_DIRECTORY = os.getenv(RESOURCE_DIRECTORY)
    SCHEDULER_API_ENABLED = True
    CHECK_PENDING_ORDERS = True
    SQLITE_ENABLED = True
    SQLITE_INITIALIZED = False
    BACKTEST_DATA_DIRECTORY_NAME = "backtest_data"

    def __init__(self, resource_directory=None):
        super().__init__()

        if resource_directory is not None:
            self.RESOURCE_DIRECTORY = resource_directory

        super().__init__(vars(self.__class__))

    # def __setitem__(self, key, item):
    #     self.__dict__[key] = item
    #
    # def __getitem__(self, key):
    #     return self.__dict__[key]
    #
    # def __repr__(self):
    #     return repr(self.__dict__)
    #
    # def __len__(self):
    #     return len(self.__dict__)
    #
    # def __delitem__(self, key):
    #     del self.__dict__[key]
    #
    # def clear(self):
    #     return self.__dict__.clear()
    #
    # def copy(self):
    #     return self.__dict__.copy()
    #
    # def has_key(self, k):
    #     return k in self.__dict__
    #
    # def update(self, *args, **kwargs):
    #     return self.__dict__.update(*args, **kwargs)
    #
    # def keys(self):
    #     return self.__dict__.keys()
    #
    # def values(self):
    #     return self.__dict__.values()
    #
    # def items(self):
    #     return self.__dict__.items()
    #
    # def pop(self, *args):
    #     return self.__dict__.pop(*args)
    #
    # def __cmp__(self, dict_):
    #     return self.__cmp__(self.__dict__, dict_)
    #
    # def __contains__(self, item):
    #     return item in self.__dict__
    #
    # def __iter__(self):
    #     return iter(self.__dict__)

    def __str__(self):
        field_strings = []

        for attribute_key in self:

            if attribute_key.isupper():
                field_strings.append(
                    f'{attribute_key}='
                    f'{self[attribute_key]!r}'
                )

        return f"<{self.__class__.__name__}({','.join(field_strings)})>"

    def get(self, key: str, default=None):
        """
        Mimics the dict get() functionality
        """

        try:
            return self[key]
        # Ignore exception
        except Exception:
            pass

        return default

    def set(self, key: str, value) -> None:
        self[key] = value

    @staticmethod
    def from_dict(dictionary):
        config = Config()

        for attribute_key in dictionary:

            if attribute_key:
                config.set(attribute_key, dictionary[attribute_key])
                config[attribute_key] = dictionary[attribute_key]

        return config


class TestConfig(Config):
    ENVIRONMENT = Environment.TEST.value
    TESTING = True
    DATABASE_CONFIG = {'DATABASE_NAME': "test"}
    LOG_LEVEL = "INFO"


class DevConfig(Config):
    ENVIRONMENT = Environment.DEV.value
    DATABASE_CONFIG = {'DATABASE_NAME': "dev"}
    LOG_LEVEL = "INFO"
