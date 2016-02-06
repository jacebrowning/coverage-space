"""Update metrics on The Coverage Space using HTTPie.

Usage:
  coverage.space <owner/repo> <metric> [<value>]
  coverage.space (-h | --help)
  coverage.space (-V | --version)

Options:
  -h --help     Show this screen.
  -V --version     Show version.

"""

import sys
import subprocess

from docopt import docopt

from .. import API, VERSION

from .plugins import get_coverage


def main():
    arguments = docopt(__doc__, version=VERSION)

    slug = arguments['<owner/repo>']
    metric = arguments['<metric>']
    value = arguments.get('<value>') or get_coverage()

    status = call(slug, metric, value)

    sys.exit(status)


def call(slug, metric, value):

    url = "{}/{}".format(API, slug)
    param = "{}={}".format(metric, value)
    args = ['http', 'put', url, param, '--check-status']
    print('\n' + "$ " + ' '.join(args) + '\n')
    status = subprocess.call(args)

    return status
