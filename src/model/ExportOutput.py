from typing import List

from typing import List, Union


from src.model.Grille import Grille
from src.model.Mouvement import Mouvement

from src.model.ParseInput import ParseInput
from src.model.TypeMap import TypeMap


class ExportOutput:

    def __init__(self):
        pass

    def traitementAPropre(self):


        pass
        
        
        
    # def traitementA(self):
    #
    #     #Façon simple
    #     output = open(name, "w")
    #
    #
    #     output.write("2\n")  # ecrire nombre de robots utilisés
    #
    #
    #     output.write("1 3 2 3\n")
    #     output.write("0 2")
    #     output.write("\n")
    #     output.write("R R W")
    #     output.write("\n")
    #
    #     output.write("3 2 1 3\n")
    #     output.write("1")
    #     output.write("\n")
    #     output.write("R D D")
    #     output.write("\n")
    #
    #     # fermeture fichier output
    #     output.close()





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

    def exportA(self):
        grille = ParseInput().parse(TypeMap.A.get_path())
        robot1 = grille.robots[0]
        pm1 = None
        pm2 = None
        for point_montage in grille.point_montages:
            if point_montage.x == 1 and point_montage.y == 3:
                pm1 = point_montage

            elif point_montage.x == 3 and point_montage.y == 2:
                pm2 = point_montage

        tache1 = -1
        tache2 = -1
        tache3 = -1
        for tache in grille.taches:
            if tache.numero == 0:
                tache1 = tache

            elif tache.numero == 1:
                tache2 = tache
            elif tache.numero == 2:
                tache3 = tache

        #if pm1 is not None and pm2 is not None and -1 != tache1 and -1 != tache2 and -1 != tache3:
        robot1.point_montage = pm1
        robot1.add_tache(tache1, grille)
        robot1.add_tache(tache3, grille)
        robot1.mouvements.append(Mouvement.DROITE)
        robot1.mouvements.append(Mouvement.DROITE)
        robot1.mouvements.append(Mouvement.ATTENDRE)

        robot2 = grille.robots[1]
        robot2.point_montage = pm2
        robot2.add_tache(tache2, grille)
        robot2.mouvements.append(Mouvement.DROITE)
        robot2.mouvements.append(Mouvement.BAS)
        robot2.mouvements.append(Mouvement.BAS)

        ExportOutput().exportOutput(grille, "a.out")


        #else:
         #   print("Problème sur les points de montages ou les tâches")