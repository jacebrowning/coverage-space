import os
import pprint
import logging

from sh import git as _git, ErrorReturnCode  # pylint: disable=no-name-in-module
import requests
from flask import current_app, request

from .. import URL

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
DATA = os.path.join(ROOT, "data")

GITHUB_BASE = "https://raw.githubusercontent.com/jacebrowning/coverage-space/master/"
CONTRIBUTING_URL = GITHUB_BASE + "CONTRIBUTING.md"
CHANGES_URL = GITHUB_BASE + "CHANGES.md"

log = logging.getLogger(__name__)


def sync(model, *, push=True):
    """Store all changes in version control."""
    git = _git.bake(git_dir=os.path.join(DATA, ".git"), work_tree=DATA)

    log.info("Saving changes...")
    git.add(all=True)
    try:
        git.commit(message=str(model))
    except ErrorReturnCode:
        log.info("No changes to save")

    log.info("Pulling changes...")
    git.pull(rebase=True)

    if push:
        log.info("Pushing changes...")
        git.push('origin', 'master')


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
