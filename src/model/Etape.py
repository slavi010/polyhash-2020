from src.model.ItemCase import ItemCase


class Etape(ItemCase):
    """Etape : Une étape d'une Tâche"""

    # le temps estimer pour aller à cette etape (en effectuant la tâche)
    # utilisé par le simulateur
    temps: int = 0
    temps_aller_retour: int = 0

    def __init__(self, x: int, y: int):
        """

        :param x: position x
        :param y: position y
        :param grille: la grille de cette item
        """
        super().__init__(x, y)
