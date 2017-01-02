import os
import pprint
import logging
from contextlib import suppress

from sh import git as _git, ErrorReturnCode  # pylint: disable=no-name-in-module
import requests
from flask import current_app, request

from .. import URL

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
DATA = os.path.join(ROOT, "data")

GITHUB_BASE = "https://raw.githubusercontent.com/jacebrowning/coverage-space/master/"
CONTRIBUTING_URL = GITHUB_BASE + "CONTRIBUTING.md"
CHANGELOG_URL = GITHUB_BASE + "CHANGELOG.md"

log = logging.getLogger(__name__)
git = _git.bake(git_dir=os.path.join(DATA, ".git"), work_tree=DATA)


def sync(model, *, changes=True):
    """Store all changes in version control."""
    if changes:
        log.info("Saving changes...")
        git.checkout('master')
        git.add(all=True)
        try:
            git.diff(cached=True, exit_code=True)
        except ErrorReturnCode:
            git.commit(message=str(model))
        else:
            log.info("No changes to save")

    log.info("Pulling changes...")
    try:
        git.pull(rebase=True)
    except ErrorReturnCode:
        log.error("Merge conflicts detected, attempting reset...")
        git.fetch()
        with suppress(ErrorReturnCode):
            git.rebase(abort=True)
        git.reset('origin/master', hard=True)

    if changes:
        log.info("Pushing changes...")
        git.push(force=True)


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
