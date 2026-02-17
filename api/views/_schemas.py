from webargs import core
from webargs.flaskparser import FlaskParser
from marshmallow import Schema, fields, pre_load, post_load
from flask_api.exceptions import ParseError
import log


parser = FlaskParser(("form", "data"))


@parser.location_handler("data")
def parse_data(request, name, field):
    return core.get_value(request.data, name, field)


class UnprocessableEntity(ParseError):
    status_code = 422


class ProjectSchema(Schema):
    unit = fields.Float()
    integration = fields.Float()
    overall = fields.Float()

    @pre_load
    def log_input(self, data, **_kwargs):
        log.debug("Input data: %r", data)
        return data

    @post_load
    def log_parsed(self, data, **_kwargs):
        log.debug("Parsed data: %r", data)
        return data

    def handle_error(self, error, data, **_kwargs):
        log.error("Unable to parse: %r", data)
        raise UnprocessableEntity(error.messages)
