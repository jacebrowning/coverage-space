import logging
from collections import OrderedDict

import yorm

from .metrics import Metrics

log = logging.getLogger(__name__)


@yorm.attr(current=Metrics)
@yorm.attr(minimum=Metrics)
@yorm.sync("data/{self.owner}/{self.repo}/{self.branch}.yml")
class Project:

    def __init__(self, owner, repo, branch='master'):
        self.owner = owner
        self.repo = repo
        self.branch = branch
        self.current = Metrics()
        self.minimum = Metrics()

    def __str__(self):
        return str(self.current)

    @property
    def current_metrics(self):
        return self.current.data

    @property
    def minimum_metrics(self):
        return self.minimum.data

    @property
    def metrics(self):
        data = OrderedDict()
        data['current'] = self.current_metrics
        data['minimum'] = self.minimum_metrics
        return data

    def update(self, data, *, exception=ValueError):
        if not data:
            raise exception("No metrics provided.")

        message = OrderedDict()
        for name in ['unit', 'integration', 'overall']:
            current = data.get(name)
            if current is not None:
                setattr(self.current, name, current)
                minimum = getattr(self.minimum, name)
                if current < minimum:
                    msg = "Value dropped below minimum: {}".format(minimum)
                    message[name] = [msg]
                else:
                    log.debug("New minimum %s: %s", name, current)
                    setattr(self.minimum, name, current)

        if message:
            raise exception(message)

    def reset(self):
        self.minimum.reset()
