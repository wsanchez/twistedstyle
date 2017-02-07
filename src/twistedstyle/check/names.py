"""
Checker for Twisted naming conventions
"""

from enum import Enum
from os import sep as fileSeparator
from typing import Iterable, Tuple

from attr import attrib, attrs

from ..error import TwistedStyleError
from ..node import Node



@attrs
class TwistedNamesChecker(object):
    """
    Checker for Twisted naming conventions
    """

    class Message(Enum):
        """
        Message IDs for :class:`TwistedNamesChecker`.
        """

        # 1xx: Modules
        N101 = 'test module name must use "test_" prefix'

        # 2xx: Classes

        # 3xx: Methods
        N301 = "invalid name for method"
        N302 = "invalid name for test method"

        # 4xx: Functions

    filename = attrib()
    rootNode = attrib()
    lines = attrib()

    def check_Module(
        self, node: Node, parents=Tuple[Node]
    ) -> Iterable[TwistedStyleError]:
        """
        Visit a module.
        """
        if hasattr(self, "_isTestModule"):
            raise RuntimeError("Module within module not expected")

        pathSegments = self.filename.split(fileSeparator)

        if "test" in pathSegments:
            self._isTestModule = True
        else:
            self._isTestModule = False

    def check_ClassDef(
        self, node: Node, parents=Tuple[Node]
    ) -> Iterable[TwistedStyleError]:
        """
        Visit a class definition.
        """
        if self._isTestModule:
            for name in node.baseClassNames:
                if name.endswith("TestCase"):
                    # We have a test class in a test module.
                    if not self.filename[-1].startswith("test_"):
                        yield TwistedStyleError(self.Message.N101, None)
