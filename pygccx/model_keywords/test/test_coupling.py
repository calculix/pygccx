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
from model_keywords import Coupling
from enums import ESurfTypes, ECouplingTypes
from protocols import IKeyword

@dataclass
class SurfaceMock:
    name:str
    type: ESurfTypes
    def write_ccx(self, buffer:list[str]): pass

@dataclass
class OrientationMock:
    name:str
    desc:str = ''

class TestCoupling(TestCase):

    def setUp(self) -> None:
        self.surf = SurfaceMock('S1', ESurfTypes.EL_FACE)
        self.ori = OrientationMock('O1')

    def test_is_IKeyword(self):
        c = Coupling(ECouplingTypes.DISTRIBUTING,
                        ref_node=1, surface=self.surf,
                        name='C1', first_dof=1)
        self.assertTrue(isinstance(c, IKeyword))

    def test_default(self):
        c = Coupling(ECouplingTypes.DISTRIBUTING,
                        ref_node=1, surface=self.surf,
                        name='C1', first_dof=1)

        known = '*COUPLING,CONSTRAINT NAME=C1,REF NODE=1,SURFACE=S1\n'
        known += '*DISTRIBUTING\n'
        known += '1\n'

        self.assertEqual(str(c), known)

    def test_default_kinematic(self):
        c = Coupling(ECouplingTypes.KINEMATIC,
                        ref_node=1, surface=self.surf,
                        name='C1', first_dof=1)

        known = '*COUPLING,CONSTRAINT NAME=C1,REF NODE=1,SURFACE=S1\n'
        known += '*KINEMATIC\n'
        known += '1\n'

        self.assertEqual(str(c), known)

    def test_last_dof(self):
        c = Coupling(ECouplingTypes.DISTRIBUTING,
                        ref_node=1, surface=self.surf,
                        name='C1', first_dof=1, last_dof=4)

        known = '*COUPLING,CONSTRAINT NAME=C1,REF NODE=1,SURFACE=S1\n'
        known += '*DISTRIBUTING\n'
        known += '1,4\n'

        self.assertEqual(str(c), known)

    def test_orientation(self):
        c = Coupling(ECouplingTypes.DISTRIBUTING,
                        ref_node=1, surface=self.surf,
                        name='C1', first_dof=1,
                        orientation=self.ori)

        known = '*COUPLING,CONSTRAINT NAME=C1,REF NODE=1,SURFACE=S1,ORIENTATION=O1\n'
        known += '*DISTRIBUTING\n'
        known += '1\n'

        self.assertEqual(str(c), known)