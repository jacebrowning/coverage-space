import os


class Config:

    ENV = None

    PATH = os.path.abspath(os.path.dirname(__file__))
    ROOT = os.path.dirname(PATH)
    DEBUG = False
    THREADED = False

    GOOGLE_ANALYTICS_TID = os.getenv('GOOGLE_ANALYTICS_TID')


class ProductionConfig(Config):

    ENV = 'production'


class StagingConfig(ProductionConfig):

    ENV = 'staging'


class LocalConfig(Config):

    ENV = 'local'

    DEBUG = True


class TestConfig(LocalConfig):

    ENV = 'test'

    TESTING = True


def get_config(name):
    assert name, "No configuration specified"

    for config in _subclasses(Config):
        if config.ENV == name:
            return config

    assert False, "No matching configuration"
    return None


def _subclasses(cls):
    yield from cls.__subclasses__()
    yield from (g for s in cls.__subclasses__() for g in _subclasses(s))
