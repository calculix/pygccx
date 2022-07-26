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
from model_features import RigidBody
from enums import ESetTypes
from protocols import IModelFeature

@dataclass()
class SetMock():
    name:str
    type:ESetTypes
    dim:int
    ids:set[int]


class TestRigidBody(TestCase):

    def setUp(self) -> None:
        self.nset = SetMock('TestSet', ESetTypes.NODE, 2, set((1, 2)))
        self.eset = SetMock('TestSet', ESetTypes.ELEMENT, 2, set((1, 2)))

    def test_is_IModelFeature(self):
        rb = RigidBody(self.nset, 1, 2)
        self.assertTrue(isinstance(rb, IModelFeature))

    def test_node_set_and_ref_node_and_rot_node(self):
      
        rb = RigidBody(self.nset, 1, 2)

        known = '*RIGID BODY,NSET=TestSet,REF NODE=1,ROT NODE=2\n'
        self.assertEqual(str(rb), known)

    def test_element_set_and_ref_node_and_rot_node(self):

        rb = RigidBody(self.eset, 1, 2)

        known = '*RIGID BODY,ELSET=TestSet,REF NODE=1,ROT NODE=2\n'
        self.assertEqual(str(rb), known)

    def test_wo_rot_node(self):

        rb = RigidBody(self.nset,1)

        known = '*RIGID BODY,NSET=TestSet,REF NODE=1\n'
        self.assertEqual(str(rb), known)

    def test_ref_node_lower_0(self):
        self.assertRaises(ValueError, RigidBody, self.nset, -1, 2)

    def test_rot_node_lower_0(self):
        self.assertRaises(ValueError, RigidBody, self.nset, 1, -2)





