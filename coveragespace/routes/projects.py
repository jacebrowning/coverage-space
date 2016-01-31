import logging

from flask import Blueprint

from .. import __version__
from ..models import Project

from ._common import track
from ._schemas import parser, ProjectSchema


blueprint = Blueprint('projects', __name__, url_prefix="/")
log = logging.getLogger(__name__)


@blueprint.route("<owner>/<repo>", methods=['GET'])
def get(owner, repo):
    """Get coverage metrics."""
    project = Project(owner, repo)

    track(blueprint.name + " -  GET")

    return project.metrics


@blueprint.route("<owner>/<repo>", methods=['PATCH'])
@parser.use_args(ProjectSchema())
def patch(args, owner, repo):
    """Update coverage metrics."""
    project = Project(owner, repo)
    project.metrics = args

    track(blueprint.name + " -  PATCH")

    return project.metrics
