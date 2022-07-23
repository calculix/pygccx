from unittest import TestCase
from model_features import Orientation
from enums import EOrientationRotAxis, EOrientationSystems
from protocols import IModelFeature

class TestOrientation(TestCase):

    def test_is_IModelFeature(self):
        o = Orientation('O1', (0,0,1), (1,0,0))
        self.assertTrue(isinstance(o, IModelFeature))

    def test_rectangular(self): 
        o = Orientation('O1', (0,0,1), (1,0,0))
        known = '*ORIENTATION,NAME=O1,SYSTEM=RECTANGULAR\n'
        known += '0,0,1,1,0,0\n'
        self.assertEqual(str(o), known)

    def test_cylindrical(self):
        o = Orientation('O1', (0,0,1), (1,0,0), EOrientationSystems.CYLINDRICAL)
        known = '*ORIENTATION,NAME=O1,SYSTEM=CYLINDRICAL\n'
        known += '0,0,1,1,0,0\n'
        self.assertEqual(str(o), known)

    def test_rectangular_w_rot(self): 
        o = Orientation('O1', (0,0,1), (1,0,0), rot_axis=EOrientationRotAxis.Y, rot_angle=1.67)
        known = '*ORIENTATION,NAME=O1,SYSTEM=RECTANGULAR\n'
        known += '0,0,1,1,0,0\n'
        known += '2,1.67\n'
        self.assertEqual(str(o), known)

    def test_cylindrical_w_rot(self):
        o = Orientation('O1', (0,0,1), (1,0,0), EOrientationSystems.CYLINDRICAL,
                        rot_axis=EOrientationRotAxis.Y, rot_angle=1.67)
        # rotation has no influence
        known = '*ORIENTATION,NAME=O1,SYSTEM=CYLINDRICAL\n'
        known += '0,0,1,1,0,0\n'
        self.assertEqual(str(o), known)

    def test_pnt_a_false_length(self):
        self.assertRaises(ValueError, Orientation, 'O1', (0,1), (1,0,0))

    def test_pnt_b_false_length(self):
        self.assertRaises(ValueError, Orientation, 'O1', (0,0,1), (1,0))