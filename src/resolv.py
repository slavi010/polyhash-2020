
"""Se fichier contien les fonctions pour trouver une solution à la grille"""
from src.model.Grille import Grille


def methode_naive(grille: Grille):
    """Une méthode très simple pour résoudre le problème"""
    # assigne les point de montage aux robots
    for idx_robot in range(len(grille.robots)):
        grille.robots[idx_robot].point_montage = grille.point_montages[idx_robot]

    # assigne les taches est fait les démos