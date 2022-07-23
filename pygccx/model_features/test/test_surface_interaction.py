from unittest import TestCase
from model_features import SurfaceInteraction
from protocols import IModelFeature

class TestSurfaceInteraction(TestCase):

    def test_is_IModelFeature(self):
        si = SurfaceInteraction('SI1')
        self.assertTrue(isinstance(si, IModelFeature))

    def test_happy_case(self):
        si = SurfaceInteraction('SI1')
        known = '*SURFACE INTERACTION,NAME=SI1\n'
        self.assertEqual(str(si), known)

    def test_name_too_long(self):
        name = 'a' * 81
        self.assertRaises(ValueError, SurfaceInteraction, name)
