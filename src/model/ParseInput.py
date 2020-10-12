import os

from src.model.Grille import Grille


class ParseInput:
    """Parser qui permet de lire le fichier texte d'input fourni par google."""

    grille: Grille

    def __init__(self):
        pass


    def parse(self, file_path: str) -> Grille:
        """parse le fichier google et retourne la Grille correspondante"""

        # test si file_path est un fichier
        assert os.path.isfile(file_path)

        # TODO : récupérer toutes les lignes du fichiers

        # TODO : récupérer longueur et hauteur grille

        # TODO : créer un instance de Grille
        # self.grille = Grille(...)

        # TODO : récupérer le nombre de robot, de point de montage, de taches et d'étapes
        # instancier dans grille le nombre de robot correspondant

        # TODO : récupérer les coordonnées de chaque point de montage
        # instancier dans grille les points de montage correspondant

        # TODO : récupérer les informations de chaque tâche
        # instancier dans grille les tâches correspondantes
        # si une étape (assembly point) n'est pas encore créer dans la grille au cordonnées correspondantes,
        # l'instancier et la mettre dans la grille (et ne pas oublier de l'associer à la tâche)

        return self.grille

