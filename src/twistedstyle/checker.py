"""
Twisted style checker
"""

from typing import Iterable

from attr import attrib, attrs


@attrs
class Checker(object):
    """
    Twisted style checker
    """

    filename = attrib()
    tree = attrib()
    line = attrib()

    def check(self) -> Iterable:
        """
        Run this checker.
        """
        print(self.filename, self.line, self.tree)
