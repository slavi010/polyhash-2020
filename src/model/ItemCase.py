from src.model.Grille import Grille


class ItemCase:
    """Un élément dans la grille"""

    x: int
    y: int
    grille: Grille

    def __init__(self, x: int, y: int, grille: Grille):
        """

        :param x: position x
        :param y: position y
        :param grille: la grille de cette item
        """
        # vérification des entrées
        assert grille is not None
        assert grille.longueur > 0 and grille.hauteur > 0
        assert x >= 0 and x < grille.longueur
        assert y >= 0 and y < grille.hauteur

        self.x = x
        self.y = y
        self.grille = grille

    def __eq__(self, other):
        """Retourne vrai si cette instance et other sont à la même place dans la même grille

            :param other: l'instance avec qui comparer
            :rtype: bool
        """
        assert isinstance(other, ItemCase)
        return self.grille == other.grille and \
            self.x == other.x and \
            self.y == other.y

    def __ne__(self, other):
        """Retourne vrai si cette instance et other ne sont pas à la même place dans la même grille

            :param other: l'instance avec qui comparer
            :rtype: bool
        """
        return not self == other
