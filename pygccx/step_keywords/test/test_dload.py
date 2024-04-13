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

from pygccx.step_keywords import Dload
from pygccx.enums import ESetTypes, ELoadOps, EDloadType
from pygccx.protocols import IKeyword

@dataclass
class AmplitudeMock:
    name:str
    desc:str = ''

@dataclass()
class SetMock():
    name:str
    type:ESetTypes
    dim:int
    ids:set[int]

class TestCload(TestCase):

    def test_is_IKeyword(self):
        d = Dload(99, EDloadType.NEWTON, tuple())
        self.assertTrue(isinstance(d, IKeyword))

    def test_Px(self):
        d = Dload(99, EDloadType.P4, (10,))
        known = '*DLOAD\n'
        known += '99,P4,1.0000000e+01\n'
        self.assertEqual(str(d), known)
        
    def test_centrif(self):
        d = Dload(99, EDloadType.CENTRIF, (10000, 0, 0, 0, 1, 0, 0))
        known = '*DLOAD\n'
        known += '99,CENTRIF,1.0000000e+04,0.0000000e+00,0.0000000e+00,0.0000000e+00,1.0000000e+00,0.0000000e+00,0.0000000e+00\n'
        self.assertEqual(str(d), known)

    def test_newton(self):
        d = Dload(99, EDloadType.NEWTON, tuple())
        known = '*DLOAD\n'
        known += '99,NEWTON\n'
        self.assertEqual(str(d), known)
        
    def test_gravity(self):
        d = Dload(99, EDloadType.GRAV, (9810, 0, 0, -1))
        known = '*DLOAD\n'
        known += '99,GRAV,9.8100000e+03,0.0000000e+00,0.0000000e+00,-1.0000000e+00\n'
        self.assertEqual(str(d), known)

    def test_Px_with_set(self):
        s = SetMock('TestSet', ESetTypes.NODE, 2, set((1,2)))
        d = Dload(s, EDloadType.P4, (10,))
        known = '*DLOAD\n'
        known += 'TestSet,P4,1.0000000e+01\n'
        self.assertEqual(str(d), known)

    def test_centrif_with_set(self):
        s = SetMock('TestSet', ESetTypes.NODE, 2, set((1,2)))
        d = Dload(s, EDloadType.CENTRIF, (10000, 0, 0, 0, 1, 0, 0))
        known = '*DLOAD\n'
        known += 'TestSet,CENTRIF,1.0000000e+04,0.0000000e+00,0.0000000e+00,0.0000000e+00,1.0000000e+00,0.0000000e+00,0.0000000e+00\n'
        self.assertEqual(str(d), known)

    def test_newton_with_set(self):
        s = SetMock('TestSet', ESetTypes.NODE, 2, set((1,2)))
        d = Dload(s, EDloadType.NEWTON, tuple())
        known = '*DLOAD\n'
        known += 'TestSet,NEWTON\n'
        self.assertEqual(str(d), known)
        
    def test_gravity_with_set(self):
        s = SetMock('TestSet', ESetTypes.NODE, 2, set((1,2)))
        d = Dload(s, EDloadType.GRAV, (9810, 0, 0, -1))
        known = '*DLOAD\n'
        known += 'TestSet,GRAV,9.8100000e+03,0.0000000e+00,0.0000000e+00,-1.0000000e+00\n'
        self.assertEqual(str(d), known)

    def test_gravity_norm(self):
        """Check if not normalized components raise an error."""
        self.assertRaises(ValueError, Dload, 99, EDloadType.GRAV, (10000, 2,1,-1))

    def test_centrif_norm(self):
        """Check if not normalized components raise an error."""
        self.assertRaises(ValueError, Dload, 99, EDloadType.CENTRIF, (10,0,0,0,1.001,0,0))

    def test_nid_lower_1(self):
        self.assertRaises(ValueError, Dload, 0, EDloadType.NEWTON, tuple())
        self.assertRaises(ValueError, Dload, -1, EDloadType.NEWTON, tuple())

    def test_add_load(self):
        d = Dload(99, EDloadType.GRAV, (9810, 0, 0, -1))
        d.add_load(100, EDloadType.CENTRIF, (10000, 0, 0, 0, 1, 0, 0))
        known = '*DLOAD\n'
        known += '99,GRAV,9.8100000e+03,0.0000000e+00,0.0000000e+00,-1.0000000e+00\n'
        known += '100,CENTRIF,1.0000000e+04,0.0000000e+00,0.0000000e+00,0.0000000e+00,1.0000000e+00,0.0000000e+00,0.0000000e+00\n'
        self.assertEqual(str(d), known)

    def test_op(self):
        d = Dload(99, EDloadType.NEWTON, tuple(), op=ELoadOps.NEW)
        known = '*DLOAD,OP=NEW\n'
        known += '99,NEWTON\n'
        self.assertEqual(str(d), known)

    def test_amplitude(self):
        a = AmplitudeMock('A1')
        c = Dload(99, EDloadType.NEWTON, tuple(), amplitude=a)
        known = '*DLOAD,AMPLITUDE=A1\n'
        known += '99,NEWTON\n'
        self.assertEqual(str(c), known)

    def test_time_delay(self):
        a = AmplitudeMock('A1')
        c = Dload(99, EDloadType.NEWTON, tuple(), amplitude=a, time_delay=0.33)
        known = '*DLOAD,AMPLITUDE=A1,TIME DELAY=3.3000000e-01\n'
        known += '99,NEWTON\n'
        self.assertEqual(str(c), known)

    def test_time_delay_wo_amplitude(self):
        # a time delay wo amplitude is not legit
        self.assertRaises(ValueError,Dload, 99, EDloadType.NEWTON, tuple(), time_delay=0.33)

    def test_load_case(self):
        d = Dload(99, EDloadType.GRAV, (9810, 0, 0, -1), load_case=2)
        known = '*DLOAD,LOAD CASE=2\n'
        known += '99,GRAV,9.8100000e+03,0.0000000e+00,0.0000000e+00,-1.0000000e+00\n'
        self.assertEqual(str(d), known)

    def test_load_case_out_of_bounds(self):
        self.assertRaises(ValueError, Dload, 99, EDloadType.NEWTON, tuple(), load_case=0)
        self.assertRaises(ValueError, Dload, 99, EDloadType.NEWTON, tuple(), load_case=3)

    def test_sector(self):
        c = Dload(99, EDloadType.NEWTON, tuple(), sector=2)
        known = '*DLOAD,SECTOR=2\n'
        known += '99,NEWTON\n'
        self.assertEqual(str(c), known)

    def test_sector_lower_1(self):
        self.assertRaises(ValueError, Dload, 99, EDloadType.NEWTON, tuple(), sector=0)
        self.assertRaises(ValueError, Dload, 99, EDloadType.NEWTON, tuple(), sector=-1)

