from collections import OrderedDict

import yorm
from yorm.converters import Float


@yorm.attr(unit=Float)
@yorm.attr(integration=Float)
@yorm.attr(overall=Float)
@yorm.sync("data/{self.owner}/{self.repo}/{self.branch}.yml")
class Project(object):

    def __init__(self, owner, repo, branch='master'):
        self.owner = owner
        self.repo = repo
        self.branch = branch
        self.unit = 0.0
        self.integration = 0.0
        self.overall = 0.0

    def __str__(self):
        return ("Unit: {self.unit}%, "
                "Integration: {self.integration}%, "
                "Overall: {self.overall}%").format(self=self)

    @property
    def metrics(self):
        data = OrderedDict()
        data['unit'] = self.unit
        data['integration'] = self.integration
        data['overall'] = self.overall
        return data

    def update(self, data, exception=ValueError):
        if not data:
            raise exception("No metrics provided.")

        message = OrderedDict()
        for name in ['unit', 'integration', 'overall']:
            current = data.get(name)
            if current is not None:
                previous = getattr(self, name)
                if current < previous:
                    msg = "Value dropped below minimum: {}".format(previous)
                    message[name] = [msg]
                else:
                    setattr(self, name, current)

        if message:
            raise exception(message)

    def reset(self):
        self.unit = 0.0
        self.integration = 0.0
        self.overall = 0.0
