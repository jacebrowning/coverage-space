# pylint: disable=unused-variable,unused-argument,expression-not-assigned
import pytest
from expecter import expect

from coveragespace.cli.plugins import get_coverage


def describe_get_coverage():

    @pytest.fixture
    def coveragepy(tmpdir):
        cwd = tmpdir.chdir()
        with open("foobar.py", 'w') as stream:
            pass
        with open(".coverage", 'w') as stream:
            stream.write("""
            !coverage.py: This is a private format, don\'t read it directly!
            {"arcs":{"foobar.py": [[-1, 3]]}}
            """.strip())

    def it_supports_coveragepy(coveragepy):
        expect(get_coverage()) == 0
