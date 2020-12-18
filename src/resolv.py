"""Ce fichier contient les fonctions pour trouver une solution à la grille"""

import copy
import math
import os
import random
from typing import Tuple

from pathfinding.core.diagonal_movement import DiagonalMovement
from pathfinding.core.grid import Grid
from pathfinding.finder.a_star import AStarFinder
from pathfinding.finder.dijkstra import DijkstraFinder

from src.debug_canvas import DebugCanvas
from src.model.Bras import Bras
from src.model.Grille import Grille
from src.model.ItemCase import ItemCase
from src.model.Mouvement import Mouvement
from src.model.PointMontage import PointMontage
from src.model.Tache import Tache
from src.model.TypeMap import TypeMap

# méthode (plus si naive que ça ) pour répondre au problème
def methode_naive(
        #initialisation des variables
        grille: Grille, # grille modélisant le cas à résoudre
        map: TypeMap,  # le cas donn à résoudre (sélection dans fichier 'main')
        MAX_STUCK: int,
        FACTEUR_DISTANCE_RETRACTATION: int,
        MAX_DIST_PM: int,
        ADDITION: Tuple, # un tuple qui contient les valeurs de pondération pour chaque cas
        FACTEUR_CONCENTRATION_BRAS: float = 1,
        affichage_graphique: bool = True,
        affichage_console: bool = True):
    """Une méthode très simple pour résoudre le problème"""

    random.shuffle(grille.point_montages)

    # assigne les point de montage aux robots
    # grille.robots[0].point_montage = grille.point_montages[0]
    # for idx_robot in range(len(grille.robots)):
    #     point_montage_max: PointMontage = None
    #     distance_max = 0
    #     for point_montage in grille.point_montages:
    #         distance_min = 9999
    #         for idx_robot_2 in range(idx_robot):
    #             if distance_min > point_montage.distance(grille.robots[idx_robot_2].point_montage):
    #                 distance_min = point_montage.distance(grille.robots[idx_robot_2].point_montage)
    #         if distance_min > distance_max:
    #             point_montage_max = point_montage
    #             distance_max = distance_min
    #     grille.robots[idx_robot].point_montage = point_montage_max
    #     # grille.robots[idx_robot].point_montage = grille.point_montages[idx_robot]

    # f_decentralized
    # point_montage_deja_pris = []
    # for idx_robot in range(len(grille.robots)):
    #     point_montage_min: PointMontage = None
    #     distance_min = 9999999
    #     for point_montage in grille.point_montages:
    #         ok = True
    #         for pm in point_montage_deja_pris:
    #             if pm == point_montage:
    #                 ok = False
    #         if ok:
    #             distance = min(point_montage.x, grille.longueur - point_montage.x, point_montage.y, grille.hauteur - point_montage.y)
    #             if distance_min > distance:
    #                 point_montage_min = point_montage
    #                 distance_min = distance
    #     point_montage_deja_pris.append(point_montage_min)
    #     grille.robots[idx_robot].point_montage = point_montage_min

    # c_few_arms
    point_montage_deja_pris = []
    for idx_robot in range(len(grille.robots)):
        point_montage_min: PointMontage = None
        total_facteur_min = 9999999
        for point_montage in grille.point_montages:
            ok = True
            for pm in point_montage_deja_pris:
                if point_montage.distance(pm) < math.sqrt(grille.longueur*grille.hauteur/len(grille.robots))*FACTEUR_CONCENTRATION_BRAS:
                    ok = False
                if pm == point_montage:
                    ok = False
            # f_decentralized
            if map == TypeMap.F:
                if 40 < min(point_montage.x, grille.longueur - point_montage.x, point_montage.y, grille.hauteur - point_montage.y):
                    ok = False

            if ok:
                total_facteur = 0
                for tache in grille.taches:
                    total_facteur += point_montage.distance(tache.centre_gravite)*tache.distance/(tache.points+1)
                if total_facteur_min > total_facteur:
                    point_montage_min = point_montage
                    total_facteur_min = total_facteur
        if point_montage_min is not None:
            point_montage_deja_pris.append(point_montage_min)
            grille.robots[idx_robot].point_montage = point_montage_min

    nb_robot_sans_pm = 0
    for robot in grille.robots:
        if robot.point_montage is None:
            nb_robot_sans_pm += 1
    if nb_robot_sans_pm:
        raise ValueError(f'Il y a {nb_robot_sans_pm} robot(s) qui n\'ont pas de point de montage assigné. '
                         f'Pensez à réduire la valeur de FACTEUR_DISTANCE_RETRACTATION.')


    # for i in range(len(grille.robots) - 100):
    #     grille.robots.pop(random.randint(0, len(grille.robots) - 1))

    # la grille qui va en live tester les solutions
    grille_live = copy.deepcopy(grille)
    # la grille qui contien la solution
    grille_solution = copy.deepcopy(grille)

    if affichage_graphique:
        debug_canvas: DebugCanvas = DebugCanvas(grille_live,
                                                cells_size=int(1200 / (grille_live.longueur + grille_live.hauteur)))

    stated_time = os.times()[0]

    # assigne les taches et fait les démos
    while grille_live.step_simulation > 0:
        coordonnees_prochain_mouvement = []

        for idx_robot, robot in enumerate(grille_live.robots):
            if affichage_graphique and grille_live.step_simulation == grille.step_simulation:
                debug_canvas.update()

            pince: ItemCase = robot.coordonnees_pince()

            if len(robot.bras) > (grille_live.longueur + grille_live.hauteur) * 1:
                robot.stucks = MAX_STUCK

            if robot.stucks == MAX_STUCK:
                robot.mouvements.clear()

            if not len(robot.taches) and len(grille_live.taches):
                # oblige la rétractation après finition d'une tâche

                # prochaine tâche
                # prochaine_tache = robot.get_tache_plus_rentable(grille_live)
                intersection_min = 9999999
                prochaine_tache: Tache = None
                facteur_max = 999999
                distance_pince_min = 999999

                # calcule
                # for robot_for_tache in grille_live.robots:
                #     if len(robot_for_tache.taches):
                #         tache = robot_for_tache.taches[0]
                #         tache.etapes[0].temps = robot_for_tache.coordonnees_pince().distance(tache.etapes[0])
                #         for etape_from, etape_to in zip(tache.etapes[0::1], tache.etapes[1::1]):
                #             etape_to.temps = etape_from.distance(etape_to) + etape_from.temps

                for tache in grille_live.taches:
                    intersection = 0
                    if tache.distance * 1.4 > grille_live.step_simulation:
                        intersection += 99999
                        facteur += 999999

                    # # intersection entre la tâche et les étapes
                    # tache.etapes[0].temps = pince.distance(tache.etapes[0])
                    # for etape_from, etape_to in zip(tache.etapes[0::1], tache.etapes[1::1]):
                    #     etape_to.temps = etape_from.distance(etape_to) + etape_from.temps
                    # tache.etapes[-1].temps_aller_retour = tache.etapes[-1].temps
                    # if len(tache.etapes) >= 2:
                    #     for etape_to, etape_from in zip(tache.etapes[-1:1:-1], tache.etapes[-2:0:-1]):
                    #         etape_from.temps_aller_retour = etape_to.temps_aller_retour \
                    #                                         + etape_to.temps - etape_from.temps
                    #     tache.etapes[0].temps_aller_retour = tache.etapes[1].temps_aller_retour \
                    #                                          + tache.etapes[1].temps - tache.etapes[0].temps

                    # etapes = []
                    # for etape in robot.etapes_done:
                    #     etapes.append(etape)
                    # etapes.append(pince)
                    # for etape in tache.etapes:
                    #     etapes.append(etape)
                    #
                    # for robot_for_tache in grille_live.robots:
                    #     robot_for_tache_pince = robot_for_tache.coordonnees_pince()
                    #
                    #     etapes_robot = []
                    #     for etape in robot_for_tache.etapes_done:
                    #         etapes_robot.append(etape)
                    #     etapes_robot.append(robot_for_tache_pince)
                    #     for tache_robot in robot_for_tache.taches:
                    #         for etape_robot in tache_robot.etapes:
                    #             etapes_robot.append(etape_robot)
                    #
                    #     for etape_from, etape_to in zip(etapes[0::1], etapes[1::1]):
                    #         for robot_etape_from, robot_etape_to in zip(etapes_robot[0::1], etapes_robot[1::1]):
                    #             if intersect_rectangle(etape_from, etape_to, robot_etape_from, robot_etape_to):
                    #                 # if robot_etape_from.temps < etape_from.temps_aller_retour + 1:
                    #                 intersection += 1

                    # for etape_from_1, etape_to_1 in zip(tache.etapes[0::1], tache.etapes[1::1]):
                    #     for etape_from_2, etape_to_2 in zip(tache.etapes[0::1], tache.etapes[1::1]):
                    #         if etape_to_1 != etape_from_2 and etape_to_2 != etape_from_1 and etape_from_1 != etape_from_2:
                    #             if intersect_rectangle(etape_from_1, etape_to_1, etape_from_2, etape_to_2):
                    #                 intersection += 1

                    # for etape_from, etape_to in zip(tache.etapes[0::1], tache.etapes[1::1]):
                    #     for robot_for_tache in grille_live.robots:
                    #         robot_for_tache_pince = robot_for_tache.coordonnees_pince()
                    #         for tache_robot in robot_for_tache.taches:
                    #             for robot_etape_from, robot_etape_to in zip(tache_robot.etapes[0::1],
                    #                                                         tache_robot.etapes[1::1]):
                    #                 if intersect_rectangle(etape_from, etape_to, robot_etape_from, robot_etape_to):
                    #                     # if robot_etape_from.temps < etape_from.temps_aller_retour + 1:
                    #                     intersection += 1
                    #                 # pince vers première étape
                    #                 if intersect_rectangle(pince, tache.etapes[0], robot_etape_from, robot_etape_to):
                    #                     intersection += 1
                    #         if len(robot_for_tache.taches) and intersect_rectangle(pince, tache.etapes[0], robot_for_tache_pince, robot_for_tache.taches[0].etapes[0]):
                    #             intersection += 1
                    #         # etapes déjà faites pour chaque robots
                    #         for robot_etape_from, robot_etape_to in zip(robot_for_tache.etapes_done[0::1],
                    #                                                     robot_for_tache.etapes_done[1::1]):
                    #             if intersect_rectangle(etape_from, etape_to, robot_etape_from, robot_etape_to):
                    #                 intersection += 1
                    #             if etape_from == etape_to:
                    #                 intersection += 1
                    #         # au niveau du bras
                    #         if (len(robot_for_tache.taches) and intersect_rectangle(etape_from, etape_to,
                    #                                                       robot_for_tache.coordonnees_pince(),
                    #                                                       robot_for_tache.taches[0].etapes[0])) \
                    #                 or (len(robot_for_tache.etapes_done) and intersect_rectangle(etape_from, etape_to,
                    #                                                            robot_for_tache.coordonnees_pince(),
                    #                                                            robot_for_tache.etapes_done[-1])):
                    #             intersection += 1
                    # for etape_from_1, etape_to_1 in zip(tache.etapes[0::1], tache.etapes[1::1]):
                    #     for etape_from_2, etape_to_2 in zip(tache.etapes[0::1], tache.etapes[1::1]):
                    #         if etape_to_1 != etape_from_2 and etape_to_2 != etape_from_1 and etape_from_1 != etape_from_2:
                    #             if intersect_rectangle(etape_from_1, etape_to_1, etape_from_2, etape_to_2):
                    #                 intersection += 1

                    # facteur = tache.etapes[0].surface(robot.point_montage)
                    facteur = tache.distance + tache.etapes[0].distance(robot.point_montage)
                    facteur = facteur/tache.points


                    # f et e
                    max_distance_from_pm = 0
                    for etape in tache.etapes:
                        distance = etape.distance(robot.point_montage)
                        if distance > max_distance_from_pm:
                            max_distance_from_pm = distance

                    facteur = (facteur+ADDITION[0])\
                              * (tache.centre_gravite.distance(robot.point_montage) + ADDITION[1])\
                              * (tache.distance_centre_gravite+ADDITION[2])\
                              * (intersection+ADDITION[3])

                    if facteur_max > facteur\
                            and max_distance_from_pm < MAX_DIST_PM :
                        intersection_min = intersection
                        facteur_max = facteur
                        distance_pince_min = facteur
                        prochaine_tache = tache

                if prochaine_tache is not None:
                    if affichage_console:
                        print(" --> Nouvelle tâche assignée : distance: ", str(prochaine_tache.etapes[0].distance(robot.point_montage)), ", etapes: ", len(prochaine_tache.etapes),
                              ", min intersection: ", intersection_min, ", facteur: ", int(facteur_max), ", ",
                              prochaine_tache.points, " points")

                    # ajoute une nouvelle tâche
                    robot.add_tache(prochaine_tache, grille_live)
                    # on essaye de retrouver la tache corrspondante dans grille_solve
                    for tache in grille_solution.taches:
                        if tache == prochaine_tache:
                            grille_solution.robots[idx_robot].add_tache(prochaine_tache, grille_solution)

            prochain_mouvement: Mouvement = Mouvement.ATTENDRE

            if len(robot.taches) and robot.stucks < MAX_STUCK:
                # toujours d'actu?
                if len(robot.mouvements):
                    # collision ?
                    collision = False
                    x_new, y_new = robot.coordonnees_pince().get_position(robot.mouvements[0])

                    # le prochain mouvement d'un autre bras a déjà réservé cette case ?
                    for idx_coordonnees in range(0, len(coordonnees_prochain_mouvement), 2):
                        if x_new == coordonnees_prochain_mouvement[idx_coordonnees] and \
                                y_new == coordonnees_prochain_mouvement[idx_coordonnees + 1]:
                            collision = True
                    # il y a un bras ou un point de montage présent sur cette case ?
                    for item in grille_live.cases[y_new][x_new]:
                        if isinstance(item, Bras) or isinstance(item, PointMontage):
                            collision = True

                    if collision:
                        robot.mouvements.clear()
                    else:
                        prochain_mouvement = robot.mouvements[0]

                # se rétracter est plus intéressant ?
                retractation = False
                if len(robot.taches):
                    distance_pince_etape = pince.distance(robot.taches[0].etapes[0])
                    for idx_bras, bras in enumerate(robot.bras[::(len(robot.bras)//10 + 1)]):
                        if bras.distance(robot.taches[0].etapes[0]) + (len(robot.bras) - idx_bras)/FACTEUR_DISTANCE_RETRACTATION < distance_pince_etape:
                            retractation = True

                if not len(robot.mouvements) and not retractation:


                    # il y a une tâche à accomplir
                    # bouge vers l'etape correspondante

                    x_diff: int = robot.taches[0].etapes[0].x - pince.x
                    y_diff: int = robot.taches[0].etapes[0].y - pince.y

                    if abs(x_diff) > abs(y_diff):
                        # en x
                        if x_diff > 0:
                            prochain_mouvement = Mouvement.DROITE
                        else:
                            prochain_mouvement = Mouvement.GAUCHE
                    else:
                        # en y
                        if y_diff > 0:
                            prochain_mouvement = Mouvement.HAUT
                        elif y_diff > 0:
                            prochain_mouvement = Mouvement.BAS
                        else:
                            prochain_mouvement = Mouvement.ATTENDRE

                    # collision ?
                    x_new, y_new = robot.coordonnees_pince().get_position(prochain_mouvement)

                    collision = False

                    # le prochain mouvement d'un autre bras a déjà réservé cette case ?
                    for idx_coordonnees in range(0, len(coordonnees_prochain_mouvement), 2):
                        if x_new == coordonnees_prochain_mouvement[idx_coordonnees] and \
                                y_new == coordonnees_prochain_mouvement[idx_coordonnees + 1]:
                            collision = True
                    # om y a un bras ou un point de montage présent sur cette case ?
                    for item in grille_live.cases[y_new][x_new]:
                        if isinstance(item, Bras) or isinstance(item, PointMontage):
                            collision = True

                    if collision:

                        prochain_mouvement = Mouvement.ATTENDRE

                    # recherche d'un chemin plus optimisé
                    if prochain_mouvement == Mouvement.ATTENDRE:
                        x_min = max((pince.x if pince.x < robot.taches[0].etapes[0].x else robot.taches[0].etapes[0].x) - (
                                1 + robot.elargissement), 0)
                        y_min = max((pince.y if pince.y < robot.taches[0].etapes[0].y else robot.taches[0].etapes[0].y) - (
                                1 + robot.elargissement), 0)
                        x_max = min((pince.x if pince.x >= robot.taches[0].etapes[0].x else robot.taches[0].etapes[0].x) + (
                                1 + robot.elargissement), grille_live.longueur - 1)
                        y_max = min((pince.y if pince.y >= robot.taches[0].etapes[0].y else robot.taches[0].etapes[0].y) + (
                                1 + robot.elargissement), grille_live.hauteur - 1)
                        matrix = grille_live.to_matrix(x_min, y_min, x_max, y_max, robot)
                        # ajoute les prochains mouvements déjà programmé des autres bras
                        for idx_coordonnees in range(0, len(coordonnees_prochain_mouvement), 2):
                            if x_min <= coordonnees_prochain_mouvement[idx_coordonnees] <= x_max and \
                                    y_min <= coordonnees_prochain_mouvement[idx_coordonnees + 1] <= y_max:
                                matrix[coordonnees_prochain_mouvement[idx_coordonnees + 1] - y_min] \
                                    [coordonnees_prochain_mouvement[idx_coordonnees] - x_min] = -1



                        # grid = Grid(matrix=matrix)
                        # start = grid.node(pince.x - x_min, pince.y - y_min)
                        # end = grid.node(robot.taches[0].etapes[0].x - x_min, robot.taches[0].etapes[0].y - y_min)
                        # finder = AStarFinder(diagonal_movement=DiagonalMovement.only_when_no_obstacle)
                        # path, runs = finder.find_path(start, end, grid)

                        start = robot.coordonnees_pince()
                        end = robot.taches[0].etapes[0]
                        path = grille_live.pathfinder(start, end, robot.bras, matrix, x_min, y_min)




                        # print(x_min, y_min, x_max, y_max)
                        # print(runs, path)
                        # print(grid.grid_str(path=path, start=start, end=end, show_weight=False))

                        if path is not None:
                            for index_path in range(0, len(path)):
                                # if 0 == path[index_path][0] and 209 == path[index_path][1]:
                                #     for line in matrix:
                                #         print(line)
                                #     print(path)
                                #     print(grille_live)
                                #     print("ok")

                                prochain_mouvement: Mouvement

                                x_diff = path[index_path][0] - (path[index_path - 1][0] if index_path != 0 else start.x)
                                y_diff = path[index_path][1] - (path[index_path - 1][1] if index_path != 0 else start.y)
                                if x_diff < 0 and y_diff < 0:
                                    robot.mouvements.append(Mouvement.GAUCHE)
                                    prochain_mouvement = Mouvement.BAS
                                elif x_diff < 0 and y_diff == 0:
                                    prochain_mouvement = Mouvement.GAUCHE
                                elif x_diff < 0:
                                    robot.mouvements.append(Mouvement.GAUCHE)
                                    prochain_mouvement = Mouvement.HAUT
                                elif x_diff == 0 and y_diff < 0:
                                    prochain_mouvement = Mouvement.BAS
                                elif x_diff == 0:
                                    prochain_mouvement = Mouvement.HAUT
                                elif x_diff > 0 and y_diff < 0:
                                    robot.mouvements.append(Mouvement.DROITE)
                                    prochain_mouvement = Mouvement.BAS
                                elif x_diff > 0 and y_diff == 0:
                                    prochain_mouvement = Mouvement.DROITE
                                else:
                                    robot.mouvements.append(Mouvement.DROITE)
                                    prochain_mouvement = Mouvement.HAUT
                                robot.mouvements.append(prochain_mouvement)

            else:
                # pas de tache -> attente
                prochain_mouvement = Mouvement.ATTENDRE

            if len(robot.mouvements):
                prochain_mouvement = robot.mouvements[0]

            if prochain_mouvement == Mouvement.ATTENDRE:
                # supprime les étapes déjà visité lors de la rétractation
                if len(robot.bras) and len(robot.etapes_done) and robot.bras[-1] == robot.etapes_done[-1]:
                    robot.etapes_done.pop()

                if len(robot.bras) >= 2:
                    if robot.bras[-2].x - robot.bras[-1].x < 0:
                        prochain_mouvement = Mouvement.GAUCHE
                    elif robot.bras[-2].x - robot.bras[-1].x > 0:
                        prochain_mouvement = Mouvement.DROITE
                    elif robot.bras[-2].y - robot.bras[-1].y < 0:
                        prochain_mouvement = Mouvement.BAS
                    else:
                        prochain_mouvement = Mouvement.HAUT
                elif len(robot.bras) == 1:
                    if robot.point_montage.x - robot.bras[-1].x < 0:
                        prochain_mouvement = Mouvement.GAUCHE
                    elif robot.point_montage.x - robot.bras[-1].x > 0:
                        prochain_mouvement = Mouvement.DROITE
                    elif robot.point_montage.y - robot.bras[-1].y < 0:
                        prochain_mouvement = Mouvement.BAS
                    else:
                        prochain_mouvement = Mouvement.HAUT
                else:
                    robot.stucks = 0
                    robot.etapes_done.clear()
                    robot.etapes_done.append(robot.point_montage)




            x_new, y_new = robot.coordonnees_pince().get_position(prochain_mouvement)
            coordonnees_prochain_mouvement.append(x_new)
            coordonnees_prochain_mouvement.append(y_new)

            if not len(robot.mouvements):
                robot.mouvements.append(prochain_mouvement)
            grille_solution.robots[idx_robot].mouvements.append(prochain_mouvement)



        grille_live.one_step_simulation()
        # pourcentage de progression
        if int(math.floor((grille_live.step_simulation) / grille_solution.step_simulation * 1000)) \
                > int(math.floor((grille_live.step_simulation - 1) / grille_solution.step_simulation * 1000)):
            pourcentage = (1000 - int(
                math.floor((grille_live.step_simulation - 1) / grille_solution.step_simulation * 1000))) / 10
            temps_estime = math.floor((os.times()[0] - stated_time) / (pourcentage + 0.000000001) * (100 - pourcentage))
            total_point_en_cours = 0
            total_tache_restante = len(grille_live.taches)
            for robot in grille_live.robots:
                for tache in robot.taches:
                    total_tache_restante += 1
                    total_point_en_cours += tache.points
            if affichage_console:
                print(pourcentage, " %, ",
                      temps_estime // 60, " min ", str(temps_estime % 60), "sec, ",
                      grille_live.points // 1000, " K points, ",
                      total_tache_restante, " taches restantes, ",
                      total_point_en_cours, " points en cours")
            if affichage_graphique:
                debug_canvas.update()
        # print(grille_live)



    # supprime les tâches non finies
    for index_robot in range(len(grille_live.robots)):
        if len(grille_live.robots[index_robot].taches) > 0:
            grille_solution.robots[index_robot].taches.pop()
    if affichage_console:
        print(grille_live)
        print("Points : ", grille_live.points)
    grille_solution.points = grille_live.points
    return grille_solution


def ccw(A: ItemCase, B: ItemCase, C: ItemCase):
    return (C.y - A.y) * (B.x - A.x) > (B.y - A.y) * (C.x - A.x)


# Return true if line segments AB and CD intersect
def intersect(A: ItemCase, B: ItemCase, C: ItemCase, D: ItemCase):
    return ccw(A, C, D) != ccw(B, C, D) and ccw(A, B, C) != ccw(A, B, D)



def intersect_rectangle(A: ItemCase, B: ItemCase, C: ItemCase, D: ItemCase):
    x_min = A.x if A.x < B.x else B.x
    x_max = A.x if A.x > B.x else B.x
    y_min = A.y if A.y < B.y else B.y
    y_max = A.y if A.y > B.y else B.y
    pts = [(C.x, C.y), (D.x, D.y), (C.x, D.y), (D.x, C.y)]
    for pt in pts:
        if x_min < pt[0] < x_max and y_min < pt[1] < y_max:
            return False

    # if B.x < C.x or D.x < A.x or B.y < C.y or D.y < A.y:
    #     return False
    return True
