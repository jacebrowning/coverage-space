# pylint: disable=unused-variable,expression-not-assigned

import pytest
from expecter import expect

from coveragespace.models import Project


def describe_project():

    @pytest.fixture
    def project():
        return Project('abc', 'def')

    @pytest.fixture
    def project2(project):
        project.unit = 1.2
        project.integration = 3.4
        project.overall = 5.6
        return project

    def describe_init():

        def it_sets_attributes(project):
            expect(project.owner) == 'abc'
            expect(project.repo) == 'def'

    def describe_str():

        def it_inclues_metrics_summary(project2):
            expect(str(project2)) == \
                "Unit: 1.2%, Integration: 3.4%, Overall: 5.6%"

    def describe_metrics():

        def is_zero_by_default(project):
            expect(project.metrics) == dict(
                unit=0.0,
                integration=0.0,
                overall=0.0,
            )

    def describe_update():

        def it_sets_new_metrics(project2):
            project2.update(dict(overall=42))

            expect(project2.metrics) == dict(
                unit=1.2,
                integration=3.4,
                overall=42.0,
            )

        def it_raises_exception_when_they_decrease(project2):
            with expect.raises(ValueError):
                project2.update(dict(unit=1.1))

    def describe_reset():

        def it_sets_all_metrics_to_zero(project2):
            project2.reset()

            expect(project2.metrics) == dict(
                unit=0.0,
                integration=0.0,
                overall=0.0,
            )
