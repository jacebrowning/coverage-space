# pylint: disable=unused-variable,expression-not-assigned

import pytest
from expecter import expect

from coveragespace.models import Project


def describe_project():

    @pytest.fixture
    def project():
        return Project('abc', 'def')

    @pytest.fixture
    def project_modified(project):
        project.unit = 1.2
        return project

    def describe_init():

        def it_sets_attributes(project):
            expect(project.owner) == 'abc'
            expect(project.repo) == 'def'

    def describe_metrics():

        def is_zero_by_default(project):
            expect(project.metrics) == dict(
                unit=0.0,
                integration=0.0,
                overall=0.0,
            )

        def can_be_set(project_modified):
            project_modified.metrics = dict(overall=42)

            expect(project_modified.metrics) == dict(
                unit=1.2,
                integration=0.0,
                overall=42.0,
            )

    def describe_reset():

        def it_sets_all_metrics_to_zero(project_modified):
            project_modified.reset()

            expect(project_modified.metrics) == dict(
                unit=0.0,
                integration=0.0,
                overall=0.0,
            )
