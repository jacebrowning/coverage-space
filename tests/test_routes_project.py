# pylint: disable=unused-variable,expression-not-assigned,unused-argument

import pytest
from expecter import expect

from coveragespace.models import Project

from .utilities import load


def describe_project():

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

        def it_returns_an_error_when_metrics_decrease(client, project_modified):
            params = {'overall': 2.9}
            status, data = load(client.patch("/my_owner/my_repo", data=params))

            expect(status) == 422
            expect(data) == {
                'message': {
                    'overall': ["Lower than previous value."],
                }
            }

        def it_handles_multiple_bad_metrics(client, project_modified):
            params = {'unit': 0, 'integration': 0, 'overall': 99}
            status, data = load(client.patch("/my_owner/my_repo", data=params))

            expect(status) == 422
            expect(data) == {
                'message': {
                    'unit': ["Lower than previous value."],
                    'integration': ["Lower than previous value."],
                }
            }


def describe_project_branch():

    @pytest.fixture
    def project(tmpdir):
        tmpdir.chdir()
        return Project('my_owner', 'my_repo', 'my_branch')

    @pytest.fixture
    def project_modified(project):
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

        def it_returns_actual_metrics_when_existing(client, project_modified):
            status, data = load(client.get("/my_owner/my_repo/my_branch"))

            expect(status) == 200
            expect(data) == {
                'unit': 4.0,
                'integration': 5.0,
                'overall': 6.0,
            }

    def describe_patch():

        def it_updates_metrics(client, project_modified):
            status, data = load(client.patch("/my_owner/my_repo/my_branch",
                                             data={'integration': 42}))

            expect(status) == 200
            expect(data) == {
                'unit': 4.0,
                'integration': 42.0,
                'overall': 6.0,
            }

        def it_uses_master_as_the_default(client, project):
            client.patch("/my_owner/my_repo", data={'unit': 1.23})
            _, data = load(client.get("/my_owner/my_repo/master"))

            expect(data['unit']) == 1.23


def describe_project_reset():

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

    def describe_post():

        def it_returns_reset_metrics(client, project_modified):
            status, data = load(client.post("/my_owner/my_repo/reset"))

            expect(status) == 200
            expect(data) == {
                'unit': 0.0,
                'integration': 0.0,
                'overall': 0.0,
            }


def describe_project_branch_reset():

    @pytest.fixture
    def project(tmpdir):
        tmpdir.chdir()
        return Project('my_owner', 'my_repo', 'my_branch')

    @pytest.fixture
    def project_modified(project):
        project.unit = 4
        project.integration = 5
        project.overall = 6
        return project

    def describe_post():

        def it_returns_reset_metrics(client, project_modified):
            endpoint = "/my_owner/my_repo/my_branch/reset"
            status, data = load(client.post(endpoint))

            expect(status) == 200
            expect(data) == {
                'unit': 0.0,
                'integration': 0.0,
                'overall': 0.0,
            }
