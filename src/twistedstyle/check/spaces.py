"""
Checker for Twisted naming conventions
"""

from enum import Enum
from typing import Iterable, Tuple

from attr import attrib, attrs

from ..error import TwistedStyleError
from ..node import Node


__all__ = ("TwistedSpacesChecker")



@attrs
class TwistedSpacesChecker(object):
    """
    Checker for Twisted spacing conventions
    """

    class Message(Enum):
        """
        Message IDs for :class:`TwistedSpacesChecker`.
        """

        # 1xx: Modules

        # 2xx: Classes
        S201 = 'class def must follow 3 blank lines'

        # 3xx: Methods

        # 4xx: Functions
        S401 = 'function def must follow 2 blank lines'

    filename = attrib()
    rootNode = attrib()
    lines = attrib()


    def check_Class(
        self, node: Node, parents=Tuple[Node]
    ) -> Iterable[TwistedStyleError]:
        """
        Visit a class definition.
        """
        for line in node.nearbyLines(self.lines, pre=3, post=-1):
            if not self.isBlankLine(line):
                yield TwistedStyleError(self.Message.S201, node, repr(line))
                break


    def check_Function(
        self, node: Node, parents=Tuple[Node]
    ) -> Iterable[TwistedStyleError]:
        """
        Visit a function definition.
        """
        for line in node.nearbyLines(self.lines, pre=2, post=-1):
            if not self.isBlankLine(line):
                yield TwistedStyleError(self.Message.S401, node, repr(line))
                break


    @staticmethod
    def isBlankLine(line: str) -> bool:
        """
        Check that a line is blank.
        """
        return line.strip() == ""
