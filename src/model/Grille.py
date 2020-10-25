from typing import List, Union

from src.model.Bras import Bras
from src.model.Etape import Etape
from src.model.ItemCase import ItemCase
from src.model.PointMontage import PointMontage
from src.model.Robot import Robot
from src.model.Tache import Tache


class Grille:
    """La grille

    """

    longueur: int
    hauteur: int

    step_simulation: int = 0

    # cases[y][x] : y est la hauteur et x la largeur
    cases: List

    robots: List
    taches: List
    point_montages: List

    points: int

    def __init__(self, longueur: int, hauteur: int):
        self.longueur = longueur
        self.hauteur = hauteur

        self.points = 0

        self.robots = []
        self.taches = []
        self.point_montages = []

        # init cases
        self.cases = []
        for idx_ligne in range(hauteur):
            self.cases.append([])
            for idx_colone in range(longueur):
                self.cases[idx_ligne].append([])

    def start_simulation(self):
        """Lance la simulation

        Va dérouler l'algo de chaque robot à chaque instant t.

        Doit vérifier que les robots ont finis toutes leurs taches et mouvement.
        """

        while self.step_simulation > 0:
            self.one_step_simulation()

        # vérifie les taches et mouvement des robots
        for robot in self.robots:
            if len(robot.taches):
                raise ValueError("Une tâche assignée n'est pas finie !!!")
            if len(robot.mouvements):
                raise ValueError("Il reste des mouvements au robot !!!")

    def one_step_simulation(self):
        """Avance la simulation à t+1

        Pour chaque Robot, fait bouger son bras avec son prochain mouvement.
        Si pas de prochain mouvement dans un des robots -> raise Error
        Si collision (ou bras hors grille) -> raise Error
        Si step_simulation == 0 -> raise Error
        Actualise les taches actuelles (supprime les étapes de la tâche du robot au fur et à mesure)
        Si une tâche n'a plus d'étape, ajoute les points de la tâche et supprime la tâche du robot.

        """

        if not self.step_simulation:
            raise ValueError("La simulation est finie !")
        self.step_simulation -= 1

        # vérifie si chaque robot a au moins un mouvement
        for robot in self.robots:
            if not len(robot.mouvements):
                raise AttributeError("Un robot n'a pas de prochain mouvement !")

        robots = self.robots.copy()
        # fait bouger chaque robot avec des mouvements de rétractation
        for robot in self.robots:
            if robot.faire_prochain_mouvement_retractation(self):
                robots.remove(robot)

        # fait bouger tous les autres robots
        for robot in robots:
            robot.faire_prochain_mouvement(self)

    def dans_grille(self, x: int, y: int):
        """Retourne Vrai si les coordonnées sont dans la grille

        Faux sinon

        :param x: La coordonnée x
        :type: int
        :param y: La coordonnée y
        :type: int
        :return: Vrai sin les coordonnées sont dans la grille
        :rtype: bool
        """
        return 0 <= x < self.longueur and \
            0 <= y < self.hauteur



    def add_point_montage(self, point_montage: PointMontage):
        """Ajoute le point de montage à la grille

        l'ajoute à point_montages + le place dans cases

        :param point_montage: Le point de montage à ajouter
        :return: Grille
        """

        assert point_montage is not None
        # vérifier si la case est vide
        assert len(self.cases[point_montage.y][point_montage.x]) == 0

        self.cases[point_montage.y][point_montage.x].append(point_montage)
        self.point_montages.append(point_montage)

        return self

    def add_tache(self, tache: Tache):
        """Ajoute l'etape à la grille

        Place l'étape dans cases.
        Si il y a déjà une étape aux coordonnées de la nouvelle étape,
        ne rien faire.

        :param tache: La tache à ajouter
        :return: Grille
        """

        assert tache is not None
        assert len(tache.etapes) > 0

        for etape in tache.etapes:
            deja_etape = False
            for item in self.cases[etape.y][etape.x]:
                # si il y a un point de montage alors error
                if isinstance(item, PointMontage):
                    raise ValueError("Il ya déjà un point de montage à la case, ajout de l'étape impossible")
                # si il n'y a pas déjà d'étapes dans la case alors on l'ajoute
                elif isinstance(item, Etape):
                    deja_etape = True
            if not deja_etape:
                self.cases[etape.y][etape.x].append(etape)

        self.taches.append(tache)

        return self

    def to_matrix(self, x1: int, y1: int, x2: int, y2: int, robot: Robot = None) -> List:
        """Renvoie la grille sous forme d'une matrice.

        0 pour un point de montage
        -1 pour un bras d'autre robots (avec ou sons etape)
        1 pour les bras du robot actuel (si lieu)
        5 pour le vide
        7 pour une etape

        :param robot: Le point de vue du robot actuel (notamment pour la rétractation)
        :return : La carte en deux dimenssions
        :rtype : List
        """
        assert x1 <= x2
        assert y1 <= y2

        map: List = []
        if robot is not None:
            pince = robot.coordonnees_pince()

        for y in range(y1, y2 + 1):
            map.append([])
            for x in range(x1, x2 + 1):
                if x < 0 or x >= self.longueur or y < 0 or y >= self.hauteur:
                    map[y - y1].append(-2)
                else:
                    if len(self.cases[y][x]) == 1:
                        if isinstance(self.cases[y][x][0], PointMontage):
                            map[y - y1].append(0)
                        elif isinstance(self.cases[y][x][0], Bras):
                            # le bras du robot ?
                            ok = False
                            if robot is not None \
                                    and (pince == self.cases[y][x][0] or
                                         (len(robot.bras) > 2 and self.cases[y][x][0] == robot.bras[-2]) or
                                         (len(robot.bras) == 1 and self.cases[y][x][0] == robot.point_montage)):
                                ok = True
                                map[y - y1].append(1)
                            if not ok:
                                map[y - y1].append(-1)
                        elif isinstance(self.cases[y][x][0], Etape):
                            map[y - y1].append(7)
                    elif len(self.cases[y][x]) == 2:
                        ok = False
                        if robot is not None \
                                and (pince == self.cases[y][x][0] or
                                  (len(robot.bras) > 2 and self.cases[y][x][0] == robot.bras[-2]) or
                                  (len(robot.bras) == 1 and self.cases[y][x][0] == robot.point_montage)):
                            ok = True
                            map[y - y1].append(1)
                        if not ok:
                            map[y - y1].append(-1)
                    else:
                        map[y - y1].append(5)
        return map

    def __str__(self):
        """Renvoie la grille sous forme d'un str représentant une carte

        :return : La carte en deux dimenssions
        :rtype : str
        """
        map: str = ""
        for y in range(self.hauteur-1, -1, -1):
            map += str(y) + '\t'
            for idx, x in enumerate(range(self.longueur)):
                if idx % 10 == 0:
                    map += " "
                if len(self.cases[y][x]) == 1:
                    if isinstance(self.cases[y][x][0], PointMontage):
                        map += "O"
                    elif isinstance(self.cases[y][x][0], Bras):
                        map += "B"
                    elif isinstance(self.cases[y][x][0], Etape):
                        map += "x"
                elif len(self.cases[y][x]) == 2:
                    map += "#"
                else:
                    map += "."
            map += "\n"
        return map