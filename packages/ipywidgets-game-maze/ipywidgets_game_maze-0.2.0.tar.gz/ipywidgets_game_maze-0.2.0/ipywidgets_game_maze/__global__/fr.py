from ipywidgets_game_maze.MazePlayer import MazePlayer

__version__ = "0.1"


def LABY3D(niveau=0, UI=None):
    niveaux = {0: "lab/lab.json", 1: "lab/laby3d.json"}
    if not (niveau in niveaux):
        niveau = 0
    global lab
    lab = MazePlayer(maze=niveaux[niveau], UI=UI, language="fr_FR")
    return lab


def avancer():
    lab.move()


def regarder():
    return lab.look()


def droite():
    lab.right()


def gauche():
    lab.left()


def haut():
    lab.up()


def bas():
    lab.down()


def horizontale():
    lab.horizontal()


def restart():
    lab.reset()
