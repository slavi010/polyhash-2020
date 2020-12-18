from typing import List

from src.model.Etape import Etape
from src.model.ItemCase import ItemCase


class Tache:
    """Une tâche à accomplir
        Les tâches sont composées d'étapes par lesquelles les robots doivent passer afin de les accomplir
        Une tâche accomplie rapporte nombre de points donné
        """

    #Le nombre de points que la tâche rapporte une fois effectuée
    points: int

    # distance et surface totale entre chaque étape
    distance: float
    surface: float

    # centre de gravité moyen de la tâche
    centre_gravite: ItemCase
    distance_centre_gravite: float

    # le numero associé à une tâche
    numero: int

    # les étapes à effectuer triées dans l'ordre
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
        """Ajoute les étapes dans la tâche

        Liste ordonnée des étapes

        :param etape: la nouvelle étape à ajouter
        :type : Etape

        :return: Tache
        """
        assert etape is not None
        for e in self.etapes :
            assert e != etape

        self.etapes.append(etape)
        return self

    def __eq__(self, other):
        """Compare deux tâches entre elles afin de savoir si il s'agit de la même tâche
            Retourne vrai si cette instance et other ont le même numéro


            :param other: l'instance de Tache avec qui comparer la tâche actuelle

            :return: True si il s'agit de la même tâche
            :rtype: bool
        """
        assert isinstance(other, Tache)

        return self.numero == other.numero

    def __ne__(self, other):
        """Retourne vrai si cette instance et other ne sont pas le même numéro

            :param other: l'instance de Tache avec qui comparer la tâche actuelle
            :rtype: bool
        """
        return not self == other

    def __str__(self) -> str:
        """Renvoie la tâche sous forme de string
            La tâche sera écrite en tant que liste de ses étapes

            Exemple :
            Tâche: 1 {[1,3],[5,6]}

            :return: la tâche en str
            :rtype: str
        """

        ret = "Tâche: " + str(self.numero) + " {"
        for etape in self.etapes:
            ret += "[{},{}],".format(etape.x, etape.y)
        ret += "}"
        return ret


        str(self.point_montage.x) + ", " + str(self.point_montage.y)
