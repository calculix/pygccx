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
from model_keywords import Boundary
from enums import ESetTypes
from protocols import IModelFeature

@dataclass()
class SetMock():
    name:str
    type:ESetTypes
    dim:int
    ids:set[int]

class TestBoundary(TestCase):

    def test_is_IModelFeature(self):
        b = Boundary(1, 1, 3)
        self.assertTrue(isinstance(b, IModelFeature))

    def test_first_dof_and_last_dof(self):

        b = Boundary(1, 1, 3)
        b.add_condition(2,1,2)

        known = '*BOUNDARY\n1,1,3\n2,1,2\n'
        self.assertEqual(str(b), known)

    def test_wo_last_dof(self):

        b = Boundary(1, 2)
        b.add_condition(2,1)

        known = '*BOUNDARY\n1,2\n2,1\n'
        self.assertEqual(str(b), known)

    def test_with_set(self):
        s = SetMock('TestSet', ESetTypes.NODE, 2, set((1,2)))
        b = Boundary(s, 1, 3)

        known = '*BOUNDARY\nTestSet,1,3\n'
        self.assertEqual(str(b), known)

    def test_nid_lower_one(self):
        self.assertRaises(ValueError, Boundary, 0, 1)
        self.assertRaises(ValueError, Boundary, -1, 1)

    def test_first_dof_lower_one(self):
        self.assertRaises(ValueError, Boundary, 1, 0)
        self.assertRaises(ValueError, Boundary, 1, -1)

    def test_last_dof_not_greater_first_dof(self):
        self.assertRaises(ValueError, Boundary, 1, 1, 0)
        self.assertRaises(ValueError, Boundary, 1, 1, 1)






