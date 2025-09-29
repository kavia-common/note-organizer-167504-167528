"""
Routes package initializer.

Exposes blueprints for convenient imports in the app factory.
"""
from .health import blp as health_blp  # noqa: F401
from .notes import blp as notes_blp  # noqa: F401
