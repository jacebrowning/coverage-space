import logging

from flask import Blueprint, request
from flask_api import exceptions
import yorm

from .. import __version__
from ..models import Project

from ._common import sync, track
from ._schemas import parser, ProjectSchema, UnprocessableEntity

BASE = "<owner>/<repo>"

blueprint = Blueprint('project', __name__, url_prefix="/")
log = logging.getLogger(__name__)


@blueprint.route(BASE, methods=['GET', 'PUT', 'DELETE'])
@parser.use_args(ProjectSchema())
def metrics(data, owner, repo):
    """Get coverage metrics for the default branch."""
    create = request.method == 'PUT'
    project = yorm.find(Project, owner, repo, create=create)
    if not project:
        raise exceptions.NotFound("No such project.")

    return _handle_request(project, data)


@blueprint.route(BASE + "/<path:branch>", methods=['GET', 'PUT', 'DELETE'])
@parser.use_args(ProjectSchema())
def branch_metrics(data, owner, repo, branch):
    """Get coverage metrics for a particular branch."""
    create = request.method == 'PUT'
    project = yorm.find(Project, owner, repo, branch, create=create)
    if not project:
        raise exceptions.NotFound("No such project or branch.")

    return _handle_request(project, data)


def _handle_request(project, data):

    if request.method == 'PUT':
        project.update(data, exception=UnprocessableEntity)
        sync(project)
        return track(project.current_metrics)

    elif request.method == 'DELETE':
        project.reset()
        sync(project)
        return track(dict(message="Reset minimum metrics."))

    else:
        assert request.method == 'GET'
        sync(project, push=False)
        return track(project.current_metrics)
