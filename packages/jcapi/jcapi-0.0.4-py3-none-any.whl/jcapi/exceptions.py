"""Exceptions for JC."""


class JCError(Exception):
    """Generic JC exception."""


class JCEmptyResponseError(Exception):
    """JC empty API response exception."""


class JCConnectionError(JCError):
    """JC connection exception."""


class JCConnectionTimeoutError(JCConnectionError):
    """JC connection Timeout exception."""
