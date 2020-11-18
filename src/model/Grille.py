import heapq
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

        # vérifie les taches et mouvements des robots
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
        :return: Vrai si les coordonnées sont dans la grille
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
        """Ajoute la tache à la grille

        Place les étapes dans cases.
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
        100 pour le vide
        150 pour une etape

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
                            map[y - y1].append(150)
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
                        map[y - y1].append(100)
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

    def pathfinder(self, depart: ItemCase,
                   arrivee: Etape,
                   bras_robot: List,
                   carte: List,
                   x_offset: int,
                   y_offset: int):

        depart_coord = (depart.x, depart.y)
        arrivee_coord = (arrivee.x, arrivee.y)

        #openList liste cases à évaluer
        openList : list = []
        # openList.append(depart_coord)

        #closeList liste cases déjà évaluées
        closeList = set()

        #liste des parents de la case
        came_from = {}

        #f et g score
        #gscore : distance au pts de départ (nbr de case déjà traversée pour y arriver)
        #hscore : distance au pts d'arrivée (x arrivee - x current )² + (y arrivee - y current )²
        #fscore = hscore + gscore
        gscore = {depart_coord: 0}
        fscore = {depart_coord: (arrivee.x - depart.x) ** 2 + (arrivee.y - depart.y) ** 2}

        # ajouter depart à openList
        heapq.heappush(openList, (fscore[depart_coord], depart_coord))

        #tant que openList n'est pas vide ou qu'on est pas déjà sorti de la boucle
        while len(openList) > 0 :
            #current_case = la case dans openList ayant le fscore le plus petit
            current_case_coord: tuple = heapq.heappop(openList)[1]

            #mettre current dans closeList
            closeList.add(current_case_coord)

            #si current_case est l'arrivee
            if current_case_coord == arrivee_coord:
                chemin : list = []
                while current_case_coord in came_from:
                    chemin.append(current_case_coord)
                    current_case_coord = came_from[current_case_coord]
                return chemin[::-1]

            #liste des voisins de current: [X+1]/[x-1]/[y+1]/[y-1]
            voisin_offsets : list = [(1, 0),(-1, 0),(0, 1), (0, -1)]

            #pour tous les voisin dans voisins
            for voisin in voisin_offsets :

                coord_voisin_abs = (voisin[0] + current_case_coord[0], voisin[1] + current_case_coord[1])
                coord_voisin_relatif = (voisin[0] + current_case_coord[0] - x_offset, voisin[1] + current_case_coord[1] - y_offset)

                # si il n'est pas dans la grille
                if not self.dans_grille(coord_voisin_abs[0], coord_voisin_abs[1]):
                    continue
                if 0 <= coord_voisin_relatif[0] < len(carte[0]):
                    if not (0 <= coord_voisin_relatif[1] < len(carte)):
                        # array bound y walls
                        continue
                else:
                    # array bound x walls
                    continue

                # si on ne peux pas traverser le voisin ou que le voisin est dans DONE
                if (carte[coord_voisin_relatif[1]][coord_voisin_relatif[0]] < 1) or (coord_voisin_abs in closeList) :
                    continue
                    #aller au prochain voisin

                # si il s'agit du bras de notre robot
                if carte[coord_voisin_relatif[1]][coord_voisin_relatif[0]] == 1:
                    if len(bras_robot) >= 2 and (coord_voisin_abs[0] != bras_robot[-2].x or coord_voisin_abs[1] != bras_robot[-2].y): #ou -1 jsp ou ça commencera
                        continue
                        # il ne s'agit pas de rétractation

                #voisin g = current g + 1
                voisin_g_score: int = gscore[current_case_coord] + 1
                #voisin h = (x arrivee - x voisin )**2 + (y arrivee - y voisin )**2
                #voisin f = voisin g + voisin h + map[voisin[0]][voisin[1]]

                # si le new chemin jusqu'à ce voisin est + court (son g score est + petit avec ce nouveau chemin)
                # ou que le voisin n'est pas dan la openListe

                if voisin_g_score < gscore.get(coord_voisin_abs, 0) or coord_voisin_abs not in [i[1]for i in openList]:
                    came_from[coord_voisin_abs] = current_case_coord
                    gscore[coord_voisin_abs] = voisin_g_score
                    fscore[coord_voisin_abs] = voisin_g_score\
                                               + carte[coord_voisin_relatif[1]][coord_voisin_relatif[0]]\
                                               + (arrivee.x - coord_voisin_abs[0]) ** 2 + (arrivee.y - coord_voisin_abs[1]) ** 2
                    # openList.append(coord_voisin_abs)
                    heapq.heappush(openList, (fscore[coord_voisin_abs], coord_voisin_abs))

        return None

