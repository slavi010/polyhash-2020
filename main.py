import os

from src import resolv
from src.model.ExportOutput import ExportOutput
from src.model.Grille import Grille
from src.model.ItemCase import ItemCase

from src.model.ParseInput import ParseInput

if __name__ == "__main__":
    grille: Grille = ParseInput().parse("data/input/f_decentralized.txt")
    print(grille)
    # Solution naïve
    grille_solution = resolv.methode_naive(grille)
    ExportOutput().exportOutput(grille_solution)

