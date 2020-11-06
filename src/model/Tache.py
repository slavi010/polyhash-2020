from typing import List

from src.model.Etape import Etape
from src.model.ItemCase import ItemCase


class Tache:
    """Une tâche à accomplir"""

    points: int

    # total distance et surface entre chaque étape
    distance: float
    surface: float
    # centre de gravité moyen
    centre_gravite: ItemCase
    distance_centre_gravite: float

    numero: int

    # les étapes a effectuer triée dans l'ordre
    etapes: List

    def __init__(self, points: int, numero: int):
        self.surface = 0
        self.points = points
        self.etapes = []
        self.distance = 0
        self.numero = numero
        self.centre_gravite = None
        self.distance_centre_gravite = 0

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

    def __str__(self) -> str:
        ret = "Tâche: " + str(self.numero) + " {"
        for etape in self.etapes:
            ret += "[{},{}],".format(etape.x, etape.y)
        ret += "}"
        return ret


        str(self.point_montage.x) + ", " + str(self.point_montage.y)
