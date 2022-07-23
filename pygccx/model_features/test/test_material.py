from unittest import TestCase
from model_features import Material
from protocols import IModelFeature

class TestMaterial(TestCase):

    def test_is_IModelFeature(self):
        m = Material('Steel')
        self.assertTrue(isinstance(m, IModelFeature))

    def test_happy_case(self):
        m = Material('Steel')

        known = '*MATERIAL,NAME=Steel\n'
        self.assertEqual(str(m), known)

    def test_name_too_long(self):
        name = 'a' * 81
        self.assertRaises(ValueError, Material, name)