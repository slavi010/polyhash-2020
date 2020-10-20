from typing import List

from src.model.Bras import Bras
from src.model.Etape import Etape
from src.model.PointMontage import PointMontage
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

    def __init__(self, longueur: int, hauteur: int):
        self.longueur = longueur
        self.hauteur = hauteur

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
        """
        pass

    def one_step_simulation(self):
        """Avance la simulation à t+1

        Pour chaque Robot, fait bouger son bras avec son prochain mouvement.
        Si pas de prochain mouvement dans un des bras -> raise Error
        Si collision (ou bras hors grille) -> raise Error
        Actualise les taches actuelles (supprime les étapes de la tâche du robot au fur et à mesure)
        Si une tâche n'a plus d'étape, ajoute les points de la tâche et supprime la tâche du robot.

        """


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


        for etape in tache.etapes :

            for item in self.cases[etape.y][etape.x] :
                # si il y a un point de montage alors error
                if isinstance(item, PointMontage) :
                    raise ValueError
                # si il n'y a pas déjà d'étapes dans la case alors on l'ajoute
                elif not isinstance(item, Etape):
                    self.cases[etape.y][etape.x].append(etape)

            self.taches.append(etape)

        return self

    def __str__(self):
        """Renvoie la grille sous forme d'un str représentant une carte

        :return : La carte en deux dimenssions
        :rtype : str
        """
        map: str = ""
        for y in range(self.hauteur):
            for x in range(self.longueur):
                if len(self.cases[y][x]) > 0:
                    if isinstance(self.cases[y][x][0], PointMontage):
                        map += "O"
                    elif isinstance(self.cases[y][x][0], Bras):
                        map += "#"
                    elif isinstance(self.cases[y][x][0], Etape):
                        map += "x"
                else:
                    map += "."
            map += "\n"
