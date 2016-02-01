import os
import pprint
import logging
from multiprocessing import Process

from sh import git  # pylint: disable=no-name-in-module
import requests
from flask import current_app, request

from .. import __url__

GITHUB_BASE = "https://raw.githubusercontent.com/jacebrowning/coverage-space/master/"
CONTRIBUTING_URL = GITHUB_BASE + "CONTRIBUTING.md"
CHANGES_URL = GITHUB_BASE + "CHANGES.md"

log = logging.getLogger(__name__)


def commit(obj):
    """Store updated metrics in version control."""

    def _commit():
        os.chdir("data")
        git.add(".")
        git.commit(message=str(obj))
        git.push()

    if current_app.config['ENV'] == 'prod':
        process = Process(target=_commit)
        process.start()

    return obj


def track(obj):
    """Log the requested content, server-side."""
    data = dict(
        v=1,
        tid=_get_tid(),
        cid=request.remote_addr,

        t='pageview',
        dh=__url__,
        dp=request.path,
        dt=request.method + ' ' + request.url_rule.endpoint,

        uip=request.remote_addr,
        ua=request.user_agent.string,
        dr=request.referrer,
    )

    if _get_tid(default=None):
        requests.post("http://www.google-analytics.com/collect", data=data)
    else:
        log.debug("Analytics data:\n%s", pprint.pformat(data))

    return obj


def _get_tid(*, default='local'):
    """Get the analtyics tracking identifier."""
    return current_app.config['GOOGLE_ANALYTICS_TID'] or default
