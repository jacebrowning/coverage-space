# pylint: disable=unused-variable,expression-not-assigned

from expecter import expect

from .utilities import load


def describe_root():

    def it_returns_metadata(client):

        status, data = load(client.get("/"))

        expect(status) == 200
        expect(sorted(data.keys())) == ['changes', 'date', 'version']
