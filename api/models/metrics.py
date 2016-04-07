from collections import OrderedDict

import yorm
from yorm.types import Float, AttributeDictionary


@yorm.attr(unit=Float)
@yorm.attr(integration=Float)
@yorm.attr(overall=Float)
class Metrics(AttributeDictionary):

    def __init__(self, unit=0, integration=0, overall=0):
        super().__init__()
        self.unit = unit
        self.integration = integration
        self.overall = overall

    def __str__(self):
        return ("Unit: {self.unit}%, "
                "Integration: {self.integration}%, "
                "Overall: {self.overall}%").format(self=self)

    def __bool__(self):
        return bool(self.unit or self.integration or self.overall)

    @property
    def data(self):
        data = OrderedDict()
        data['unit'] = self.unit
        data['integration'] = self.integration
        data['overall'] = self.overall
        return data

    def reset(self):
        self.unit = 0
        self.integration = 0
        self.overall = 0
