"""
Flake8 plugin
"""

from typing import Iterable

from .checker import Checker
from .version import version


class Flake8Plugin(object):
    """
    Flake8 plugin
    """

    name = "twisted"
    version = version

    def __init__(self, filename: str, line: int, tree: object) -> None:
        """
        :param filename: The name of the file to check.

        :param line: The line number in the file to check.

        :param tree: The AST tree of the file to check.
        """
        self.checker = Checker(filename, tree, line)

    def run(self) -> Iterable:
        """
        Run this plugin.
        """
        for error in self.checker.check():
            yield error
