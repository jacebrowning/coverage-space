# pylint: disable=unused-variable,expression-not-assigned

from expecter import expect

from .conftest import load


def describe_root():

    def it_returns_links_and_metadata(client):
        response = client.get("/")

        expect(response.status_code) == 200
        expect(load(response)) == dict(
            version="0.0.0",
            changes="https://raw.githubusercontent.com/jacebrowning/coverage-space/master/CHANGES.md"
        )
