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
from model_keywords import ContactPair
from enums import EContactTypes, ESetTypes, ESurfTypes
from protocols import IKeyword

@dataclass
class InteractionMock:
    name:str
    desc:str = ''

@dataclass()
class SetMock():
    name:str
    type:ESetTypes
    dim:int
    ids:set[int]

@dataclass()
class SurfaceMock:
    name:str
    type: ESurfTypes
    def write_ccx(self, buffer:list[str]): pass

class TestContactPair(TestCase):

    def setUp(self) -> None:
        self.ia = InteractionMock('IA1')
        self.s = SetMock('TestSet', ESetTypes.NODE, 2, set((1,2)))
        self.se = SetMock('TestSet', ESetTypes.ELEMENT, 2, set((1,2)))
        self.dep_surf = SurfaceMock('dep_surf', ESurfTypes.EL_FACE)
        self.ind_surf = SurfaceMock('ind_surf', ESurfTypes.EL_FACE)
        self.dep_surf_node = SurfaceMock('dep_surf', ESurfTypes.NODE)
        self.ind_surf_node = SurfaceMock('ind_surf', ESurfTypes.NODE)

    def test_is_IKeyword(self):
        cp = ContactPair(self.ia, EContactTypes.NODE_TO_SURFACE, self.dep_surf, self.ind_surf)
        self.assertTrue(isinstance(cp, IKeyword))

    def test_default(self):
        cp = ContactPair(self.ia, EContactTypes.NODE_TO_SURFACE, self.dep_surf, self.ind_surf)
        known = '*CONTACT PAIR,INTERACTION=IA1,TYPE=NODE TO SURFACE\n'
        known += 'dep_surf,ind_surf\n'
        self.assertEqual(str(cp), known)

    def test_dep_surf_node(self):
        cp = ContactPair(self.ia, EContactTypes.NODE_TO_SURFACE, self.dep_surf_node, self.ind_surf)
        known = '*CONTACT PAIR,INTERACTION=IA1,TYPE=NODE TO SURFACE\n'
        known += 'dep_surf,ind_surf\n'
        self.assertEqual(str(cp), known)

    def test_small_sliding_yes(self):
        cp = ContactPair(self.ia, EContactTypes.NODE_TO_SURFACE, self.dep_surf, self.ind_surf, 
                            True)
        known = '*CONTACT PAIR,INTERACTION=IA1,TYPE=NODE TO SURFACE,SMALL SLIDING\n'
        known += 'dep_surf,ind_surf\n'
        self.assertEqual(str(cp), known)

    def test_small_sliding_no(self):
        cp = ContactPair(self.ia, EContactTypes.NODE_TO_SURFACE, self.dep_surf, self.ind_surf, 
                            False)
        known = '*CONTACT PAIR,INTERACTION=IA1,TYPE=NODE TO SURFACE\n'
        known += 'dep_surf,ind_surf\n'
        self.assertEqual(str(cp), known)

    def test_adjust_number(self):
        cp = ContactPair(self.ia, EContactTypes.NODE_TO_SURFACE, self.dep_surf, self.ind_surf, 
                            adjust=0.1)
        known = '*CONTACT PAIR,INTERACTION=IA1,TYPE=NODE TO SURFACE,ADJUST=1.0000000e-01\n'
        known += 'dep_surf,ind_surf\n'
        self.assertEqual(str(cp), known)

    def test_adjust_set(self):
        cp = ContactPair(self.ia, EContactTypes.NODE_TO_SURFACE, self.dep_surf, self.ind_surf, 
                            adjust=self.s)
        known = '*CONTACT PAIR,INTERACTION=IA1,TYPE=NODE TO SURFACE,ADJUST=TestSet\n'
        known += 'dep_surf,ind_surf\n'
        self.assertEqual(str(cp), known)

    def test_adjust_number_lower_zero(self):
        self.assertRaises(ValueError, ContactPair, self.ia, EContactTypes.NODE_TO_SURFACE, 
                            self.dep_surf, self.ind_surf, adjust=-0.1)

    def test_adjust_set_false_type(self):
        self.assertRaises(ValueError, ContactPair, self.ia, EContactTypes.NODE_TO_SURFACE, 
                            self.dep_surf, self.ind_surf, adjust=self.se)

    def test_ind_surf_false_type(self):
        # ind_surf must be of type EL_FACE
        self.assertRaises(ValueError, ContactPair, self.ia, EContactTypes.NODE_TO_SURFACE, 
                            self.dep_surf, self.ind_surf_node)

    def test_dep_surf_false_type(self):
        # ind_surf must be of type EL_FACE if contact type is SURFACE TO SURFACE
        self.assertRaises(ValueError, ContactPair, self.ia, EContactTypes.SURFACE_TO_SURFACE, 
                            self.dep_surf_node, self.ind_surf_node)
