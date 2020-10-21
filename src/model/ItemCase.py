from src.model.Mouvement import Mouvement


class ItemCase:
    """Un élément dans la grille"""

    x: int
    y: int

    def __init__(self, x: int, y: int):
        """

        :param x: position x
        :param y: position y
        :param grille: la grille de cette item
        """
        # vérification des entrées
        assert x >= 0
        assert y >= 0

        self.x = x
        self.y = y

    def get_position(self, mouvement: Mouvement = None):
        """Retourner les coordonnées x et y après application d'un mouvement.

        :param mouvement: Le mouvement appliqué
        :type: Mouvement
        :return: x, y

        """
        if mouvement is None:
            return self.x, self.y
        else:
            if mouvement == Mouvement.HAUT:
                return self.x, self.y + 1
            elif mouvement == Mouvement.DROITE:
                return self.x + 1, self.y
            elif mouvement == Mouvement.BAS:
                return self.x, self.y - 1
            elif mouvement == Mouvement.GAUCHE:
                return self.x - 1, self.y + 1
            else:
                raise ValueError("Mouvement non reconnu !")

    def __eq__(self, other):
        """Retourne vrai si cette instance et other sont à la même place dans la même grille

            :param other: l'instance avec qui comparer
            :rtype: bool
        """
        assert isinstance(other, ItemCase)
        return self.x == other.x and \
            self.y == other.y

    def __ne__(self, other):
        """Retourne vrai si cette instance et other ne sont pas à la même place dans la même grille

            :param other: l'instance avec qui comparer
            :rtype: bool
        """
        return not self == other
