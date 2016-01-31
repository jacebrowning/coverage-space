import logging

from flask import Blueprint, request

from .. import __version__
from ..models import Project

from ._common import track
from ._schemas import parser, ProjectSchema


blueprint = Blueprint('project', __name__, url_prefix="/")
log = logging.getLogger(__name__)


@blueprint.route("<owner>/<repo>", methods=['GET', 'PATCH'])
@parser.use_args(ProjectSchema())
def metrics(args, owner, repo):
    """Get coverage metrics for the default branch."""
    project = Project(owner, repo)

    if request.method == 'PATCH':
        project.metrics = args

    return track(project.metrics)


@blueprint.route("<owner>/<repo>/<path:branch>", methods=['GET', 'PATCH'])
@parser.use_args(ProjectSchema())
def branch_metrics(args, owner, repo, branch):
    """Get coverage metrics for a particular branch."""
    project = Project(owner, repo, branch)

    if request.method == 'PATCH':
        project.metrics = args

    return track(project.metrics)
