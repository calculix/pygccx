from unittest import TestCase
from model_features import Friction
from protocols import IModelFeature

class TestFriction(TestCase):

    def test_is_IModelFeature(self):
        f = Friction(0.3, 50000.)
        self.assertTrue(isinstance(f, IModelFeature))

    def test_happy_case(self):
        f = Friction(0.3, 50000.)
        known = '*FRICTION\n'
        known += '0.3,50000.0\n'
        self.assertEqual(str(f), known)

    def test_mue_lower_zero(self):
        self.assertRaises(ValueError, Friction, 0, 50000)
        self.assertRaises(ValueError, Friction, -1, 50000)

    def test_lam_lower_zero(self):
        self.assertRaises(ValueError, Friction, 0.3, 0)
        self.assertRaises(ValueError, Friction, 0.3, -1)
