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
from model_keywords import Gap
from protocols import IKeyword
from enums import ESetTypes

@dataclass()
class SetMock():
    name:str
    type:ESetTypes
    dim:int
    ids:set[int]

class TestGap(TestCase):

    def setUp(self) -> None:
        self.nset = SetMock('N1', ESetTypes.NODE, 1, set([1,2,3,4]))
        self.elset = SetMock('E1', ESetTypes.ELEMENT, 1, set([1,2,3,4]))

    def test_is_IKeyword(self):
        g = Gap(self.elset, 0, [1,0,0])
        self.assertTrue(isinstance(g, IKeyword))

    def test_default(self):
        g = Gap(self.elset, 0, [1,0,0])
        known = '*GAP,ELSET=E1\n'
        known += '0.0000000e+00,1.0000000e+00,0.0000000e+00,0.0000000e+00\n'
        self.assertEqual(str(g), known)

    def test_clearance(self):
        g = Gap(self.elset, 0.1, [1,0,0])
        known = '*GAP,ELSET=E1\n'
        known += '1.0000000e-01,1.0000000e+00,0.0000000e+00,0.0000000e+00\n'
        self.assertEqual(str(g), known)

    def test_k(self):
        g = Gap(self.elset, 0, [1,0,0], k=1000.)
        known = '*GAP,ELSET=E1\n'
        known += '0.0000000e+00,1.0000000e+00,0.0000000e+00,0.0000000e+00,,1.0000000e+03\n'
        self.assertEqual(str(g), known)

    def test_f_inf(self):
        g = Gap(self.elset, 0, [1,0,0], f_inf=0.5)
        known = '*GAP,ELSET=E1\n'
        known += '0.0000000e+00,1.0000000e+00,0.0000000e+00,0.0000000e+00,,,5.0000000e-01\n'
        self.assertEqual(str(g), known)

    def test_k_and_f_inf(self):
        g = Gap(self.elset, 0, [1,0,0], k=1000., f_inf=0.5)
        known = '*GAP,ELSET=E1\n'
        known += '0.0000000e+00,1.0000000e+00,0.0000000e+00,0.0000000e+00,,1.0000000e+03,5.0000000e-01\n'
        self.assertEqual(str(g), known)

    def test_elset_wrong_type(self):
        self.assertRaises(ValueError, Gap, self.nset, 0, [1,0,0])

    def test_length_of_normal_not_3(self):
        self.assertRaises(ValueError, Gap, self.nset, 0, [1,0])

    def test_k_not_greater_0(self):
        self.assertRaises(ValueError, Gap, self.elset, 0, [1,0,0], k=0)
        self.assertRaises(ValueError, Gap, self.elset, 0, [1,0,0], k=-1)

    def test_f_inf_not_greater_0(self):
        self.assertRaises(ValueError, Gap, self.elset, 0, [1,0,0], f_inf=0)
        self.assertRaises(ValueError, Gap, self.elset, 0, [1,0,0], f_inf=-1)

    def test_norm_of_normal_not_1(self):
        self.assertRaises(ValueError, Gap, self.elset, 0, [2,0,0])



