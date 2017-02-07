"""
AST node.
"""

from ast import iter_child_nodes
from typing import Iterable

from attr import attrib, attrs



@attrs
class Node(object):
    """
    AST node.
    """

    astNode = attrib()


    @property
    def name(self):
        """
        The identifier (symbol name) for this node.
        """
        return self.astNode.id


    @property
    def type(self):
        """
        The type of this node.
        This corresponds to the underlying AST class name.
        """
        return self.astNode.__class__.__name__


    @property
    def lineNumber(self):
        """
        The line number corresponding to this node, if known, `None` otherwise.
        """
        return getattr(self.astNode, "lineno", None)


    @property
    def columnNumber(self):
        """
        The column number corresponding to this node, if known, `None`
        otherwise.
        """
        return getattr(self.astNode, "col_offset", None)


    @property
    def filePosition(self):
        """
        The file position corresponding to this node, expressed as a string
        in the form `"{line}:{column}"`.
        """
        info = []

        lineNumber = self.lineNumber
        if lineNumber is not None:
            info.append(str(lineNumber))

            columnNumber = self.columnNumber
            if columnNumber is not None:
                info.append(str(columnNumber))

        return ":".join(info)


    def children(self) -> Iterable:
        """
        Look up the children of this node.
        """
        for child in iter_child_nodes(self.astNode):
            yield Node(child)


    def baseClassNames(self):
        """
        Look up the base class of this `ClassDef` node.
        """
        if self.type != "ClassDef":
            raise AssertionError("baseClassNames() call on non-ClassDef node")

        for child in self.children():
            if child.type == "Name":
                yield child.name


    def nearbyLines(self, lines, pre=3, post=3, numbered=False):
        """
        Look up the lines of code nearby to this node.
        """
        mid = self.lineNumber - 1
        low = mid - pre
        high = mid + post + 1

        if low < 0:
            low = 0

        if high > len(lines):
            high = len(lines)

        if numbered:
            return (
                "{}: {}".format(i + 1, lines[i])
                for i in range(low, high)
            )
        else:
            return iter(lines[low:high])
