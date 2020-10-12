from typing import List

from src.model.PointMontage import PointMontage


class Robot:
    """Un robot"""

    point_montage: [PointMontage, None]
    bras: List
    taches: List
    mouvements: List

    def __init__(self):
        self.point_montage = None
        self.bras = []
        self.taches = []
        self.mouvements = []
