"""
Modern Copper CRM integration package for Python.
"""

from .client import CopperClient
from .models.people import Person, PersonAddress
from .config import Settings

__version__ = "0.1.0"
__all__ = ["CopperClient", "Person", "PersonAddress", "Settings"]
