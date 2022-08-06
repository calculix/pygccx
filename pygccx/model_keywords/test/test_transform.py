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
from model_keywords import Transform
from enums import EOrientationSystems, ESetTypes
from protocols import IModelFeature
import numpy as np

@dataclass()
class SetMock():
    name:str
    type:ESetTypes
    dim:int
    ids:set[int]

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

class TestTransform(TestCase):

    def setUp(self) -> None:
        self.nset = SetMock('S1', ESetTypes.NODE, 2, set([1,2,3,4]))

    def test_is_IModelFeature(self):
        t = Transform(self.nset, (0,0,1), (1,0,0))
        self.assertTrue(isinstance(t, IModelFeature))

    def test_rectangular(self): 
        t = Transform(self.nset, (0,0,1), (1,0,0))
        known = '*TRANSFORM,NSET=S1,TYPE=R\n'
        known += '0,0,1,1,0,0\n'
        self.assertEqual(str(t), known)

    def test_cylindrical(self):
        o = Transform(self.nset, (0,0,1), (1,0,0), EOrientationSystems.CYLINDRICAL)
        known = '*TRANSFORM,NSET=S1,TYPE=C\n'
        known += '0,0,1,1,0,0\n'
        self.assertEqual(str(o), known)

    def test_pnt_a_false_length(self):
        self.assertRaises(ValueError, Transform, self.nset, (0,1), (1,0,0))

    def test_pnt_b_false_length(self):
        self.assertRaises(ValueError, Transform, self.nset, (0,0,1), (1,0))

    def test_wrong_set_type(self):
        eset = SetMock('S2', ESetTypes.ELEMENT, 3, set([1,2,3,4]))
        self.assertRaises(ValueError, Transform, eset, (0,0,1), (1,0))

    def test_from_coordinate_system_rectangular(self):
        cs = CoordinateSystemMock('C1', EOrientationSystems.RECTANGULAR)
        t = Transform.from_coordinate_system(self.nset, cs)
        known = '*TRANSFORM,NSET=S1,TYPE=R\n'
        known += '0,0,1,0,-1,0\n'
        self.assertEqual(str(t), known)
    
    def test_from_coordinate_system_cylindrical(self):
        cs = CoordinateSystemMock('C1', EOrientationSystems.CYLINDRICAL)
        t = Transform.from_coordinate_system(self.nset, cs)
        known = '*TRANSFORM,NSET=S1,TYPE=C\n'
        known += '1,2,3,2,2,3\n'
        self.assertEqual(str(t), known)
