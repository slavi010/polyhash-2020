import os
import random
from threading import Thread

from src import resolv
from src.model.ExportOutput import ExportOutput
from src.model.Grille import Grille
from src.model.ItemCase import ItemCase

from src.model.ParseInput import ParseInput

# class th(Thread):
#     def __init__(self, best):
#         self.best = best
#         super ().__init__ ()
#
#     def run(self) -> None:


if __name__ == "__main__":
    file = "data/input/f_decentralized.txt"
    grille: Grille = ParseInput().parse(file)

    # print(grille)
    maxi = 0
    facteur = 0
    for tache in grille.taches:
        maxi += tache.points
        facteur += (tache.distance+1)/tache.points

    print("max=", maxi)
    print("moyenne=", maxi//len(grille.taches))
    print("max facteur=", facteur)
    print("moyenne facteur=", facteur/len(grille.taches))
    # Solution naïve
    best = [None, 0]
    for i in range(30):
        # d
        # FACTEUR_DISTANCE_RETRACTATION = 30
        # MAX_STUCK = random.randint(1, 30)
        # MAX_DIST_PM = 5
        # ADDITION = (random.random() * 0.8 + 0.2,
        #             random.randint(1, 15),
        #             random.randint(1, 15))
        # FACTEUR_CONCENTRATION_BRAS = 0.99
        # c
        # FACTEUR_DISTANCE_RETRACTATION = 30
        # MAX_STUCK = 10
        # MAX_DIST_PM = 300
        # FACTEUR_CONCENTRATION_BRAS = 1.25
        # f
        FACTEUR_DISTANCE_RETRACTATION = 30
        MAX_STUCK = 10
        MAX_DIST_PM = random.randint(110, 120)
        ADDITION = (0.304678,
                    13,
                    5)
        FACTEUR_CONCENTRATION_BRAS = 0.18
        grille_solution = resolv.methode_naive(grille, MAX_STUCK, FACTEUR_DISTANCE_RETRACTATION, MAX_DIST_PM, ADDITION, FACTEUR_CONCENTRATION_BRAS,
                                               affichage_graphique=False, affichage_console=False)
        print(i," points: ", grille_solution.points//1000, " K, ADDITION: ", ADDITION, ", MAX_STUCK: ", MAX_STUCK)
        if grille_solution.points > best[1]:
            best[1] = grille_solution.points
            best[0] = grille_solution
            print("best_points: ", best[1]//1000, " K")
            ExportOutput().exportOutput(best[0], os.path.basename(file) + "_" + str(best[1]) + ".out")

