"""
Flake8 plugin
"""

from typing import Iterable

from .checker import TwistedStyleChecker
from .version import version


__all__ = (
    "TwistedStyleExtension",
)



class TwistedStyleExtension(object):
    """
    Twisted style Flake8 extension
    """

    name = "twisted-style"
    version = version

    def __init__(self, tree, filename: str, lines=None) -> None:
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
        for error in self.checker.check():
            message = "t{} {}".format(error.message.name, error.message.value)
            if error.example is not None:
                message = "{}: {}".format(message, error.example)

            yield (
                error.node.lineNumber,
                error.node.columnNumber,
                message,
                type(self)
            )
