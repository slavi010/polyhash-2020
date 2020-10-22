from typing import List
import math

from src.model.Bras import Bras
from src.model.ItemCase import ItemCase
from src.model.Mouvement import Mouvement
from src.model.PointMontage import PointMontage
from src.model.Tache import Tache


class Robot:
    """Un robot"""

    point_montage: PointMontage
    bras: List
    taches: List
    mouvements: List

    def __init__(self):
        self.bras = []
        self.taches = []
        self.mouvements = []

    def faire_prochain_mouvement_retractation(self, grille):
        """Fait une rétractation et renvoie True si le prochain mouvement est une rétractation.

        False sinon

        :param grille: La grille du robot
        :type: Grille
        :return: Vrai si une rétractation est faite
        :rtype: bool
        """
        assert len(self.mouvements) > 0

        # le bras est déjà sur son point de montage ?
        if len(self.bras) == 0:
            return False

        # le prochain mouvement est d'attendre ?
        if self.mouvements[0] == Mouvement.ATTENDRE:
            return False

        # prochaines coordonnées après application du mouvement
        x_new, y_new = self.coordonnees_pince().get_position(self.mouvements[0])
        if (len(self.bras) == 1 and x_new == self.point_montage.x and y_new == self.point_montage.y) or (len(self.bras) >= 2 and x_new == self.bras[-2].x and y_new == self.bras[-2].y):
            # C'est une rétractation
            # suppression du bras dans cases
            bras_pince = self.coordonnees_pince()
            for item in grille.cases[bras_pince.y][bras_pince.x]:
                if isinstance(item, Bras):
                    grille.cases[bras_pince.y][bras_pince.x].remove(item)

            self.bras.pop()
            self.mouvements.pop(0)
            return True

    def faire_prochain_mouvement(self, grille):
        """Fait le prochain mouvement du robot.

        Ne prend pas en compte la rétractation !!!

        :param grille: La grille du robot
        :type: Grille
        """
        assert len(self.mouvements) > 0

        # le prochain mouvement n'est pas d'attendre ?
        if self.mouvements[0] != Mouvement.ATTENDRE:
            # prochaines coordonnées après application du mouvement
            x_new, y_new = self.coordonnees_pince().get_position(self.mouvements[0])

            # dans la grille ?
            if not grille.dans_grille(x_new, y_new):
                raise TabError("Mouvement hors de la grille !")

            # collision ?
            for item in grille.cases[y_new][x_new]:
                if isinstance(item, Bras) or isinstance(item, PointMontage):
                    raise ConnectionError("COLLISION !!! x.x")

            # Tout est ok, ajoute une nouvelle extension de bras
            bras = Bras(x_new, y_new)
            self.bras.append(bras)
            grille.cases[y_new][x_new].append(bras)

            # Une étape faite ?
            if len(self.taches):
                if self.taches[0].etapes[0] == self.coordonnees_pince():
                    self.taches[0].etapes.pop(0)
                    # tâche finie ?
                    if not len(self.taches[0].etapes):
                        # ajoute les points
                        grille.points += self.taches[0].points
                        self.taches.pop(0)

        self.mouvements.pop(0)
        return self

    def coordonnees_pince(self):
        """Renvoie l'itemCase de la pince (La dernière extrépité du bras ou le point de montage)

        :rtype: ItemCase
        """
        if not len(self.bras):
            # la pince est au point de montage
            return self.point_montage
        else:
            # prend le dernier bras
            return self.bras[-1]

    def add_tache(self, tache: Tache, grille):
        """Assigne la tache au robot

        Ajoute la tache comme dernière tache au robot.
        Supprime la tache dans grille.

        :param tache: La tache à assigner
        :param grille: La grille
        """
        assert tache is not None
        assert grille is not None

        self.taches.append(tache)
        grille.taches.remove(tache)

        return self

    def get_plus_proche_tache(self, grille):
        """Retourne la plus proche tâche non déjà assignée par rapport à la pince

        La distance est évaluée à vol d'oiseaux.
        On considère la première étape de la tâche comme position.
        Renvoie None s'il n'y a plus de tâche disponible.

        :return: soit une tache, soit None si pas de tâche dispo
        :rtype: Tache, None
        """
        assert grille is not None

        if not len(grille.taches):
            return None

        pince: ItemCase = self.coordonnees_pince()

        tache_min = None
        distance_min = 9999999
        for tache in grille.taches:
            distance = math.sqrt((tache.etapes[0].x - pince.x)**2 + (tache.etapes[0].y - pince.y)**2)
            if distance < distance_min:
                distance_min = distance
                tache_min = tache

        return tache_min