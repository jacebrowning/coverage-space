import os
import pprint
import contextlib
import logging

from sh import git, ErrorReturnCode  # pylint: disable=no-name-in-module
import requests
from flask import current_app, request

from .. import URL

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
DATA = os.path.join(ROOT, "data")

GITHUB_BASE = "https://raw.githubusercontent.com/jacebrowning/coverage-space/master/"
CONTRIBUTING_URL = GITHUB_BASE + "CONTRIBUTING.md"
CHANGES_URL = GITHUB_BASE + "CHANGES.md"

log = logging.getLogger(__name__)


def sync(model):
    """Store all changes in version control."""
    remote = current_app.config['ENV'] == 'prod'

    message = str(model)  # YORM models can't be used in a different directory

    with location(DATA):
        git.add(all=True)
        git.stash()
        if remote:
            git.pull()
        try:
            git.stash('apply')
            git.add(all=True)
            git.commit(message=message)
        except ErrorReturnCode:
            log.warning("No changes to save")
        else:
            log.info("Saved model: %s", message)
            if remote:
                git.push()


@contextlib.contextmanager
def location(dirpath):
    """Change to a directory, temporarily."""
    cwd = os.getcwd()
    os.chdir(dirpath)
    yield
    os.chdir(cwd)


def track(obj):
    """Log the requested content, server-side."""
    data = dict(
        v=1,
        tid=_get_tid(),
        cid=request.remote_addr,

        t='pageview',
        dh=URL,
        dp=request.path,
        dt=request.method + ' ' + request.url_rule.endpoint,

        uip=request.remote_addr,
        ua=request.user_agent.string,
        dr=request.referrer,
    )

    if _get_tid(default=None):
        requests.post("http://www.google-analytics.com/collect", data=data)
        log.debug("Analytics data:\n%s", pprint.pformat(data))

    return obj


def _get_tid(*, default='local'):
    """Get the analtyics tracking identifier."""
    return current_app.config['GOOGLE_ANALYTICS_TID'] or default
