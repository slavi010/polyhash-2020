from src.model.ItemCase import ItemCase
from src.model.Robot import Robot


class Bras(ItemCase):
    """Un morceau de bras d'un robot"""

    robot: Robot

    def __init__(self, x: int, y: int, robot: Robot):
        """

        :param x: position x
        :param y: position y
        :param grille: la grille de cette item
        :param robot: Le robot au quel ce morceau de bras est attaché
        """
        super().__init__(x, y)
        self.robot = robot

