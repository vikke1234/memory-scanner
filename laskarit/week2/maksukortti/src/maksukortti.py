EDULLINEN = 2.5
MAUKAS = 4


class Maksukortti:
    def __init__(self, arvo_alussa):
        self.arvo = arvo_alussa

    def syo_edullisesti(self):
        if self.arvo >= EDULLINEN:
            self.arvo -= EDULLINEN

    def syo_maukkaasti(self):
        if self.arvo >= MAUKAS:
            self.arvo -= MAUKAS

    def lataa_rahaa(self, rahamaara):
        if rahamaara < 0:
            return

        self.arvo += rahamaara

        if self.arvo > 150:
            self.arvo = 150

    def __str__(self):
        return f"Kortilla on rahaa {self.arvo} euroa"
