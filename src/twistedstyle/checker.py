"""
Master Twisted style checker
"""

import sys
from ast import AST, NodeVisitor, iter_child_nodes
from typing import Iterable, Sequence, Tuple

from twisted.logger import Logger, textFileLogObserver


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
    Master Twisted style checker
    """

    def __init__(self, filename: str, tree: AST, lines: Sequence[str]) -> None:
        """
        :param filename: The name of the file to check.

        :param lines: The lines in the file to check.

        :param tree: The AST tree of the file to check.
        """
        #
        # This weirdness is because we are a plugin, which is to say we aren't
        # the "application", so it's not appropriate for us to start the global
        # log observer, as we'd potentially be competing with another plugin
        # trying to do the same thing.
        #
        if not hasattr(self.__class__, "logObserver"):
            self.__class__.logObserver = textFileLogObserver(sys.stdout)

        if not hasattr(self.__class__, "_log"):
            self.__class__._log = Logger(observer=self.__class__.logObserver)

        self.filename = filename
        self.tree = tree
        self.lines = lines
        self._visitor = CheckerNodeVisitor(master=self)

    def check(self) -> Iterable[TwistedStyleError]:
        """
        Run this checker.

        :return: Any errors found in the file.
        """
        self._log.debug(
            "Checking file: {filename}", filename=self.filename
        )
        self._visitor.visit(self.tree)

        return ()


class CheckerNodeVisitor(NodeVisitor):
    """
    Node visitor for :class:`TwistedStyleChecker`.
    """

    def __init__(self, master: TwistedStyleChecker) -> None:
        self._master = master

        if not hasattr(self.__class__, "_log"):
            self.__class__._log = Logger(observer=master.logObserver)

    def visit(self, node: AST, _parents: Tuple[AST] = ()) -> None:
        self._log.debug(
            "{indent}{node.__class__.__name__}",
            indent=". " * len(_parents),
            node=node,
        )

        childParents = _parents + (node,)
        for child in iter_child_nodes(node):
            self.visit(child, childParents)
