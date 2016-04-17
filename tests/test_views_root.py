# pylint: disable=unused-variable,expression-not-assigned

from expecter import expect

from .utilities import load


def describe_root():

    def it_returns_metadata(client, monkeypatch):
        monkeypatch.setenv('DEPLOY_DATE', "today")

        status, data = load(client.get("/"))

        expect(status) == 200
        expect(data) == {
            'version': "0.2",
            'date': "today",
            'changes': "https://raw.githubusercontent.com/jacebrowning/coverage-space/master/CHANGES.md"
        }
