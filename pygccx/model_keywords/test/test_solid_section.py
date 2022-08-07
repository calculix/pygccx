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
from model_keywords import SolidSection
from enums import ESetTypes
from protocols import IKeyword

@dataclass()
class SetMock():
    name:str
    type:ESetTypes
    dim:int
    ids:set[int]

@dataclass
class FeatureMock():
    name:str
    desc:str = ''

class TestSolidSection(TestCase):

    def setUp(self) -> None:
        self.s = SetMock('SET1', ESetTypes.ELEMENT, 2, set((1,2,3,4)))
        self.mat = FeatureMock('MAT1')
        self.ori = FeatureMock('OR1')

    def test_is_IKeyword(self):
        sos = SolidSection(self.s, self.mat)
        self.assertTrue(isinstance(sos, IKeyword))
    
    def test_wo_orientation(self):
        sos = SolidSection(self.s, self.mat)
        known = '*SOLID SECTION,MATERIAL=MAT1,ELSET=SET1\n'
        self.assertEqual(str(sos), known)

    def test_w_orientation(self):
        sos = SolidSection(self.s, self.mat, self.ori)
        known = '*SOLID SECTION,MATERIAL=MAT1,ELSET=SET1,ORIENTATION=OR1\n'
        self.assertEqual(str(sos), known)

    def test_false_set_type(self):
        s = SetMock('SET1', ESetTypes.NODE, 2, set((1,2,3,4)))
        mat = FeatureMock('MAT1')
        self.assertRaises(ValueError, SolidSection, s, mat)