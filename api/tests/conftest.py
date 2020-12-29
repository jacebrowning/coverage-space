"""Unit tests configuration file."""
# pylint: disable=redefined-outer-name,unused-argument

import yorm


def pytest_configure(config):
    """Disable verbose output when running tests."""
    terminal = config.pluginmanager.getplugin('terminal')
    terminal.TerminalReporter.showfspath = False


def pytest_runtest_setup(item):
    """Disable file creation during unit tests."""
    yorm.settings.fake = True
