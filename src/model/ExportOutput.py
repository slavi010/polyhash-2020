from typing import List

from src.model.Grille import Grille
from src.model.Mouvement import Mouvement
from src.model.Tache import Tache


class ExportOutput:

    def __init__(self):
        pass

    def exportOutput(self, grille: Grille, name: str):
        """lecture du fichier de sortie
        -> nombre de robots utilisés
        -> Premier Robot : Coordonées de montages + nombre de taches faites + nombre d'étapes
        Taches effectuées
        Déplacements  -> U=up / R= right / L= Left / D=Down / W= Waits
        Pas d'espace
        second robot
        ...
        """

        #Création + écriture fichier output
        output = open(name,"w")

        # calcule nb robot actif
        actif = 0
        for robot in grille.robots:
            if len(robot.taches):
                actif += 1

        output.write(str(actif) + "\n") #ecrire nombre de robots utilisés

        for robot in grille.robots:
            if len(robot.taches):
                pointMontage=robot.point_montage #le point de montage

                taches: List = robot.taches #liste des taches
                mouv: List = robot.mouvements # liste des mouvements

                nbtaches = len(taches) #nombre de taches
                nbEtapes = len(mouv) #nombre de mouvement

                output.write(str(pointMontage.x) + " " + str(pointMontage.y) + " " + str(nbtaches) + " " + str(nbEtapes) + "\n")

                #citer les taches et mettre dans doc
                for t in taches:
                    output.write(str(t.numero) + " ")
                output.write("\n")
                # citer les mouvements et mettre dans doc
                for m in mouv:
                    output.write(m.value + " ")
                output.write("\n")

        #fermeture fichier output
        output.close()



