import logging

from webargs import core
from webargs.flaskparser import FlaskParser
from marshmallow import Schema, fields, pre_load, post_load
from flask_api.exceptions import ParseError


parser = FlaskParser(('form', 'data'))
log = logging.getLogger(__name__)


@parser.location_handler('data')
def parse_data(request, name, field):
    return core.get_value(request.data, name, field)


class UnprocessableEntity(ParseError):
    status_code = 422


class ProjectSchema(Schema):
    unit = fields.Float()
    integration = fields.Float()
    overall = fields.Float()

    _pre = pre_load(lambda _, data: log.debug("Parsing data: %r", data))
    _post = post_load(lambda _, data: log.debug("Parsed data: %r", data))

    def handle_error(self, exc, data):
        log.error("Unable to parse: %r", data)
        raise UnprocessableEntity(exc.messages)

    class Meta:
        strict = True
