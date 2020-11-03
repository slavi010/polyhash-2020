from enum import Enum


class TypeMap(Enum):
    """Le mouvement d'un robot"""
    A = "A"
    B = "B"
    C = "C"
    D = "D"
    E = "E"
    F = "F"

    def __str__(self):
        return self.value
