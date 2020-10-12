#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
    Module de résolution du problème de placement de bornes wifi
    posé par le projet Poly#.
    Usage:

    >>> from polyhash import solve
    >>> solve()
"""


__all__ = ['solve']  # ajouter dans cette liste tous les symboles 'importables'


from .polyhutils import say_hello

def solve():
    """
        Fonction de résolution. Aucun paramètre, et
        retourne None, car ce n'est qu'un modèle.
    """
    say_hello("Poly#")


if __name__ == "__main__":
    solve()
