from typing import List

from src.model.Etape import Etape


class Tache:
    """Une tâche à acomplire"""

    points: int

    # les etapes a effectuer triée dans l'ordre
    etapes: List

    def __init__(self, points: int):
        self.points = points
        self.etapes = []

    def add_etape(self, etape: Etape):
        """Ajoute les étapes dans la tache

        Liste ordonnée des étapes

        :param etape: la nouvelle étape à ajouter
        :type : Etape
        """
        assert etape is not None
        for e in self.etapes :
            assert e != etape

        self.etapes.append(etape)
        return self
