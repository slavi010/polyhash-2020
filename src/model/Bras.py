from src.model.ItemCase import ItemCase


class Bras(ItemCase):
    """Bras : Un morceau de bras d'un robot"""

    def __init__(self, x: int, y: int):
        """

        :param x: position x
        :param y: position y
        :param grille: la grille de cette item
        """
        super().__init__(x, y)

