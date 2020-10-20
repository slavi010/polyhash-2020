
"""Toutes les fonctions de test de l'application"""
from src.model.Etape import Etape
from src.model.Grille import Grille
from src.model.ItemCase import ItemCase
from src.model.PointMontage import PointMontage
from src.model.Tache import Tache


def item_case_test():
    grille = Grille(10, 10)
    item_1 = ItemCase(2, 2)
    item_2 = ItemCase(2, 2)
    item_3 = ItemCase(5, 7)

    assert item_1 == item_2
    assert not item_1 == item_3
    assert not item_1 != item_2
    assert item_1 != item_3


def grille_add_point_montage_test():
    grille = Grille(10, 10)
    point_montage_1 = PointMontage(5, 5)
    point_montage_2 = PointMontage(6, 4)
    point_montage_3 = PointMontage(5, 5)

    grille.add_point_montage(point_montage_1)
    grille.add_point_montage(point_montage_2)

    try :
        grille.add_point_montage(point_montage_3)
    except AssertionError:
        pass

def grille_add_tache_test():
    grille = Grille(10, 10)
    tache_1 = Tache(4)
    tache_2 = Tache(5)

    tache_1.add_etape(Etape(5, 6)).add_etape(Etape(6, 7))
    tache_2.add_etape(Etape(5, 6)).add_etape(Etape(8, 7))
    #TODO COntinuer