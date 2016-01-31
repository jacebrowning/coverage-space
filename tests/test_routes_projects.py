# pylint: disable=unused-variable,expression-not-assigned,unused-argument

import pytest
from expecter import expect

from coveragespace.models import Project

from .utilities import load


def describe_projects():

    @pytest.fixture
    def project(tmpdir):
        tmpdir.chdir()
        return Project('my_owner', 'my_repo')

    @pytest.fixture
    def project_modified(project):
        project.unit = 1
        project.integration = 2
        project.overall = 3
        return project

    def describe_get():

        def it_returns_default_metrics_when_new(client, project):
            status, data = load(client.get("/my_owner/my_repo"))

            expect(status) == 200
            expect(data) == {
                'unit': 0.0,
                'integration': 0.0,
                'overall': 0.0,
            }

        def it_returns_actual_metrics_when_existing(client, project_modified):
            status, data = load(client.get("/my_owner/my_repo"))

            expect(status) == 200
            expect(data) == {
                'unit': 1.0,
                'integration': 2.0,
                'overall': 3.0,
            }

    def describe_patch():

        def it_updates_metrics(client, project_modified):
            params = {'integration': 42}
            status, data = load(client.patch("/my_owner/my_repo", data=params))

            expect(status) == 200
            expect(data) == {
                'unit': 1.0,
                'integration': 42.0,
                'overall': 3.0,
            }

        def it_supports_updating_mulptiple_metrics(client, project_modified):
            params = {'unit': 55, 'integration': 66}
            status, data = load(client.patch("/my_owner/my_repo", data=params))

            expect(status) == 200
            expect(data) == {
                'unit': 55.0,
                'integration': 66.0,
                'overall': 3.0,
            }

        def it_returns_an_error_on_invalid_metrics(client):
            params = {'integration': "foobar"}
            status, data = load(client.patch("/my_owner/my_repo", data=params))

            expect(status) == 422
            expect(data) == {
                'message': {
                    'integration': ["Not a valid number."],
                }
            }
