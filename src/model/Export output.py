from src.model.Grille import Grille



class ExportOutput:

    def __init__(self):
        pass

    def exportOutput(self):

        #Création + écriture fichier output
        output = open("output.txt","a")


        """
        lecture du fichier de sortie:
        ->nombre de robots utilisés 
       -> Premier Robot : Coordonées de montages + nombre de taches faites + nombre d'étapes
        Taches effectuées
        Déplacements  -> U=up / R= right / L= Left / D=Down / W= Waits
        Pas d'espace
        second robot
        ...
        """

        nbRobots:int = len(Grille.robots) #nombre de robots


        output.write(nbRobots + "\n") #ecrire nombre de robots utilisés

        for robot in Grille.robots:
            pointMontage=robot.point_montage #le point de montage

            taches = robot.taches #liste des taches
            mouv=robot.mouvements # liste des mouvements

            nbtaches=len(taches) #nombre de taches
            nbEtapes=len(mouv) #nombre de mouvement

            output.write(pointMontage[0] + " " + pointMontage[1] + " " + nbtaches + " " + nbEtapes + "\n")

            #citer les taches et mettre dans doc
            for t in taches:
                output.write(t + " ")
            output.write("\n")
            # citer les mouvements et mettre dans doc
            for m in mouv:
                output.write(m + " ")
            output.write("\n")




        #fermeture fichier output
        self.output.close()



