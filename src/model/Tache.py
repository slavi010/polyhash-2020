from typing import List

from src.model.Etape import Etape


class Tache:
    """Une tâche à acomplire"""

    points: int

    # total distance entre chaque étape
    distance: int

    numero: int

    # les etapes a effectuer triée dans l'ordre
    etapes: List

    def __init__(self, points: int, numero: int):
        self.points = points
        self.etapes = []
        self.distance = 0
        self.numero = numero

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

    def __eq__(self, other):
        """Retourne vrai si cette instance et other ont le même numéro

            :param other: l'instance avec qui comparer
            :rtype: bool
        """
        assert isinstance(other, Tache)

        return self.numero == other.numero

    def __ne__(self, other):
        """Retourne vrai si cette instance et other ne sont pas le même numéro

            :param other: l'instance avec qui comparer
            :rtype: bool
        """
        return not self == other