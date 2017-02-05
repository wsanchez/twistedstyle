"""
Twisted style checker
"""

from ast import AST, NodeVisitor, iter_child_nodes
from typing import Iterable, Sequence, Tuple


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

        :param lines: The lines in the file to check.

        :param tree: The AST tree of the file to check.
        """
        self.filename = filename
        self.tree = tree
        self.lines = lines
        self._visitor = CheckerNodeVisitor()

    def check(self) -> Iterable[TwistedStyleError]:
        """
        Run this checker.

        :return: Any errors found in the file.
        """
        self._visitor.visit(self.tree)

        return ()


class CheckerNodeVisitor(NodeVisitor):
    """
    Node visitor for :class:`TwistedStyleChecker`.
    """

    def visit(self, node: AST, _parents: Tuple[AST] = ()) -> None:
        print("{}{}".format(".   " * len(_parents), node))

        childParents = _parents + (node,)
        for child in iter_child_nodes(node):
            self.visit(child, childParents)
