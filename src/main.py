#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
    Module d'entrée pour la mise en oeuvre du projet Poly#.
"""

# from polyhash import solve
from src.model.ParseInput import ParseInput

if __name__ == "__main__":
    grille = ParseInput().parse("data/input/a_example.txt")
