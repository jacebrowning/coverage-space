import shutil

from flask import Blueprint, request
from flask_api import exceptions
import log
import yorm

from .. import __version__
from ..models import Project
from ._utils import sync, track
from ._schemas import parser, ProjectSchema, UnprocessableEntity

BASE = "<owner>/<repo>"

blueprint = Blueprint('project', __name__, url_prefix="/")


@blueprint.route(BASE, methods=['GET', 'PUT', 'DELETE'])
@parser.use_args(ProjectSchema())
def metrics(data, owner, repo):
    """Get coverage metrics for the default branch."""
    create = request.method == 'PUT'

    project = _get_project(owner, repo, create=create)
    if not project:
        raise exceptions.NotFound("No such project.")

    return _handle_request(project, data)


@blueprint.route(BASE + "/<path:branch>", methods=['GET', 'PUT', 'DELETE'])
@parser.use_args(ProjectSchema())
def branch_metrics(data, owner, repo, branch):
    """Get coverage metrics for a particular branch."""
    create = request.method == 'PUT'

    project = _get_project(owner, repo, branch, create=create)
    if not project:
        raise exceptions.NotFound("No such project or branch.")

    return _handle_request(project, data)


def _get_project(owner, repo, branch=None, *, create=False):
    if owner.startswith(".") or repo.startswith("."):
        return None
    args = [owner, repo]
    if branch:
        args.append(branch)
    try:
        project = yorm.find(Project, *args, create=create)
    except yorm.exceptions.FileContentError as e:
        log.critical(e)
        shutil.rmtree(f'data/{owner}/{repo}')
        project = yorm.create(Project, *args)
    return project


def _handle_request(project, data):
    if request.method == 'PUT':
        if not data:
            raise exceptions.ParseError("No metrics provided.")
        try:
            project.update(data, exception=UnprocessableEntity)
        finally:
            sync(project)
        return track(project.current_metrics)

    elif request.method == 'DELETE':
        project.reset()
        sync(project)
        return track(dict(message="Reset minimum metrics.")), 202

    else:
        assert request.method == 'GET'
        sync(project, changes=False)
        return track(project.current_metrics)
