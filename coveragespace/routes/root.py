from collections import OrderedDict

from flask import Blueprint

from .. import __version__

from ._common import CHANGES_URL, track


blueprint = Blueprint('root', __name__, url_prefix="/")


@blueprint.route("")
def get():
    """Track code coverage metrics."""
    data = OrderedDict()
    data['version'] = __version__
    data['changes'] = CHANGES_URL

    track(blueprint.name + " - GET")

    return data
