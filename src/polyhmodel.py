#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
    Module de définition des structures de données de Poly#.
"""

__all__ = ['useless'] # ajouter dans cette liste tous les symboles 'importables'


class useless:
    """
        Une classe vraiment inutile.
    """
    def __str__(self):
        return "Poly# vide"


if __name__ == "__main__":
    inutile = useless()
    print('J\'ai créé un {}.'.format(inutile))