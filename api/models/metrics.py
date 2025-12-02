from collections import OrderedDict
from dataclasses import dataclass


@dataclass
class Metrics:

    unit: float = 0
    integration: float = 0
    overall: float = 0

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
