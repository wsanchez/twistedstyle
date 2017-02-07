"""
Twisted style checker
"""

import sys
from ast import AST
from typing import Iterable, Sequence, Tuple

from twisted.logger import Logger, textFileLogObserver

from .check.names import TwistedNamesChecker
from .check.spaces import TwistedSpacesChecker
from .error import TwistedStyleError
from .node import Node


__all__ = ("TwistedStyleChecker")


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
        self.rootNode = Node(tree)
        self.lines = lines

        checkerArguments = dict(
            filename=self.filename,
            rootNode=self.rootNode,
            lines=tuple(self.lines),
        )

        self.checkers = set((
            TwistedNamesChecker(**checkerArguments),
            TwistedSpacesChecker(**checkerArguments),
        ))

    def check(self) -> Iterable[TwistedStyleError]:
        """
        Run this checker.

        :return: Any errors found in the file.
        """
        self._log.debug(
            "Checking file: {filename}", filename=self.filename
        )

        return self.checkNode(self.rootNode)

    def checkNode(self, node: Node, _parents: Tuple[Node] = ()) -> None:
        """
        Check a node.

        :param node: The node to check.
        """
        self._log.debug(
            "{log_source.filename}: {indent}{node.type} ({node.filePosition})",
            indent=". " * len(_parents),
            node=node,
        )

        checkMethodName = "check_{}".format(node.type)

        for checker in self.checkers:
            check = getattr(checker, checkMethodName, None)
            if check is not None:
                messages = check(node, parents=_parents)
                if messages is not None:
                    for message in messages:
                        yield message

        childParents = _parents + (node,)
        for child in node.children():
            for message in self.checkNode(child, childParents):
                yield message
