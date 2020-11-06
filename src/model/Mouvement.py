from enum import Enum


class Mouvement(Enum):
    """Le mouvement d'un robot"""
    HAUT = "U"
    DROITE = "R"
    BAS = "D"
    GAUCHE = "L"
    ATTENDRE = "W"

    def __str__(self):
        return self.value

    def rotation_90(self, multiplicateur: int = 1):
        """Retourne le mouvement après rotation a 90° dans le sens horaire

        Exemple :
            Si mouvement = HAUT et multiplicateur = 1 alors retourne DROITE

        :param multiplicateur: Multiplication par 90°
        :return: Mouvement après rotation
        """
        assert multiplicateur >= 0

        mouvement = self

        for i in range(multiplicateur):
            if mouvement == Mouvement.HAUT:
                mouvement = Mouvement.DROITE
            elif mouvement == Mouvement.DROITE:
                mouvement = Mouvement.BAS
            elif mouvement == Mouvement.BAS:
                mouvement = Mouvement.GAUCHE
            else:
                mouvement = Mouvement.HAUT

        return mouvement
