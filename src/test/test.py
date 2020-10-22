
"""Toutes les fonctions de test de l'application"""
from src.model.Bras import Bras
from src.model.Etape import Etape
from src.model.Grille import Grille
from src.model.ItemCase import ItemCase
from src.model.Mouvement import Mouvement
from src.model.PointMontage import PointMontage
from src.model.Robot import Robot
from src.model.Tache import Tache


def item_case_test():
    item_1 = ItemCase(2, 2)
    item_2 = ItemCase(2, 2)
    item_3 = ItemCase(5, 7)

    assert item_1 == item_2
    assert not item_1 == item_3
    assert not item_1 != item_2
    assert item_1 != item_3


def item_case_get_position_test():
    item = ItemCase(2, 2)
    x, y = item.get_position(Mouvement.HAUT)
    assert x == 2 and y == 3
    x, y = item.get_position(Mouvement.DROITE)
    assert x == 3 and y == 2
    x, y = item.get_position(Mouvement.BAS)
    assert x == 2 and y == 1
    x, y = item.get_position(Mouvement.GAUCHE)
    assert x == 1 and y == 2


def grille_add_point_montage_test():
    grille = Grille(10, 10)
    point_montage_1 = PointMontage(5, 5)
    point_montage_2 = PointMontage(6, 4)
    point_montage_3 = PointMontage(5, 5)

    grille.add_point_montage(point_montage_1)
    grille.add_point_montage(point_montage_2)

    try:
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

def robot_faire_prochain_mouvement_retractation_test():
    grille = Grille(10, 10)
    point_montage = PointMontage(5, 5)
    grille.add_point_montage(point_montage)
    robot = Robot()
    robot.point_montage = point_montage
    robot.mouvements.append(Mouvement.DROITE)
    robot.mouvements.append(Mouvement.BAS)

    assert not robot.faire_prochain_mouvement_retractation(grille)

    # simulation mouvement haut
    bras = Bras(5, 6)
    robot.bras.append(bras)
    grille.cases[6][5].append(bras)

    # pas de rétractation car mouvement a droit et non vers le bas
    assert not robot.faire_prochain_mouvement_retractation(grille)
    robot.mouvements.pop(0)

    assert robot.faire_prochain_mouvement_retractation(grille)
    assert len(robot.bras) == 0
    for item in grille.cases[6][5]:
        assert not isinstance(item, Bras)


def robot_faire_prochain_mouvement_test():
    grille = Grille(10, 10)
    point_montage = PointMontage(5, 5)
    point_montage_bis = PointMontage(6, 6)
    grille.add_point_montage(point_montage)
    grille.add_point_montage(point_montage_bis)

    etape = Etape(5, 6)
    tache = Tache(15)
    tache.add_etape(etape)

    robot = Robot()
    robot.point_montage = point_montage
    robot.add_tache(tache)
    robot.mouvements.append(Mouvement.HAUT)
    robot.mouvements.append(Mouvement.DROITE)
    grille.robots.append(robot)

    # tout va bien
    robot.faire_prochain_mouvement(grille)
    assert len(grille.cases[6][5]) == 1 and isinstance(grille.cases[6][5][0], Bras)
    assert len(robot.bras) == 1
    assert len(robot.mouvements) == 1

    assert grille.points == 15
    assert not len(robot.taches)

    # collision avec point de montage bis
    try:
        robot.faire_prochain_mouvement(grille)
    except ConnectionError:
        pass
    else:
        assert False


def robot_coordonnees_pince_test():
    grille = Grille(10, 10)
    point_montage = PointMontage(5, 5)
    grille.add_point_montage(point_montage)

    robot = Robot()
    robot.point_montage = point_montage
    assert robot.coordonnees_pince() == robot.point_montage

    # simulation mouvement haut
    bras = Bras(5, 6)
    robot.bras.append(bras)
    grille.cases[6][5].append(bras)
    assert robot.coordonnees_pince() == bras



def grille_dans_grille_test():
    grille = Grille(10, 10)

    assert grille.dans_grille(5, 5)
    assert grille.dans_grille(0, 0)
    assert grille.dans_grille(9, 9)
    assert not grille.dans_grille(-1, 5)
    assert not grille.dans_grille(10, 5)


def robot_add_tache_test():
    grille = Grille(10, 10)
    point_montage = PointMontage(5, 5)
    etape_1 = Etape(5, 6)
    etape_2 = Etape(5, 7)
    tache = Tache(15)
    tache.add_etape(etape_1)
    tache.add_etape(etape_2)
    grille.add_tache(tache)
    robot = Robot()
    robot.point_montage = point_montage
    robot.add_tache(tache, grille)

    assert len(robot.taches)
    assert not len(grille.taches)


def robot_get_plus_proche_tache_test():
    grille = Grille(10, 10)
    point_montage = PointMontage(5, 5)
    etape_1 = Etape(5, 6)
    etape_2 = Etape(5, 7)
    tache = Tache(15)
    tache.add_etape(etape_1)
    tache.add_etape(etape_2)
    grille.add_tache(tache)
    robot = Robot()
    robot.point_montage = point_montage
    robot.add_tache(robot.get_plus_proche_tache(grille), grille)
    assert not robot.get_plus_proche_tache(grille)


def grill_start_simulation_test():
    grille = Grille(10, 10)
    grille.step_simulation = 2
    point_montage = PointMontage(5, 5)
    point_montage_bis = PointMontage(6, 6)
    grille.add_point_montage(point_montage)
    grille.add_point_montage(point_montage_bis)

    etape_1 = Etape(5, 6)
    etape_2 = Etape(5, 7)
    tache = Tache(15)
    tache.add_etape(etape_1)
    tache.add_etape(etape_2)
    grille.add_tache(tache)

    robot = Robot()
    robot.point_montage = point_montage
    robot.add_tache(tache,grille)
    robot.mouvements.append(Mouvement.HAUT)
    robot.mouvements.append(Mouvement.HAUT)
    grille.robots.append(robot)

    grille.start_simulation()
    print(grille.points)