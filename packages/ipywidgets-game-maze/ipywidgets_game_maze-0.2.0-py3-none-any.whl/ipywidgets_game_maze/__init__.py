"""
__init__.py for ipywidgets_game_maze
"""
__version__ = "0.1"
from .Object3D import Object3D
from .StaticObject import StaticObject
from .Ant import Ant
from .Maze import Maze
from .MazePlayer import MazePlayer

__all__ = [
    "Object3D",
    "StaticObject",
    "Ant",
    "Maze",
    "MazePlayer"
]


def _jupyter_nbextension_paths():
    return [
        dict(section="notebook", src="static", dest="ipywidgets_game_maze", require="")
    ]
