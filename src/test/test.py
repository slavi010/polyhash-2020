
"""Toutes les fonctions de test de l'application"""

from src.model.Grille import Grille
from src.model.ItemCase import ItemCase


def item_case_test():
    grille = Grille(10, 10)
    item_1 = ItemCase(2, 2, grille)
    item_2 = ItemCase(2, 2, grille)
    item_3 = ItemCase(5, 7, grille)

    assert item_1 == item_2
    assert not item_1 == item_3
    assert not item_1 != item_2
    assert item_1 != item_3
