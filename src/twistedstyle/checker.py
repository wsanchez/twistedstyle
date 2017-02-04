"""
Twisted style checker
"""

from typing import Iterable


class TwistedStyleChecker(object):
    """
    Twisted style checker
    """

    def __init__(self, filename: str, tree, lines) -> None:
        """
        :param filename: The name of the file to check.

        :param line: The line number in the file to check.

        :param tree: The AST tree of the file to check.
        """
        self.filename = filename
        self.tree = tree
        self.lines = lines

    def check(self) -> Iterable:
        """
        Run this checker.
        """
        yield "Hello there! {} :: {} :: {}".format(
            self.filename, self.lines, self.tree
        )
