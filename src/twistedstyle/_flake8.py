"""
Flake8 plugin
"""

from .version import version


class Flake8Plugin(object):
    """
    Flake8 plugin
    """

    name = "twisted"
    version = version

    def __init__(self, filename, tree):
        """
        :param filename:
            The name of the file being checked.

        :param tree:
            The AST tree for the file being checked.
        """
        pass
