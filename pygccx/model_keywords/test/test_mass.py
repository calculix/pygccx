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
from model_keywords import Mass
from enums import ESetTypes
from protocols import IKeyword

@dataclass()
class SetMock():
    name:str
    type:ESetTypes
    dim:int
    ids:set[int]

class TestMass(TestCase):

    def setUp(self) -> None:
        self.nset = SetMock('N1', ESetTypes.NODE, 2, set([1,2,3,4]))
        self.eset = SetMock('E1', ESetTypes.ELEMENT, 1, set([1,2,3,4]))

    def test_is_IKeyword(self):
        m = Mass(self.eset, 1e3)
        self.assertTrue(isinstance(m, IKeyword))

    def test_happy_case(self):
        m = Mass(self.eset, 1e3)

        known = '*MASS,ELSET=E1\n'
        known += '1.0000000e+03\n'
        self.assertEqual(str(m), known)

    def test_wrong_set_type(self):
        self.assertRaises(ValueError, Mass, self.nset, 1e3)