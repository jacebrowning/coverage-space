# pylint: disable=unused-variable,expression-not-assigned

from expecter import expect

from .utilities import load


def describe_root():

    def it_returns_links_and_metadata(client):
        status, data = load(client.get("/"))

        expect(status) == 200
        expect(data) == dict(
            version="0.0.0",
            changes="https://raw.githubusercontent.com/jacebrowning/coverage-space/master/CHANGES.md"
        )
