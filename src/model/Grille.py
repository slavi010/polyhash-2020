from typing import List


class Grille:
    """La grille

    """

    longueur: int
    hauteur: int

    # cases[y][x]
    cases: List

    robots: List
    taches: List
    point_montage: List

    def __init__(self, longueur: int, hauteur: int):
        self.longueur = longueur
        self.hauteur = hauteur

        self.robots = []
        self.taches = []
        self.point_montage = []

        # init cases
        cases = []
        for idx_ligne in range(hauteur):
            cases.append([])
            for idx_colone in range(longueur):
                cases[idx_ligne].append([])
