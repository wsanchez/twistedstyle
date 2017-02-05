"""
Twisted style checker
"""

from ast import AST
from typing import Iterable, Sequence


__all__ = (
    "TwistedStyleError",
    "TwistedStyleChecker",
)


class TwistedStyleError(object):
    """
    Error from :class:`TwistedStyleChecker`.
    """

    def __init__(
        self, message: str, lineNumber: int, columnNumber: int
    ) -> None:
        """
        :param message: The error message.

        :param lineNumber: The line number corresponding to the error.

        :param columnNumber: The column number corresponding to the error.
        """
        self.message = message
        self.lineNumber = lineNumber
        self.columnNumber = columnNumber


class TwistedStyleChecker(object):
    """
    Twisted style checker
    """

    def __init__(self, filename: str, tree: AST, lines: Sequence[str]) -> None:
        """
        :param filename: The name of the file to check.

        :param line: The line number in the file to check.

        :param tree: The AST tree of the file to check.
        """
        self.filename = filename
        self.tree = tree
        self.lines = lines

    def check(self) -> Iterable[TwistedStyleError]:
        """
        Run this checker.

        :return: Any errors found in the file.
        """
        yield TwistedStyleError(
            message="Hello there!",
            lineNumber=0,
            columnNumber=0,
        )
