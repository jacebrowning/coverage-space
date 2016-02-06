# pylint: disable=redefined-outer-name

import pytest

from api.app import create_app
from api.settings import get_config


@pytest.fixture
def app():
    return create_app(get_config('test'))


@pytest.fixture
def client(app):
    return app.test_client()
