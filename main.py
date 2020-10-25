import os

from src import resolv
from src.model.Grille import Grille
from src.model.ItemCase import ItemCase

from src.model.ParseInput import ParseInput

if __name__ == "__main__":
    grille: Grille = ParseInput().parse("data/input/f_decentralized.txt")
    if grille.longueur <= 100:
        print(grille)
    # Solution naïve
    resolv.methode_naive(grille)
