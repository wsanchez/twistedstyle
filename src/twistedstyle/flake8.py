"""
Flake8 plugin
"""

from typing import Iterable

from .checker import TwistedStyleChecker
from .version import version


class TwistedStyleExtension(object):
    """
    Twisted style Flake8 extension
    """

    name = "twisted-style"
    version = version

    def __init__(self, filename: str, tree, lines) -> None:
        """
        :param filename: The name of the file to check.

        :param line: The line number in the file to check.

        :param tree: The AST tree of the file to check.
        """
        self.checker = TwistedStyleChecker(
            filename=filename, tree=tree, lines=lines
        )

    def run(self) -> Iterable:
        """
        Run this plugin.
        """
        for message in self.checker.check():
            yield (1, 1, "t001 {}".format(message), type(self))
