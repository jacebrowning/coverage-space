import pprint
import logging

import requests
from flask import current_app, request

GITHUB_BASE = "https://raw.githubusercontent.com/jacebrowning/coverage-space/master/"
CONTRIBUTING_URL = GITHUB_BASE + "CONTRIBUTING.md"
CHANGES_URL = GITHUB_BASE + "CHANGES.md"

log = logging.getLogger(__name__)


def track():
    """Log the requested content, server-side."""
    data = dict(
        v=1,
        tid=_get_tid(),
        cid=request.remote_addr,

        t='pageview',
        # TODO: determine if this is neccessary
        # dh='coverage.space',
        dp=request.path,
        # dt="TBD""

        uip=request.remote_addr,
        ua=request.user_agent.string,
        dr=request.referrer,
    )
    if _get_tid(default=None):
        requests.post("http://www.google-analytics.com/collect", data=data)
    else:
        log.debug("Analytics data:\n%s", pprint.pformat(data))


def _get_tid(*, default='local'):
    """Get the analtyics tracking identifier."""
    return current_app.config['GOOGLE_ANALYTICS_TID'] or default
