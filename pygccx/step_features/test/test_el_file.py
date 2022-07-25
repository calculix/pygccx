from unittest import TestCase
from step_features import ElFile, TimePoints
from enums import EElementResults, EResultOutputs

class TestElFile(TestCase):

    def test_default(self):

        ef = ElFile([EElementResults.S, EElementResults.E])
        known = '*EL FILE\n'
        known +='S,E\n'
        self.assertEqual(str(ef), known)

    def test_frequency(self):

        ef = ElFile([EElementResults.S], frequency=2)
        known = '*EL FILE,FREQUENCY=2\n'
        known +='S\n'
        self.assertEqual(str(ef), known)

    def test_time_points(self):
        tp = TimePoints('TP1', (1,2,3,4))
        ef = ElFile([EElementResults.S], time_points=tp)
        known = '*EL FILE,TIME POINTS=TP1\n'
        known +='S\n'
        self.assertEqual(str(ef), known)

    def test_last_iteration(self):

        ef = ElFile([EElementResults.S], last_Iterations=True)
        known = '*EL FILE,LAST ITERATIONS\n'
        known +='S\n'
        self.assertEqual(str(ef), known)

    def test_contact_elements(self):

        ef = ElFile([EElementResults.S], contact_elements=True)
        known = '*EL FILE,CONTACT ELEMENTS\n'
        known +='S\n'
        self.assertEqual(str(ef), known)

    def test_global_no(self):

        ef = ElFile([EElementResults.S], global_=False)
        known = '*EL FILE,GLOBAL=NO\n'
        known +='S\n'
        self.assertEqual(str(ef), known)

    def test_output_all(self):

        ef = ElFile([EElementResults.S], output_all=True)
        known = '*EL FILE,OUTPUT ALL\n'
        known +='S\n'
        self.assertEqual(str(ef), known)

    def test_output_2D(self):

        ef = ElFile([EElementResults.S], output=EResultOutputs._2D)
        known = '*EL FILE,OUTPUT=2D\n'
        known +='S\n'
        self.assertEqual(str(ef), known)

    def test_empty_entities(self):
        self.assertRaises(ValueError, ElFile, [])

    def test_time_points_and_frequency(self):
        tp = TimePoints('TP1', (1,2,3,4))
        self.assertRaises(ValueError, ElFile, [EElementResults.S], time_points=tp, frequency=2)
