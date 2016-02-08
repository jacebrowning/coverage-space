import os
from collections import OrderedDict

from flask import Blueprint

from .. import __version__

from ._common import CHANGES_URL, track


blueprint = Blueprint('root', __name__, url_prefix="/")


@blueprint.route("")
def index():
    """Track code coverage metrics."""
    metadata = OrderedDict()

    metadata['version'] = __version__
    metadata['date'] = os.getenv('DEPLOY_DATE')
    metadata['changes'] = CHANGES_URL

    return track(metadata)