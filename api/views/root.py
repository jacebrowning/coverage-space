from collections import OrderedDict

from flask import Blueprint

from .. import __version__

from ._utils import CHANGELOG_URL, track


blueprint = Blueprint('root', __name__, url_prefix="/")


@blueprint.route("")
def index():
    """Track code coverage metrics."""
    metadata = OrderedDict()

    metadata['version'] = __version__
    metadata['changelog'] = CHANGELOG_URL

    return track(metadata)
