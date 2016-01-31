"""Integration tests configuration file."""
# pylint: disable=unused-argument,wildcard-import,unused-wildcard-import

import yorm

from coveragespace.test.conftest import pytest_configure  # pylint: disable=unused-import

from .fixtures import *


def pytest_runtest_setup(item):
    """Ensure files are created for integration tests."""
    yorm.settings.fake = False
