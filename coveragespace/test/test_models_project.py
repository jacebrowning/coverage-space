# pylint: disable=unused-variable,expression-not-assigned

import pytest
from expecter import expect

from coveragespace.models import Project


def describe_project():

    @pytest.fixture
    def project():
        return Project('abc', 'def')

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
