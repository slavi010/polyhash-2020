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
