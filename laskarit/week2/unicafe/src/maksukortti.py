class Maksukortti:
    def __init__(self, saldo):
        self.saldo = saldo

    def lataa_rahaa(self, lisays):
        self.saldo += lisays

    def ota_rahaa(self, maara):
        if self.saldo < maara:
            return False

        self.saldo = self.saldo - maara
        return True

    def __str__(self):
        saldo_euroissa = round(self.saldo / 100, 2)

        return f"saldo: {saldo_euroissa}"
