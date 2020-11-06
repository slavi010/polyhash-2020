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
from src.model.TypeMap import TypeMap

if __name__ == "__main__":
    map = TypeMap.D
    iteration = 50
    affichage_graphique = False
    affichage_console = False


    FACTEUR_DISTANCE_RETRACTATION = int
    MAX_STUCK = int
    MAX_DIST_PM = int
    ADDITION: tuple
    FACTEUR_CONCENTRATION_BRAS: float


    # print(grille)
    # maxi = 0
    # facteur = 0
    # for tache in grille.taches:
    #     maxi += tache.points
    #     facteur += (tache.distance+1)/tache.points
    #
    # print("max=", maxi)
    # print("moyenne=", maxi//len(grille.taches))
    # print("max facteur=", facteur)
    # print("moyenne facteur=", facteur/len(grille.taches))

    grille: Grille = ParseInput().parse(map.get_path())

    best = [None, 0]
    for i in range(iteration):
        if map == TypeMap.A:
            pass
        elif map == TypeMap.B:
            pass
        elif map == TypeMap.C:
            FACTEUR_DISTANCE_RETRACTATION = 30
            MAX_STUCK = 10
            MAX_DIST_PM = random.randint(150, 400)
            ADDITION = (random.random() * 0.01 + 0.0001,
                        random.randint(6, 15),
                        random.randint(6, 15),
                        random.randint(1, 30))
            FACTEUR_CONCENTRATION_BRAS = 1.25
        elif map == TypeMap.D:
            FACTEUR_DISTANCE_RETRACTATION = 30
            MAX_STUCK = 34
            MAX_DIST_PM = 5
            ADDITION = (0.007439079675817982, 6, 15, 2)
            # ADDITION = (random.random() * 0.01 + 0.0001,
            #             random.randint(6, 15),
            #             random.randint(6, 15),
            #             random.randint(1, 30))
            FACTEUR_CONCENTRATION_BRAS = 0.99
        elif map == TypeMap.E:
            pass
        elif map == TypeMap.F:
            FACTEUR_DISTANCE_RETRACTATION = 30
            MAX_STUCK = 10
            MAX_DIST_PM = random.randint(110, 120)
            ADDITION = (0.304678,
                        13,
                        5)
            FACTEUR_CONCENTRATION_BRAS = 0.18

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
        # FACTEUR_DISTANCE_RETRACTATION = 30
        # MAX_STUCK = 10
        # MAX_DIST_PM = random.randint(110, 120)
        # ADDITION = (0.304678,
        #             13,
        #             5)
        # FACTEUR_CONCENTRATION_BRAS = 0.18
        grille_solution = resolv.methode_naive(grille, map, MAX_STUCK, FACTEUR_DISTANCE_RETRACTATION, MAX_DIST_PM, ADDITION, FACTEUR_CONCENTRATION_BRAS,
                                               affichage_graphique=affichage_graphique, affichage_console=affichage_console)
        print(i," points: ", grille_solution.points//1000, " K, ADDITION: ", ADDITION, ", MAX_STUCK: ", MAX_STUCK)
        if grille_solution.points > best[1]:
            best[1] = grille_solution.points
            best[0] = grille_solution
            print("best_points: ", best[1]//1000, " K")
            ExportOutput().exportOutput(best[0], os.path.basename(map.get_path()) + "_" + str(best[1]) + ".out")

