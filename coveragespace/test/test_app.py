# pylint: disable=unused-variable,expression-not-assigned

from expecter import expect

from coveragespace import app
from coveragespace import settings


def describe_app():

    def when_dev():
        _app = app.create_app(settings.DevConfig)

        expect(_app.config['DEBUG']) is True
        expect(_app.config['TESTING']) is False

    def when_test():
        _app = app.create_app(settings.TestConfig)

        expect(_app.config['DEBUG']) is True
        expect(_app.config['TESTING']) is True

    def when_prod():
        _app = app.create_app(settings.ProdConfig)

        expect(_app.config['DEBUG']) is False
        expect(_app.config['TESTING']) is False
