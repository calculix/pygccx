from unittest import TestCase
from model_features import Plastic
from enums import EHardeningRules
from protocols import IModelFeature

class TestPlastic(TestCase):

    def test_is_IModelFeature(self):
        p = Plastic([210., 235.], [0., 0.002])
        self.assertTrue(isinstance(p, IModelFeature))

    def test_default(self):
        p = Plastic([210., 235.], [0., 0.002])
        known = '*PLASTIC\n'
        known += '  2.1000000e+02,  0.0000000e+00,  2.9400000e+02\n'
        known += '  2.3500000e+02,  2.0000000e-03,  2.9400000e+02\n'

        self.assertEqual(str(p), known)

    def test_hardening_options(self):
        p = Plastic([210., 235.], [0., 0.002], hardening=EHardeningRules.KINEMATIC)
        known = '*PLASTIC,HARDENING=KINEMATIC\n'
        known += '  2.1000000e+02,  0.0000000e+00,  2.9400000e+02\n'
        known += '  2.3500000e+02,  2.0000000e-03,  2.9400000e+02\n'
        self.assertEqual(str(p), known)

        p = Plastic([210., 235.], [0., 0.002], hardening=EHardeningRules.COMBINED)
        known = '*PLASTIC,HARDENING=COMBINED\n'
        known += '  2.1000000e+02,  0.0000000e+00,  2.9400000e+02\n'
        known += '  2.3500000e+02,  2.0000000e-03,  2.9400000e+02\n'
        self.assertEqual(str(p), known)

    def test_add_plastic_params_for_temp(self):
        p = Plastic([210., 235.], [0., 0.002])
        p.add_plastic_stress_strain_for_temp(310., [190., 230.],[0., 0.002])
        known = '*PLASTIC\n'
        known += '  2.1000000e+02,  0.0000000e+00,  2.9400000e+02\n'
        known += '  2.3500000e+02,  2.0000000e-03,  2.9400000e+02\n'
        known += '  1.9000000e+02,  0.0000000e+00,  3.1000000e+02\n'
        known += '  2.3000000e+02,  2.0000000e-03,  3.1000000e+02\n'
        self.assertEqual(str(p), known)

    def test_sress_strain_different_length(self):
        self.assertRaises(ValueError,Plastic, [210.], [0., 0.002])
