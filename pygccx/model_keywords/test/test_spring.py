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
from model_keywords import SpringLin, SpringNonlin
from enums import EPressureOverclosures, ESetTypes
from protocols import IKeyword

@dataclass()
class SetMock():
    name:str
    type:ESetTypes
    dim:int
    ids:set[int]

@dataclass()
class OrientationMock():
    name:str
    desc:str = ''

class TestSpringLin(TestCase):

    def setUp(self) -> None:
        self.nset = SetMock('S1', ESetTypes.NODE, 1, set([1,2,3,4]))
        self.elset = SetMock('S1', ESetTypes.ELEMENT, 1, set([1,2,3,4]))
        self.ori = OrientationMock('O1')

    def test_default_spring_a(self):
        sp = SpringLin(self.elset, 10)
        known = '*SPRING,ELSET=S1\n'
        known += '\n'
        known += '1.0000000e+01,,2.9400000e+02\n'
        self.assertEqual(str(sp), known)

    def test_default_spring_1(self):
        sp = SpringLin(self.elset, 10, first_dof=2)
        known = '*SPRING,ELSET=S1\n'
        known += '2\n'
        known += '1.0000000e+01,,2.9400000e+02\n'
        self.assertEqual(str(sp), known)

    def test_default_spring_2(self):
        sp = SpringLin(self.elset, 10, first_dof=2, second_dof=3)
        known = '*SPRING,ELSET=S1\n'
        known += '2,3\n'
        known += '1.0000000e+01,,2.9400000e+02\n'
        self.assertEqual(str(sp), known)

    def test_default_orientation(self):
        sp = SpringLin(self.elset, 10, orientation=self.ori)
        known = '*SPRING,ELSET=S1,ORIENTATION=O1\n'
        known += '\n'
        known += '1.0000000e+01,,2.9400000e+02\n'
        self.assertEqual(str(sp), known)

    def test_add_stiffness_for_temp(self):
        sp = SpringLin(self.elset, 10)
        sp.add_stiffness_for_temp(300, 12)
        known = '*SPRING,ELSET=S1\n'
        known += '\n'
        known += '1.0000000e+01,,2.9400000e+02\n'
        known += '1.2000000e+01,,3.0000000e+02\n'
        self.assertEqual(str(sp), known)
        
    def test_wrong_set_type(self):
        self.assertRaises(ValueError, SpringLin, self.nset, 10)

    def test_first_dof_too_low(self):
        self.assertRaises(ValueError, SpringLin, self.elset, 10, first_dof=0)
        self.assertRaises(ValueError, SpringLin, self.elset, 10, first_dof=-1)

    def test_second_dof_too_low(self):
        self.assertRaises(ValueError, SpringLin, self.elset, 10, first_dof=1, second_dof=0)
        self.assertRaises(ValueError, SpringLin, self.elset, 10, first_dof=1, second_dof=-1)

    def test_second_dof_given_but_no_first_dof(self):
        self.assertRaises(ValueError, SpringLin, self.elset, 10, second_dof=1)
        sp = SpringLin(self.elset, 10, first_dof=2, second_dof=3)
        def change_first_dof_to_none():
            sp.first_dof = None
        self.assertRaises(ValueError, change_first_dof_to_none)

class TestSpringNonlin(TestCase):

    def setUp(self) -> None:
        self.nset = SetMock('S1', ESetTypes.NODE, 1, set([1,2,3,4]))
        self.elset = SetMock('S1', ESetTypes.ELEMENT, 1, set([1,2,3,4]))
        self.ori = OrientationMock('O1')

    def test_default_spring_a(self):
        sp = SpringNonlin(self.elset, [0,10,100], [0,1,2])
        known = '*SPRING,ELSET=S1,NONLINEAR\n'
        known += '\n'
        known += '  0.0000000e+00,  0.0000000e+00,  2.9400000e+02\n'
        known += '  1.0000000e+01,  1.0000000e+00,  2.9400000e+02\n'
        known += '  1.0000000e+02,  2.0000000e+00,  2.9400000e+02\n'
        self.assertEqual(str(sp), known)

    def test_default_spring_1(self):
        sp = SpringNonlin(self.elset, [0,10,100], [0,1,2], first_dof=2)
        known = '*SPRING,ELSET=S1,NONLINEAR\n'
        known += '2\n'
        known += '  0.0000000e+00,  0.0000000e+00,  2.9400000e+02\n'
        known += '  1.0000000e+01,  1.0000000e+00,  2.9400000e+02\n'
        known += '  1.0000000e+02,  2.0000000e+00,  2.9400000e+02\n'
        self.assertEqual(str(sp), known)

    def test_default_spring_2(self):
        sp = SpringNonlin(self.elset, [0,10,100], [0,1,2], first_dof=2, second_dof=3)
        known = '*SPRING,ELSET=S1,NONLINEAR\n'
        known += '2,3\n'
        known += '  0.0000000e+00,  0.0000000e+00,  2.9400000e+02\n'
        known += '  1.0000000e+01,  1.0000000e+00,  2.9400000e+02\n'
        known += '  1.0000000e+02,  2.0000000e+00,  2.9400000e+02\n'
        self.assertEqual(str(sp), known)

    def test_default_orientation(self):
        sp = SpringNonlin(self.elset, [0,10,100], [0,1,2], orientation=self.ori)
        known = '*SPRING,ELSET=S1,NONLINEAR,ORIENTATION=O1\n'
        known += '\n'
        known += '  0.0000000e+00,  0.0000000e+00,  2.9400000e+02\n'
        known += '  1.0000000e+01,  1.0000000e+00,  2.9400000e+02\n'
        known += '  1.0000000e+02,  2.0000000e+00,  2.9400000e+02\n'

    def test_add_stiffness_for_temp(self):
        sp = SpringNonlin(self.elset, [0,10,100], [0,1,2])
        sp.add_force_elong_for_temp(300, [0,20,200], [0,1,2])
        known = '*SPRING,ELSET=S1,NONLINEAR,ORIENTATION=O1\n'
        known += '\n'
        known += '  0.0000000e+00,  0.0000000e+00,  2.9400000e+02\n'
        known += '  1.0000000e+01,  1.0000000e+00,  2.9400000e+02\n'
        known += '  1.0000000e+02,  2.0000000e+00,  2.9400000e+02\n'
        known += '  0.0000000e+00,  0.0000000e+00,  3.0000000e+02\n'
        known += '  2.0000000e+01,  1.0000000e+00,  3.0000000e+02\n'
        known += '  2.0000000e+02,  2.0000000e+00,  3.0000000e+02\n'
        
    def test_wrong_set_type(self):
        self.assertRaises(ValueError, SpringNonlin, self.nset, [0,10,100], [0,1,2])

    def test_first_dof_too_low(self):
        self.assertRaises(ValueError, SpringNonlin, self.nset, [0,10,100], [0,1,2], first_dof=0)
        self.assertRaises(ValueError, SpringNonlin, self.nset, [0,10,100], [0,1,2], first_dof=-1)

    def test_second_dof_too_low(self):
        self.assertRaises(ValueError, SpringNonlin, self.nset, [0,10,100], [0,1,2], first_dof=1, second_dof=0)
        self.assertRaises(ValueError, SpringNonlin, self.nset, [0,10,100], [0,1,2], first_dof=1, second_dof=-1)

    def test_second_dof_given_but_no_first_dof(self):
        self.assertRaises(ValueError, SpringNonlin, self.nset, [0,10,100], [0,1,2], second_dof=1)
        sp = SpringNonlin(self.elset, [0,10,100], [0,1,2], first_dof=2, second_dof=3)
        def change_first_dof_to_none():
            sp.first_dof = None
        self.assertRaises(ValueError, change_first_dof_to_none)

    def test_force_elong_different_lengths(self):
        self.assertRaises(ValueError, SpringNonlin, self.nset, [0,10,100], [0,1])