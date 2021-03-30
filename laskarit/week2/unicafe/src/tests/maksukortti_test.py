import unittest
from maksukortti import Maksukortti

class TestMaksukortti(unittest.TestCase):
    def setUp(self):
        self.maksukortti = Maksukortti(10)

    def test_luotu_kortti_on_olemassa(self):
        self.assertNotEqual(self.maksukortti, None)

    def test_oikee_maara(self):
        self.assertEqual(str(self.maksukortti), "saldo: 0.1")

    def test_ota_rahaa(self):
        self.maksukortti.ota_rahaa(5)
        self.assertEqual(str(self.maksukortti), "saldo: 0.05")

    def test_ota_liikaa_rahaa(self):
        self.maksukortti.ota_rahaa(1000)
        self.assertEqual(str(self.maksukortti), "saldo: 0.1")


    def test_ota_liikaa_palautus_arvo(self):
        self.assertEqual(self.maksukortti.ota_rahaa(1000), False)

    def test_ota_sopivasti_palautus_arvo(self):
        self.assertEqual(self.maksukortti.ota_rahaa(1), True)

