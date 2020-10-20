from src.model.ItemCase import ItemCase


class PointMontage(ItemCase):
    """Un point de montage pour un Robot"""

    def __init__(self, x: int, y: int):
        """

        :param x: position x
        :param y: position y
        :param grille: la grille de cet item
        """
        super().__init__(x, y)