import os
from typing import List

from src.model.Etape import Etape
from src.model.Grille import Grille
from src.model.PointMontage import PointMontage
from src.model.Robot import Robot
from src.model.Tache import Tache


class ParseInput:
    """Parser qui permet de lire le fichier texte d'input fourni par google."""

    grille: Grille

    def __init__(self):
        pass

    def parse(self, file_path: str) -> Grille:
        """parse le fichier google et retourne la Grille correspondante

        :rtype: Grille
        """

        # file_path = '/polyhash-2020/data/input/' + input('Entrer le nom du fichier à tester')
        # test si file_path est un fichier
        assert os.path.isfile(file_path)

        with open(file_path, 'r') as file:
            index: int = 0

            # récupère toutes les lignes du fichiers
            lines: List = file.readlines()

            # Transformation des lignes en liste d'entiers
            for index_line in range(len(lines)):
                lines[index_line] = lines[index_line].split(' ')
                for index_val in range(len(lines[index_line])):
                    lines[index_line][index_val] = int(lines[index_line][index_val])

        # crée un instance de Grille
        self.grille = Grille(lines[0][0], lines[0][1])

        # instancie dans grille le nombre de robot correspondant
        # crée les robots
        for idx_robot in range(lines[0][2]):
            self.grille.robots.append(Robot())

        # Crée les points de montage, et les place dans la grille
        for idx_point_montage in range(lines[0][3]):
            index += 1
            self.grille.add_point_montage(PointMontage(lines[index][0], lines[index][1], self.grille))

        # Récupère le nombre de tour d'horloge autorisé
        self.grille.step_simulation = lines[0][5]

        # Récupére les informations de chaque tâche
        # instancier dans grille les tâches correspondantes
        # si une étape (assembly point) n'est pas encore créer dans la grille au cordonnées correspondantes,
        # l'instancier et la mettre dans la grille (et ne pas oublier de l'associer à la tâche)

        # Crée les instances Taches et Etapes
        for index_tache in range(lines[0][4]):
            index += 1
            tache_tampon: Tache = Tache(lines[index][0])
            index += 1
            for index_etape in range(lines[index-1][1]):
                tache_tampon.add_etape(Etape(lines[index][index_etape*2+0], lines[index][index_etape*2+1], self.grille))
            self.grille.add_tache(tache_tampon)

        return self.grille
