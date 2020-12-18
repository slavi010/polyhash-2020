import os
from typing import List

from src.model.Etape import Etape
from src.model.Grille import Grille
from src.model.ItemCase import ItemCase
from src.model.PointMontage import PointMontage
from src.model.Robot import Robot
from src.model.Tache import Tache


class ParseInput:
    """Parser qui permet de lire le fichier texte d'input fourni par Google.
    Va transformer ce fichier en données et classes exploitables pour nous
     """

    grille: Grille

    def __init__(self):
        pass

    def parse(self, file_path: str) -> Grille:
        """parse le fichier google et retourne la Grille correspondante

        :rtype: Grille
        """

        # tests si file_path est un fichier
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
            grille = Grille(lines[0][0], lines[0][1])

            # instancie dans grille le nombre de robot correspondant
            # crée les robots
            for idx_robot in range(lines[0][2]):
                grille.robots.append(Robot())

            # Crée les points de montage, et les place dans la grille
            for idx_point_montage in range(lines[0][3]):
                index += 1
                grille.add_point_montage(PointMontage(lines[index][0], lines[index][1]))

            # Récupère le nombre de tour d'horloge autorisé
            grille.step_simulation = lines[0][5]

            # Récupére les informations de chaque tâche
            # instancier dans grille les tâches correspondantes
            # si une étape (assembly point) n'est pas encore créée dans la grille aux cordonnées correspondantes,
            # l'instancier et la mettre dans la grille (et ne pas oublier de l'associer à la tâche)

            # Crée les instances Taches et Etapes
            for index_tache in range(lines[0][4]):
                index += 1
                tache_tampon: Tache = Tache(lines[index][0], index_tache)
                index += 1

                g_x = 0
                g_y = 0
                for index_etape in range(lines[index-1][1]):
                    #ajoute les étapes
                    etape = Etape(lines[index][index_etape*2+0], lines[index][index_etape*2+1])
                    tache_tampon.add_etape(etape)
                    g_x += (etape.x - g_x)/len(tache_tampon.etapes)
                    g_y += (etape.y - g_y)/len(tache_tampon.etapes)
                #ajoute les paramètres dans la classe tache
                tache_tampon.centre_gravite = ItemCase(int(g_x), int(g_y))
                tache_tampon.distance_centre_gravite = max(tache_tampon.etapes,
                                                           key=lambda etape: tache_tampon.centre_gravite.distance(etape)) \
                    .distance(tache_tampon.centre_gravite)
                grille.add_tache(tache_tampon)

                # calcul la distance et la surface aproximative entre chaque étape
                for etape_from, etape_to in zip(tache_tampon.etapes[0::1], tache_tampon.etapes[1::1]):
                    tache_tampon.distance += etape_from.distance(etape_to)
                    tache_tampon.surface += etape_from.distance(etape_to)

            return grille