import unittest
from kassapaate import Kassapaate
from maksukortti import Maksukortti


class TestKassapaate(unittest.TestCase):
    def setUp(self) -> None:
        self.kassa = Kassapaate()
        self.kortti = Maksukortti(1000)

    def test_init_works(self):
        self.assertEqual(self.kassa.kassassa_rahaa, 100_000)

    # KATEINEN
    def test_syo_maukkaasti_kateisella(self):
        self.kassa.syo_maukkaasti_kateisella(450)
        self.assertEqual(self.kassa.kassassa_rahaa, 100_400)

    def test_syo_maukkaasti_kateisella_tasaraha(self):
        self.kassa.syo_maukkaasti_kateisella(400)
        self.assertEqual(self.kassa.kassassa_rahaa, 100_400)

    def test_syo_maukkaasti_kateisella_maara_nousee(self):
        self.kassa.syo_maukkaasti_kateisella(400)
        self.assertEqual(self.kassa.maukkaat, 1)

    def test_syo_maukkaasti_liian_vahan_rahaa(self):
        self.kassa.syo_maukkaasti_kateisella(123)
        self.assertEqual(self.kassa.kassassa_rahaa, 100_000)

    def test_syo_maukkaasti_kateisella_maara_ei_nouse(self):
        self.kassa.syo_maukkaasti_kateisella(123)
        self.assertEqual(self.kassa.maukkaat, 0)

    def test_syo_maukkaasti_kateisella_rahat_takas(self):
        self.assertEqual(self.kassa.syo_maukkaasti_kateisella(123), 123)

    def test_syo_maukkaasti_kateisella_vaihto_raha(self):
        self.assertEqual(self.kassa.syo_maukkaasti_kateisella(450), 50)

    def test_syo_edullisesti_kateisella(self):
        self.kassa.syo_edullisesti_kateisella(450)
        self.assertEqual(self.kassa.kassassa_rahaa, 100_240)

    def test_syo_edullisesti_kateisella_tasaraha(self):
        self.kassa.syo_edullisesti_kateisella(240)
        self.assertEqual(self.kassa.kassassa_rahaa, 100_240)

    def test_syo_edullisesti_kateisella_maara_nousee(self):
        self.kassa.syo_edullisesti_kateisella(240)
        self.assertEqual(self.kassa.edulliset, 1)

    def test_syo_edullisesti_liian_vahan_rahaa(self):
        self.kassa.syo_edullisesti_kateisella(123)
        self.assertEqual(self.kassa.kassassa_rahaa, 100_000)

    def test_syo_edullisesti_kateisella_maara_ei_nouse(self):
        self.kassa.syo_edullisesti_kateisella(123)
        self.assertEqual(self.kassa.edulliset, 0)

    def test_syo_edullisesti_kateisella_rahat_takas(self):
        self.assertEqual(self.kassa.syo_edullisesti_kateisella(123), 123)

    def test_syo_edullisesti_kateisella_oikea_vaihto_raha(self):
        self.assertEqual(self.kassa.syo_edullisesti_kateisella(300), 60)
    # KATEINEN
    
    # KORTTI 
    def test_syo_maukkaasti_kortilla_tarpeeks(self):
        self.assertEqual(self.kassa.syo_maukkaasti_kortilla(self.kortti), True)

    def test_syo_maukkaasti_kortilla_tasaraha(self):
        kortti = Maksukortti(400)
        self.assertEqual(self.kassa.syo_maukkaasti_kortilla(kortti), True)
        
    def test_syo_maukkaasti_maara_kasvaa(self):
        self.kassa.syo_maukkaasti_kortilla(self.kortti)
        self.assertEqual(self.kassa.maukkaat, 1)
    
    def test_syo_maukkaasti_liian_vahan_rahaa_maara_ei_vaihdu(self):
        kortti = Maksukortti(5)
        self.kassa.syo_maukkaasti_kortilla(kortti)
        self.assertEqual(self.kassa.maukkaat, 0)
    def test_syo_maukkaasti_liian_vahan_rahaa_kortti_ei_vaihdu(self):
        kortti = Maksukortti(5)
        self.kassa.syo_maukkaasti_kortilla(kortti)
        self.assertEqual(kortti.saldo, 5)
    
    def test_syo_maukkaasti_liian_vahan_rahaa_palautusarvo(self):
        kortti = Maksukortti(5)
        self.assertEqual(self.kassa.syo_maukkaasti_kortilla(kortti), False)


    def test_syo_edullisesti_kortilla_tarpeeks(self):
        self.assertEqual(self.kassa.syo_edullisesti_kortilla(self.kortti), True)

    def test_syo_edullisesti_kortilla_tasaraha(self):
        kortti = Maksukortti(240)
        self.assertEqual(self.kassa.syo_edullisesti_kortilla(kortti), True)

    def test_syo_edullisesti_maara_kasvaa(self):
        self.kassa.syo_edullisesti_kortilla(self.kortti)
        self.assertEqual(self.kassa.edulliset, 1)

    def test_syo_edullisesti_liian_vahan_rahaa_maara_ei_vaihdu(self):
        kortti = Maksukortti(5)
        self.kassa.syo_edullisesti_kortilla(kortti)
        self.assertEqual(self.kassa.edulliset, 0)

    def test_syo_edullisesti_liian_vahan_rahaa_kortti_ei_vaihdu(self):
        kortti = Maksukortti(5)
        self.kassa.syo_edullisesti_kortilla(kortti)
        self.assertEqual(kortti.saldo, 5)

    def test_syo_edullisesti_liian_vahan_rahaa_palautusarvo(self):
        kortti = Maksukortti(5)
        self.assertEqual(self.kassa.syo_edullisesti_kortilla(kortti), False)

    def test_syo_edullisesti_kortilla_cash_maara_ei_vaihdu(self):
        self.kassa.syo_edullisesti_kortilla(self.kortti)
        self.assertEqual(self.kassa.kassassa_rahaa, 100_000)

    def test_syo_edullisesti_kortilla_cash_maara_ei_vaihdu(self):
        self.kassa.syo_edullisesti_kortilla(self.kortti)
        self.assertEqual(self.kassa.kassassa_rahaa, 100_000)

    def test_lataa_rahaa(self):
        self.kassa.lataa_rahaa_kortille(self.kortti, 100)
        self.assertEqual(self.kassa.kassassa_rahaa, 100_100)

    def test_lataa_neg_rahaa(self):
        self.kassa.lataa_rahaa_kortille(self.kortti, -1)
        self.assertEqual(self.kassa.kassassa_rahaa, 100_000)

    # KORTTI