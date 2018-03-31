from urllib.parse import urlencode, unquote

from flask import request, current_app
from flask_api import FlaskAPI
import log

from . import views


def create_app(config):
    app = FlaskAPI(__name__)
    app.config.from_object(config)

    configure_logging(app)

    register_services(app)
    register_blueprints(app)
    register_errors(app)

    return app


def configure_logging(app):
    if app.config['DEBUG']:
        level = log.DEBUG
    else:
        level = log.INFO
    log.init(level=level, format="%(levelname)s: %(message)s")
    log.silence('sh', allow_warning=True)
    log.silence('yorm', allow_warning=True)
    log.silence('requests', allow_warning=True)


def register_services(app):

    def log_request(response=None):
        if current_app.debug:
            path = request.path
            if request.args:
                path += "?%s" % unquote(urlencode(request.args))
            if response:
                log.info("%s: %s - %i", request.method, path,
                         response.status_code)
            else:
                log.info("%s: %s", request.method, path)

        return response

    app.before_request(log_request)
    app.after_request(log_request)


def register_blueprints(app):
    app.register_blueprint(views.root.blueprint)
    app.register_blueprint(views.project.blueprint)
    app.blueprints['flask-api'] = views.theme.blueprint


def register_errors(app):
    # pylint: disable=unused-variable

    @app.errorhandler(500)
    def handle_500(error):
        log.exception(error)
        return {'message': "An unknown error has occurred."}, 500
