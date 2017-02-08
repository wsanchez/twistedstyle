"""
AST node.
"""

from ast import iter_child_nodes
from enum import Enum
from typing import Iterable

from attr import attrib, attrs



@attrs
class Node(object):
    """
    AST node.
    """

    class NodeType(Enum):
        """
        Node types.
        """
        Module = object()
        Class = object()
        Method = object()
        Function = object()


    class NodeTypeError(TypeError):
        """
        Wrong node type for requested operation.
        """


    nodeTypeMap = dict(
        Module=NodeType.Module,
        ClassDef=NodeType.Class,
    )

    astNode = attrib()


    def __str__(self):
        nodeType = self.type
        if nodeType is None:
            nodeType = "{{{}}}".format(self.astNode.__class__.__name__)
        else:
            nodeType = nodeType.name

        pos = self.filePosition
        if pos:
            pos = "@{}".format(pos)

        name = self.name
        if name:
            name = "({})".format(name)
        else:
            name = ""

        return "{nodeType}{name}{position}".format(
            nodeType=nodeType, name=name, position=pos
        )


    @property
    def name(self):
        """
        The identifier (symbol name) for this node.
        """
        if hasattr(self.astNode, "id"):
            return self.astNode.id
        else:
            return None


    @classmethod
    def _nodeTypeFromASTClass(cls, astClass):
        astClassName = astClass.__name__

        nodeType = cls.nodeTypeMap.get(astClassName, None)
        if nodeType is not None:
            return nodeType

        if astClassName == "FunctionDef":
            return cls.NodeType.Function

        return None


    @property
    def type(self):
        """
        The type of this node.
        This corresponds to the underlying AST class name.
        """
        if not hasattr(self, "_type"):
            self._type = self._nodeTypeFromASTClass(self.astNode.__class__)
        return self._type


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
            raise self.NodeTypeError("Not a ClassDef: {}".format(self))

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
