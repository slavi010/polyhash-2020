"""Se fichier contien les fonctions pour trouver une solution à la grille"""

import copy
import math
import random

from pathfinding.core.diagonal_movement import DiagonalMovement
from pathfinding.core.grid import Grid
from pathfinding.finder.a_star import AStarFinder

from src.model.Bras import Bras
from src.model.Grille import Grille
from src.model.ItemCase import ItemCase
from src.model.Mouvement import Mouvement
from src.model.PointMontage import PointMontage

MAX_STUCK = 20

def methode_naive(grille: Grille):
    """Une méthode très simple pour résoudre le problème"""
    # assigne les point de montage aux robots
    for idx_robot in range(len(grille.robots)):
        grille.robots[idx_robot].point_montage = grille.point_montages[idx_robot]

    # la grille qui va en live tester les solutions
    grille_live = copy.deepcopy(grille)
    # la grille qui contien la solution
    grille_solution = copy.deepcopy(grille)

    # assigne les taches et fait les démos
    while grille_live.step_simulation > 0:
        coordonnees_prochain_mouvement = []

        for idx_robot, robot in enumerate(grille_live.robots):
            if not len(robot.taches):
                # prochaine tâche
                prochaine_tache = robot.get_plus_proche_tache(grille_live)
                if prochaine_tache is not None:
                    # ajoute une nouvelle tâche
                    robot.add_tache(prochaine_tache, grille_live)
                    # on essaye de retrouver la tache corrspondante dans grille_solve
                    for tache in grille_solution.taches:
                        if tache == prochaine_tache:
                            grille_solution.robots[idx_robot].add_tache(prochaine_tache, grille_solution)

            prochain_mouvement: Mouvement = Mouvement.ATTENDRE
            pince: ItemCase = robot.coordonnees_pince()

            if len(robot.taches):
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
                    # om y a un bras ou un point de montage présent sur cette case ?
                    for item in grille_live.cases[y_new][x_new]:
                        if isinstance(item, Bras) or isinstance(item, PointMontage):
                            collision = True

                    if collision:
                        robot.mouvements.clear()
                    else:
                        prochain_mouvement = robot.mouvements[0]

                if not len(robot.mouvements) and robot.stucks < MAX_STUCK:
                    # il y a un tâche à accomplir
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
                        else:
                            prochain_mouvement = Mouvement.BAS

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
                        # collision = False
                        # x_new_colision, y_new_colision = robot.coordonnees_pince().get_position(
                        #     prochain_mouvement.rotation_90())
                        # # le prochain mouvement d'un autre bras a déjà réservé cette case ?
                        # if not grille_live.dans_grille(x_new_colision, y_new_colision):
                        #     collision = True
                        # else:
                        #     for idx_coordonnees in range(0, len(coordonnees_prochain_mouvement), 2):
                        #         if x_new_colision == coordonnees_prochain_mouvement[idx_coordonnees] and \
                        #                 y_new_colision == coordonnees_prochain_mouvement[idx_coordonnees + 1]:
                        #             collision = True
                        #     for item in grille_live.cases[y_new_colision][x_new_colision]:
                        #         if isinstance(item, Bras) or isinstance(item, PointMontage):
                        #             collision = True
                        # if collision:
                        #     collision = False
                        #     x_new_colision, y_new_colision = robot.coordonnees_pince().get_position(
                        #         prochain_mouvement.rotation_90(2))
                        #     if not grille_live.dans_grille(x_new_colision, y_new_colision):
                        #         collision = True
                        #     else:
                        #         for idx_coordonnees in range(0, len(coordonnees_prochain_mouvement), 2):
                        #             if x_new_colision == coordonnees_prochain_mouvement[idx_coordonnees] and \
                        #                     y_new_colision == coordonnees_prochain_mouvement[idx_coordonnees + 1]:
                        #                 collision = True
                        #         for item in grille_live.cases[y_new_colision][x_new_colision]:
                        #             if isinstance(item, Bras) or isinstance(item, PointMontage):
                        #                 collision = True
                        #     if collision:
                        #         prochain_mouvement = Mouvement.ATTENDRE
                        #     else:
                        #         prochain_mouvement = prochain_mouvement.rotation_90(2)
                        #
                        # else:
                        #     prochain_mouvement = prochain_mouvement.rotation_90()

                    # recherche d'un chemin plus optimisé
                    if prochain_mouvement == Mouvement.ATTENDRE or random.randint(2, 16) < robot.elargissement:
                        x_min = (pince.x if pince.x < robot.taches[0].etapes[0].x else robot.taches[0].etapes[0].x) - (1 + robot.elargissement)
                        y_min = (pince.y if pince.y < robot.taches[0].etapes[0].y else robot.taches[0].etapes[0].y) - (1 + robot.elargissement)
                        x_max = (pince.x if pince.x >= robot.taches[0].etapes[0].x else robot.taches[0].etapes[0].x) + (1 + robot.elargissement)
                        y_max = (pince.y if pince.y >= robot.taches[0].etapes[0].y else robot.taches[0].etapes[0].y) + (1 + robot.elargissement)
                        matrix = grille_live.to_matrix(x_min, y_min, x_max, y_max, robot)
                        # ajoute les prochains mouvements déjà programmé des autres bras
                        for idx_coordonnees in range(0, len(coordonnees_prochain_mouvement), 2):
                            if x_min <= coordonnees_prochain_mouvement[idx_coordonnees] <= x_max and \
                                    y_min <= coordonnees_prochain_mouvement[idx_coordonnees + 1] <= y_max:
                                matrix[coordonnees_prochain_mouvement[idx_coordonnees + 1] - y_min] \
                                    [coordonnees_prochain_mouvement[idx_coordonnees] - x_min] = -1
                        grid = Grid(matrix=matrix)
                        start = grid.node(pince.x - x_min, pince.y - y_min)
                        end = grid.node(robot.taches[0].etapes[0].x - x_min, robot.taches[0].etapes[0].y - y_min)
                        finder = AStarFinder(diagonal_movement=DiagonalMovement.never, weight=10)
                        path, runs = finder.find_path(start, end, grid)
                        # print(x_min, y_min, x_max, y_max)
                        # print(runs, path)
                        # print(grid.grid_str(path=path, start=start, end=end, show_weight=False))

                        for index_path in range(1, len(path)):
                            prochain_mouvement: Mouvement
                            if path[index_path][0] - path[index_path - 1][0] < 0:
                                prochain_mouvement = Mouvement.GAUCHE
                            elif path[index_path][0] - path[index_path - 1][0] > 0:
                                prochain_mouvement = Mouvement.DROITE
                            elif path[index_path][1] - path[index_path - 1][1] < 0:
                                prochain_mouvement = Mouvement.BAS
                            else:
                                prochain_mouvement = Mouvement.HAUT
                            robot.mouvements.append(prochain_mouvement)

            else:
                # pas de tache -> attente
                prochain_mouvement = Mouvement.ATTENDRE

            if prochain_mouvement == Mouvement.ATTENDRE:
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

            if len(robot.mouvements):
                prochain_mouvement = robot.mouvements[0]

            x_new, y_new = robot.coordonnees_pince().get_position(prochain_mouvement)
            coordonnees_prochain_mouvement.append(x_new)
            coordonnees_prochain_mouvement.append(y_new)

            if not len(robot.mouvements):
                robot.mouvements.append(prochain_mouvement)
            grille_solution.robots[idx_robot].mouvements.append(prochain_mouvement)

        # pourcentage de progression
        if int(math.floor((grille_live.step_simulation) / grille_solution.step_simulation * 1000)) \
                > int(math.floor((grille_live.step_simulation - 1) / grille_solution.step_simulation * 1000)):
            print((1000 - int(
                math.floor((grille_live.step_simulation - 1) / grille_solution.step_simulation * 1000))) / 10,
                  " %")
            # print(grille_live)
        grille_live.one_step_simulation()



    # supprime les tâches non finies
    for index_robot in range(len(grille_live.robots)):
        if len(grille_live.robots[index_robot].taches) > 0:
            grille_solution.robots[index_robot].taches.pop()
    if grille_live.longueur <= 100:
        print(grille_live)
    print("Points : ", grille_live.points)
    return grille_solution
