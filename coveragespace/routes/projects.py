from flask import Blueprint

from .. import __version__
from ..models import Project

from ._common import track


blueprint = Blueprint('projects', __name__, url_prefix="/")


@blueprint.route("<owner>/<repo>")
def get(owner, repo):
    """Get coverage metrics."""
    project = Project(owner, repo)

    track(blueprint.name + " -  GET")

    return project.metrics
