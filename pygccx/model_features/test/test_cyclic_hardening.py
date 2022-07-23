from unittest import TestCase
from model_features import CyclicHardening
from protocols import IModelFeature

class TestCyclicHardening(TestCase):

    def test_is_IModelFeature(self):
        c = CyclicHardening([210., 235.], [0., 0.002])
        self.assertTrue(isinstance(c, IModelFeature))

    def test_default(self):
        c = CyclicHardening([210., 235.], [0., 0.002])
        known = '*CYCLIC HARDENING\n'
        known += '  2.1000000e+02,  0.0000000e+00,  2.9400000e+02\n'
        known += '  2.3500000e+02,  2.0000000e-03,  2.9400000e+02\n'

        self.assertEqual(str(c), known)

    def test_add_plastic_params_for_temp(self):
        c = CyclicHardening([210., 235.], [0., 0.002])
        c.add_plastic_stress_strain_for_temp(310., [190., 230.],[0., 0.002])
        known = '*CYCLIC HARDENING\n'
        known += '  2.1000000e+02,  0.0000000e+00,  2.9400000e+02\n'
        known += '  2.3500000e+02,  2.0000000e-03,  2.9400000e+02\n'
        known += '  1.9000000e+02,  0.0000000e+00,  3.1000000e+02\n'
        known += '  2.3000000e+02,  2.0000000e-03,  3.1000000e+02\n'
        self.assertEqual(str(c), known)

    def test_sress_strain_different_length(self):
        self.assertRaises(ValueError, CyclicHardening, [210.], [0., 0.002])
