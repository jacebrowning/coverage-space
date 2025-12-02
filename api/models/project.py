from collections import OrderedDict
from pathlib import Path

from datafiles import datafile, field
import log

from .metrics import Metrics


@datafile("./data/{self.owner}/{self.repo}/{self.branch}.yml")
class Project:

    THRESHOLD = 0.5

    owner: str
    repo: str
    branch: str = 'main'
    current: Metrics = field(default_factory=Metrics)
    minimum: Metrics = field(default_factory=Metrics)

    def __post_init__(self):
        self._create_readme()

    def __str__(self):
        if self.minimum:
            return str(self.current)

        return "Reset minimum metrics"

    @property
    def slug(self) -> str:
        return f'{self.owner}/{self.repo}'

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

    def _create_readme(self):
        readme = Path('data') / self.owner / self.repo / 'README.md'
        if not readme.exists():
            readme.parent.mkdir(parents=True, exist_ok=True)
            with readme.open('w') as f:
                f.write(f'[{self.slug}](https://github.com/{self.slug})')

    def update(self, data, *, exception=ValueError):
        message = OrderedDict()

        for name in ['unit', 'integration', 'overall']:
            current = data.get(name)
            if current is not None:
                setattr(self.current, name, current)
                minimum = getattr(self.minimum, name)
                if minimum - current > self.THRESHOLD:
                    msg = "Value dropped below minimum: {}".format(minimum)
                    message[name] = [msg]
                else:
                    log.debug("New minimum %s: %s", name, current)
                    setattr(self.minimum, name, current)

        if message:
            raise exception(message)

    def reset(self):
        self.minimum.reset()
