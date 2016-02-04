import os
import pprint
import logging
from multiprocessing import Process

from sh import git as _git  # pylint: disable=no-name-in-module
import requests
from flask import current_app, request

from .. import __url__

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
DATA = os.path.join(ROOT, "data")

GITHUB_BASE = "https://raw.githubusercontent.com/jacebrowning/coverage-space/master/"
CONTRIBUTING_URL = GITHUB_BASE + "CONTRIBUTING.md"
CHANGES_URL = GITHUB_BASE + "CHANGES.md"

log = logging.getLogger(__name__)


def sync(obj, commit=True):
    """Store updated metrics in version control."""

    def run(_sync=False):
        git = _git.bake(git_dir=os.path.join(DATA, ".git"), work_tree=DATA)
        if commit:
            git.add(".")
            git.commit(message=str(obj))
        if _sync:
            if commit:
                git.push(force=True)
            git.pull()

    _sync = current_app.config['ENV'] == 'prod'
    process = Process(target=run, args=[_sync])
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
