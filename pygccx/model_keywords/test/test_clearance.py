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
from model_keywords import Clearance
from enums import ESurfTypes
from protocols import IKeyword

@dataclass
class SurfaceMock:
    name:str
    type: ESurfTypes
    def write_ccx(self, buffer:list[str]): pass

class TestClearance(TestCase):

    def setUp(self) -> None:
        self.s1 = SurfaceMock('S1', ESurfTypes.EL_FACE)
        self.s2 = SurfaceMock('S2', ESurfTypes.EL_FACE)

    def test_is_IKeyword(self):
        c = Clearance(self.s1, self.s2, 0.1)
        self.assertTrue(isinstance(c, IKeyword))

    def test_default(self):
        c = Clearance(self.s1, self.s2, 0.1)
        known = '*CLEARANCE,MASTER=S1,SLAVE=S2,VALUE=1.0000000e-01\n'
        self.assertEqual(str(c), known)