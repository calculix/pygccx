from unittest import TestCase
from model_features import Elastic
from enums import EELasticTypes
from protocols import IModelFeature

class TestElastic(TestCase):

    def test_is_IModelFeature(self):
        e = Elastic((210000., 0.3))
        self.assertTrue(isinstance(e, IModelFeature))

    def test_iso(self):
        e = Elastic((210000., 0.3))
        known = '*ELASTIC,TYPE=ISO\n210000.0,0.3,294.0\n'
        self.assertEqual(str(e), known)

    def test_ortho(self):
        e = Elastic((500000.,157200.,400000.,157200.,
                     157200.,300000.,126200.,126200.,
                     126200.), EELasticTypes.ORTHO)
        known = '*ELASTIC,TYPE=ORTHO\n'
        known += '500000.0,157200.0,400000.0,157200.0,157200.0,300000.0,126200.0,126200.0,\n'
        known += '126200.0,294.0\n'
        self.assertEqual(str(e), known)

    def test_aniso(self):
        e = Elastic((1,2,3,4,5,6,7,8,9,10,
                     11,12,13,14,15,16,17,18,19,20,21),
                     EELasticTypes.ANISO, )
        known = '*ELASTIC,TYPE=ANISO\n'
        known += '1,2,3,4,5,6,7,8,\n'
        known += '9,10,11,12,13,14,15,16,\n'
        known += '17,18,19,20,21,294.0\n'
        self.assertEqual(str(e), known)

    def test_ortho_two_temps(self):
        e = Elastic((500000.,157200.,400000.,157200.,
                     157200.,300000.,126200.,126200.,
                     126200.), EELasticTypes.ORTHO)
        e.add_elastic_params_for_temp(300.,
            500000.,157200.,400000.,157200.,
            157200.,300000.,126200.,126200.,
            126200.
        )
        known = '*ELASTIC,TYPE=ORTHO\n'
        known += '500000.0,157200.0,400000.0,157200.0,157200.0,300000.0,126200.0,126200.0,\n'
        known += '126200.0,294.0\n'
        known += '500000.0,157200.0,400000.0,157200.0,157200.0,300000.0,126200.0,126200.0,\n'
        known += '126200.0,300.0\n'
        self.assertEqual(str(e), known)

    def test_params_false_length(self):
        self.assertRaises(ValueError, Elastic, (500000.,157200.,400000.,157200.,
                                                157200.,300000.,126200.,126200.), EELasticTypes.ORTHO)
        # one param less than required

