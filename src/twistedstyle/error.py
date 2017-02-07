"""
Error messages
"""

from attr import attrib, attrs


__all__ = ("TwistedStyleError")


@attrs
class TwistedStyleError(object):
    """
    Error from :class:`TwistedStyleChecker`.
    """

    message = attrib()
    node = attrib()
