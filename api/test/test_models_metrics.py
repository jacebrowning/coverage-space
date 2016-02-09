# pylint: disable=unused-variable,expression-not-assigned

import pytest
from expecter import expect

from api.models import Metrics


def describe_metrics():

    @pytest.fixture
    def metrics():
        return Metrics(1.2, 3.4, 5.6)

    def describe_init():

        def it_sets_attributes(metrics):
            expect(metrics.unit) == 1.2
            expect(metrics.integration) == 3.4
            expect(metrics.overall) == 5.6

    def describe_str():

        def it_summarizes_values(metrics):
            expect(str(metrics)) == \
                "Unit: 1.2%, Integration: 3.4%, Overall: 5.6%"

    def describe_reset():

        def it_sets_all_values_to_zero(metrics):
            metrics.reset()

            expect(metrics.data) == dict(
                unit=0.0,
                integration=0.0,
                overall=0.0,
            )
