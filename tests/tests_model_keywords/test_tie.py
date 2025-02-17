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

from turtle import position
from unittest import TestCase
from dataclasses import dataclass

from pygccx.model_keywords import Tie
from pygccx.protocols import IKeyword
from pygccx.enums import ESurfTypes

@dataclass()
class SurfaceMock:
    name:str
    type: ESurfTypes
    def write_ccx(self, buffer:list[str]): pass

class TestTie(TestCase):

    def setUp(self) -> None:
        self.surf_node = SurfaceMock('SN', ESurfTypes.NODE)
        self.surf_elem = SurfaceMock('SE', ESurfTypes.EL_FACE)

    def test_is_IKeyword(self):
        t = Tie('T1', self.surf_node, self.surf_elem)
        self.assertTrue(isinstance(t, IKeyword))

    def test_happy_case_simple_tie(self):
        # dep_surf = NODE, ind_surf=EL_FACE
        t = Tie('T1', self.surf_node, self.surf_elem)
        known = '*TIE,NAME=T1\n'
        known += 'SN,SE\n'
        self.assertEqual(str(t), known)

        # dep_surf = EL_FACE, ind_surf=EL_FACE
        t = Tie('T1', self.surf_elem, self.surf_elem)
        known = '*TIE,NAME=T1\n'
        known += 'SE,SE\n'
        self.assertEqual(str(t), known)

    def test_simple_tie_adjust_false(self):
        t = Tie('T1', self.surf_node, self.surf_elem, adjust=False)
        known = '*TIE,NAME=T1,ADJUST=NO\n'
        known += 'SN,SE\n'
        self.assertEqual(str(t), known)

    def test_simple_tie_position_tolerance(self):
        t = Tie('T1', self.surf_node, self.surf_elem, position_tolerance=0.1)
        known = '*TIE,NAME=T1,POSITION TOLERANCE=1.0000000e-01\n'
        known += 'SN,SE\n'
        self.assertEqual(str(t), known)

    def test_happy_case_cyclic_symmetry(self):
        # dep_surf = NODE, ind_surf=NODE
        t = Tie('T1', self.surf_node, self.surf_node, cyclic_symmetry=True)
        known = '*TIE,NAME=T1,CYCLIC SYMMETRY\n'
        known += 'SN,SN\n'
        self.assertEqual(str(t), known)
        # dep_surf = EL_FACE, ind_surf=EL_FACE
        t = Tie('T1', self.surf_elem, self.surf_elem, cyclic_symmetry=True)
        known = '*TIE,NAME=T1,CYCLIC SYMMETRY\n'
        known += 'SE,SE\n'
        self.assertEqual(str(t), known)
        # dep_surf = NODE, ind_surf=EL_FACE
        t = Tie('T1', self.surf_node, self.surf_elem, cyclic_symmetry=True)
        known = '*TIE,NAME=T1,CYCLIC SYMMETRY\n'
        known += 'SN,SE\n'
        self.assertEqual(str(t), known)
        # dep_surf = EL_FACE, ind_surf=NODE
        t = Tie('T1', self.surf_elem, self.surf_node, cyclic_symmetry=True)
        known = '*TIE,NAME=T1,CYCLIC SYMMETRY\n'
        known += 'SE,SN\n'
        self.assertEqual(str(t), known)

    def test_happy_case_multistage(self):
        # dep_surf = NODE, ind_surf=NODE
        t = Tie('T1', self.surf_node, self.surf_node, multistage=True)
        known = '*TIE,NAME=T1,MULTISTAGE\n'
        known += 'SN,SN\n'
        self.assertEqual(str(t), known)

    def test_cyclic_symmetry_and_multistage(self):
        self.assertRaises(ValueError, Tie, 'T1', self.surf_node, self.surf_node, 
                            multistage=True, cyclic_symmetry=True)

    def test_position_tolerance_lower_zero(self):
        self.assertRaises(ValueError, Tie, 'T1', self.surf_node, self.surf_elem, 
                            position_tolerance=-0.1)

    def test_simple_tie_wrong_ind_surf(self):
        self.assertRaises(ValueError, Tie, 'T1', self.surf_node, self.surf_node)

    def test_multistage_wrong_dep_surf(self):
        self.assertRaises(ValueError, Tie, 'T1', self.surf_elem, self.surf_node,
                            multistage=True)

    def test_multistage_wrong_ind_surf(self):
        self.assertRaises(ValueError, Tie, 'T1', self.surf_node, self.surf_elem,
                            multistage=True)

    def test_name_too_long(self):
        name = 'a' * 81
        self.assertRaises(ValueError, Tie, name, self.surf_node, self.surf_elem)