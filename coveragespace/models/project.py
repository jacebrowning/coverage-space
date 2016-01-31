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

    @property
    def metrics(self):
        data = OrderedDict()
        data['unit'] = self.unit
        data['integration'] = self.integration
        data['overall'] = self.overall
        return data

    @metrics.setter
    def metrics(self, data):
        self.unit = data.get('unit', self.unit)
        self.integration = data.get('integration', self.integration)
        self.overall = data.get('overall', self.overall)

    def reset(self):
        self.unit = 0.0
        self.integration = 0.0
        self.overall = 0.0
