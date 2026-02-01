"""Business logic methods for User model.

Import and attach these to the User model as needed, or use as standalone functions.
"""
from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .models import User


def get_display_name(user: User) -> str:
    """Return the best display name for the user."""
    if user.first_name and user.last_name:
        return f"{user.first_name} {user.last_name}"
    if user.first_name:
        return user.first_name
    return user.username or user.email
