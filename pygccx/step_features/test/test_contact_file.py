from unittest import TestCase
from step_features import ContactFile, TimePoints
from enums import EContactResults

class TestContactFile(TestCase):

    def test_default(self):

        cf = ContactFile([EContactResults.CDIS, EContactResults.CELS])
        known = '*CONTACT FILE\n'
        known +='CDIS,CELS\n'
        self.assertEqual(str(cf), known)

    def test_frequency(self):

        cf = ContactFile([EContactResults.CDIS, EContactResults.CELS], frequency=2)
        known = '*CONTACT FILE,FREQUENCY=2\n'
        known +='CDIS,CELS\n'
        self.assertEqual(str(cf), known)

    def test_time_points(self):
        tp = TimePoints('TP1', (1,2,3,4))
        cf = ContactFile([EContactResults.CDIS, EContactResults.CELS], time_points=tp)
        known = '*CONTACT FILE,TIME POINTS=TP1\n'
        known +='CDIS,CELS\n'
        self.assertEqual(str(cf), known)

    def test_contact_elements(self):

        cf = ContactFile([EContactResults.CDIS, EContactResults.CELS], contact_elements=True)
        known = '*CONTACT FILE,CONTACT ELEMENTS\n'
        known +='CDIS,CELS\n'
        self.assertEqual(str(cf), known)

    def test_empty_entities(self):
        self.assertRaises(ValueError, ContactFile, [])

    def test_time_points_and_frequency(self):
        tp = TimePoints('TP1', (1,2,3,4))
        self.assertRaises(ValueError, ContactFile, [EContactResults.CDIS], time_points=tp, frequency=2)
