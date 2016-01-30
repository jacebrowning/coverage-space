"""Package for coverage.space."""

import sys

__project__ = 'coverage.space'
__version__ = '0.0.0'
__url__ = 'coveage.space'

VERSION = "{0} v{1}".format(__project__, __version__)

PYTHON_VERSION = 3, 4

if sys.version_info < PYTHON_VERSION:  # pragma: no cover (manual test)
    exit("Python {}.{}+ is required.".format(*PYTHON_VERSION))
