from abc import ABCMeta, abstractmethod


class BasePlugin(metaclass=ABCMeta):  # pragma: no cover (abstract class)

    @abstractmethod
    def match(self, cwd):
        """Determine if the current directory contains coverage data.

        :return bool: Indicates the current directory can be processesed.

        """

    @abstractmethod
    def run(self, cwd):
        """Extract the coverage data from the current directory.

        :return float: Percentange of lines covered.

        """
