from typing import List


class Tache:
    """Une tâche à acomplire"""

    points: int

    # les etapes a effectuer triée dans l'ordre
    etapes: List

    def __init__(self, points: int):
        self.points = points
        self.etapes = []
        