from typing import List

from src.model.Bras import Bras
from src.model.Etape import Etape
from src.model.PointMontage import PointMontage
from src.model.Robot import Robot
from src.model.Tache import Tache


class Grille:
    """La grille

    """

    longueur: int
    hauteur: int

    step_simulation: int = 0

    # cases[y][x]
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
        cases = []
        for idx_ligne in range(hauteur):
            cases.append([])
            for idx_colone in range(longueur):
                cases[idx_ligne].append([])

    def start_simulation(self):
        """Lance la simulation

        Va dérouler l'algo de chaque robot à chaque instant t.
        """

    def one_step_simulation(self):
        """Avance la simulation à t+1

        Pour chaque Robot, fait bouger son bras avec son prochain mouvement.
        Si pas de prochain mouvement -> raise Error
        Si pas 
        """


    def add_point_montage(self, point_montage: PointMontage):
        """Ajoute le point de montage à la grille

        l'ajoute à point_montages + le place dans cases

        :param point_montage: Le point de montage à ajouter
        :return: Grille
        """

        assert point_montage is not None

        # TODO add_point_montage
        return self

    def add_etape(self, tache: Tache):
        """Ajoute l'etape à la grille

        Place l'étape dans casesèk.
        Si il y a déjà une étape aux coordonnées de la nouvelle étape,
        ne rien faire.

        :param point_montage: Le point de montage à ajouter
        :return: Grille
        """

        assert tache is not None

        # TODO add_etape
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
