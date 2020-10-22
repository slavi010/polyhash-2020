from enum import Enum


class Mouvement(Enum):
    """Le mouvement d'un robot"""
    HAUT = "U"
    DROITE = "R"
    BAS = "D"
    GAUCHE = "L"
    ATTENDRE = "W"

    def __str__(self):
        return self.value
