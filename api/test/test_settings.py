# pylint: disable=unused-variable,expression-not-assigned

from expecter import expect

from api.settings import get_config


def describe_get_config():

    def it_returns_a_config():
        config = get_config('prod')

        expect(config.ENV) == 'prod'

    def it_handles_empty_names():
        with expect.raises(AssertionError):
            get_config('')

    def it_handles_unknown_names():
        with expect.raises(AssertionError):
            get_config('not_a_valid_config')
