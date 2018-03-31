# pylint: disable=redefined-outer-name,unused-variable,expression-not-assigned

from . import user


def describe_index():

    def has_custom_title(expect):
        user.visit("/")
        expect(user.browser.title) == "The Coverage Space"
