"""
    __init__.py 
"""
__version__ = "0.1"

from .Boat import Boat
from .Coast import Coast
from .Field import Field
from .Game import Game
from .WGCPlayer import WGCPlayer 

__all__ = [
    "Boat",
    "Coast",
    "Field",
    "Game",
    "WGCPlayer",
    "__global__",
]
