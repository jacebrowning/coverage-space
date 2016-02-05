import logging

from flask import Blueprint, request

from .. import __version__
from ..models import Project

from ._common import sync, track
from ._schemas import parser, ProjectSchema, UnprocessableEntity

BASE = "<owner>/<repo>"

blueprint = Blueprint('project', __name__, url_prefix="/")
log = logging.getLogger(__name__)


@blueprint.route(BASE, methods=['GET', 'PUT', 'DELETE'])
@parser.use_args(ProjectSchema())
def metrics(args, owner, repo):
    """Get coverage metrics for the default branch."""
    project = Project(owner, repo)
    return _handle_request(project, args)


@blueprint.route(BASE + "/<path:branch>", methods=['GET', 'PUT', 'DELETE'])
@parser.use_args(ProjectSchema())
def branch_metrics(args, owner, repo, branch):
    """Get coverage metrics for a particular branch."""
    project = Project(owner, repo, branch)
    return _handle_request(project, args)


def _handle_request(project, args):
    if request.method == 'PUT':
        project.update(args, exception=UnprocessableEntity)
        sync(project)
    elif request.method == 'DELETE':
        project.reset()
        sync(project)
    else:
        assert request.method == 'GET'
        sync(project, commit=False)

    return track(project.metrics)
