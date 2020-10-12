from enum import Enum


class Mouvement(Enum):
    """Le mouvement d'un robot"""
    HAUT = 0
    DROITE = 1
    BAS = 2
    GAUCHE = 3
