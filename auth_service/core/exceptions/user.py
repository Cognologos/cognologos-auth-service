from .abc import AbstractException, ConflictException, NotFoundException, UnauthorizedException


class UserException(AbstractException):
    """Base user exception."""


class UserNotFoundException(UserException, NotFoundException):
    """User not found."""

    detail = "User not found"


class UserUnauthorizedException(UserException, UnauthorizedException):
    """User unauthorized"""

    detail = "User unauthorized"


class UserDeletedException(UserException, ConflictException):
    """User deleted."""

    detail = "User deleted"
