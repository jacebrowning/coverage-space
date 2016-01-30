# pylint: disable=unused-variable,expression-not-assigned,unused-argument

import pytest
from expecter import expect

from coveragespace.models import Project

from .conftest import load


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

    def describe_GET():

        def it_returns_default_metrics_on_new(client, project):
            response = client.get("/my_owner/my_repo")

            expect(response.status_code) == 200
            expect(load(response)) == dict(
                unit=0.0,
                integration=0.0,
                overall=0.0,
            )

        def it_returns_actual_metrics_on_existing(client, project_modified):
            response = client.get("/my_owner/my_repo")

            expect(response.status_code) == 200
            expect(load(response)) == dict(
                unit=1.0,
                integration=2.0,
                overall=3.0,
            )
