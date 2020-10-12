from src.model.Grille import Grille
from src.model.ItemCase import ItemCase


class Etape(ItemCase):
    """Une étape d'une Tâche"""

    def __init__(self, x: int, y: int, grille: Grille):
        """

        :param x: position x
        :param y: position y
        :param grille: la grille de cette item
        """
        super().__init__(x, y, grille)