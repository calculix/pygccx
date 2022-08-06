'''
Copyright Matthias Sedlmaier 2022
This file is part of pygccx.

pygccx is free software: you can redistribute it 
and/or modify it under the terms of the GNU General Public License as 
published by the Free Software Foundation, either version 3 of the 
License, or (at your option) any later version.

pygccx is distributed in the hope that it will 
be useful, but WITHOUT ANY WARRANTY; without even the implied warranty 
of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with pygccx.  
If not, see <http://www.gnu.org/licenses/>.
'''

from unittest import TestCase
from dataclasses import dataclass
from model_keywords import Orientation
from enums import EOrientationRotAxis, EOrientationSystems
from protocols import IModelFeature
import numpy as np

@dataclass
class CoordinateSystemMock:
    name:str
    type:EOrientationSystems

    def get_origin(self):
        return np.array([1,2,3])

    def get_matrix(self):
        return np.array([[0, 0, 1],
                        [0, -1, 0],
                        [1, 0, 0]])

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

    def test_from_coordinate_system_rectangular(self):
        cs = CoordinateSystemMock('C1', EOrientationSystems.RECTANGULAR)
        o = Orientation.from_coordinate_system(cs)
        known = '*ORIENTATION,NAME=OR_C1,SYSTEM=RECTANGULAR\n'
        known += '0,0,1,0,-1,0\n'
        self.assertEqual(str(o), known)
    
    def test_from_coordinate_system_cylindrical(self):
        cs = CoordinateSystemMock('C1', EOrientationSystems.CYLINDRICAL)
        o = Orientation.from_coordinate_system(cs)
        known = '*ORIENTATION,NAME=OR_C1,SYSTEM=CYLINDRICAL\n'
        known += '1,2,3,2,2,3\n'
        self.assertEqual(str(o), known)