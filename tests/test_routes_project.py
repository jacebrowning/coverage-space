# pylint: disable=unused-variable,expression-not-assigned,unused-argument

import pytest
from expecter import expect

from api.models import Project

from .utilities import load


def describe_project():

    @pytest.fixture
    def project(tmpdir):
        tmpdir.chdir()
        return Project('my_owner', 'my_repo')

    @pytest.fixture
    def project2(project):
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

        def it_returns_actual_metrics_when_existing(client, project2):
            status, data = load(client.get("/my_owner/my_repo"))

            expect(status) == 200
            expect(data) == {
                'unit': 1.0,
                'integration': 2.0,
                'overall': 3.0,
            }

    def describe_put():

        def it_updates_metrics(client, project2):
            params = {'integration': 42}
            status, data = load(client.put("/my_owner/my_repo", data=params))

            expect(status) == 200
            expect(data) == {
                'unit': 1.0,
                'integration': 42.0,
                'overall': 3.0,
            }

        def it_supports_updating_mulptiple_metrics(client, project2):
            params = {'unit': 55, 'integration': 66}
            status, data = load(client.put("/my_owner/my_repo", data=params))

            expect(status) == 200
            expect(data) == {
                'unit': 55.0,
                'integration': 66.0,
                'overall': 3.0,
            }

        def it_returns_an_error_on_invalid_metrics(client):
            params = {'integration': "foobar"}
            status, data = load(client.put("/my_owner/my_repo", data=params))

            expect(status) == 422
            expect(data) == {
                'message': {
                    'integration': ["Not a valid number."],
                }
            }

        def it_returns_an_error_when_metrics_decrease(client, project2):
            params = {'overall': 2.9}
            status, data = load(client.put("/my_owner/my_repo", data=params))

            expect(status) == 422
            expect(data) == {
                'message': {
                    'overall': ["Value dropped below minimum: 3.0"],
                }
            }

        def it_handles_multiple_bad_metrics(client, project2):
            params = {'unit': 0, 'integration': 0, 'overall': 99}
            status, data = load(client.put("/my_owner/my_repo", data=params))

            expect(status) == 422
            expect(data) == {
                'message': {
                    'unit': ["Value dropped below minimum: 1.0"],
                    'integration': ["Value dropped below minimum: 2.0"],
                }
            }

        def it_returns_an_error_when_no_metrics_specified(client):
            status, data = load(client.put("/my_owner/my_repo"))

            expect(status) == 422
            expect(data) == {
                'message': "No metrics provided."
            }

    def describe_delete():

        def it_resets_metrics(client, project2):
            status, data = load(client.delete("/my_owner/my_repo"))

            expect(status) == 200
            expect(data) == {
                'unit': 0.0,
                'integration': 0.0,
                'overall': 0.0,
            }


def describe_project_branch():

    @pytest.fixture
    def project(tmpdir):
        tmpdir.chdir()
        return Project('my_owner', 'my_repo', 'my_branch')

    @pytest.fixture
    def project2(project):
        project.unit = 4
        project.integration = 5
        project.overall = 6
        return project

    def describe_get():

        def it_returns_default_metrics_when_new(client, project):
            status, data = load(client.get("/my_owner/my_repo/my_branch"))

            expect(status) == 200
            expect(data) == {
                'unit': 0.0,
                'integration': 0.0,
                'overall': 0.0,
            }

        def it_returns_actual_metrics_when_existing(client, project2):
            status, data = load(client.get("/my_owner/my_repo/my_branch"))

            expect(status) == 200
            expect(data) == {
                'unit': 4.0,
                'integration': 5.0,
                'overall': 6.0,
            }

    def describe_put():

        def it_updates_metrics(client, project2):
            status, data = load(client.put("/my_owner/my_repo/my_branch",
                                           data={'integration': 42}))

            expect(status) == 200
            expect(data) == {
                'unit': 4.0,
                'integration': 42.0,
                'overall': 6.0,
            }

        def it_uses_master_as_the_default(client, project):
            client.put("/my_owner/my_repo", data={'unit': 1.23})
            _, data = load(client.get("/my_owner/my_repo/master"))

            expect(data['unit']) == 1.23

    def describe_reset():

        def it_resets_metrics(client, project2):
            endpoint = "/my_owner/my_repo/my_branch"
            status, data = load(client.delete(endpoint))

            expect(status) == 200
            expect(data) == {
                'unit': 0.0,
                'integration': 0.0,
                'overall': 0.0,
            }
