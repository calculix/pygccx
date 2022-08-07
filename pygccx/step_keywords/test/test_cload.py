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
from step_keywords import Cload
from enums import ESetTypes, ELoadOps
from protocols import IKeyword

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
        c = Cload(99, 1, 1.234)
        self.assertTrue(isinstance(c, IKeyword))

    def test_default(self):
        c = Cload(99, 1, 1.234)
        known = '*CLOAD\n'
        known += '99,1,1.234\n'
        self.assertEqual(str(c), known)

    def test_default_with_set(self):
        s = SetMock('TestSet', ESetTypes.NODE, 2, set((1,2)))
        c = Cload(s, 1, 1.234)
        known = '*CLOAD\n'
        known += 'TestSet,1,1.234\n'
        self.assertEqual(str(c), known)

    def test_dof_lower_1(self):
        self.assertRaises(ValueError, Cload, 99, 0, 1.234)
        self.assertRaises(ValueError, Cload, 99, -1, 1.234)

    def test_nid_lower_1(self):
        self.assertRaises(ValueError, Cload, 0, 0, 1.234)
        self.assertRaises(ValueError, Cload, -1, -1, 1.234)

    def test_add_load(self):
        c = Cload(99, 1, 1.234)
        c.add_load(100, 2, 4.87)
        known = '*CLOAD\n'
        known += '99,1,1.234\n'
        known += '100,2,4.87\n'
        self.assertEqual(str(c), known)

    def test_op(self):
        c = Cload(99, 1, 1.234, op=ELoadOps.NEW)
        known = '*CLOAD,OP=NEW\n'
        known += '99,1,1.234\n'
        self.assertEqual(str(c), known)

    def test_amplitude(self):
        a = AmplitudeMock('A1')
        c = Cload(99, 1, 1.234, amplitude=a)
        known = '*CLOAD,AMPLITUDE=A1\n'
        known += '99,1,1.234\n'
        self.assertEqual(str(c), known)

    def test_time_delay(self):
        a = AmplitudeMock('A1')
        c = Cload(99, 1, 1.234, amplitude=a, time_delay=0.33)
        known = '*CLOAD,AMPLITUDE=A1,TIME DELAY=0.33\n'
        known += '99,1,1.234\n'
        self.assertEqual(str(c), known)

    def test_time_delay_wo_amplitude(self):
        # a time delay wo amplitude is not legit
        self.assertRaises(ValueError,Cload, 99, 1, 1.234, time_delay=0.33)

    def test_load_case(self):
        c = Cload(99, 1, 1.234, load_case=2)
        known = '*CLOAD,LOAD CASE=2\n'
        known += '99,1,1.234\n'
        self.assertEqual(str(c), known)

    def test_load_case_out_of_bounds(self):
        self.assertRaises(ValueError, Cload, 99, 1, 1.234, load_case=0)
        self.assertRaises(ValueError, Cload, 99, 1, 1.234, load_case=3)

    def test_sector(self):
        c = Cload(99, 1, 1.234, sector=2)
        known = '*CLOAD,SECTOR=2\n'
        known += '99,1,1.234\n'
        self.assertEqual(str(c), known)

    def test_sector_lower_1(self):
        self.assertRaises(ValueError, Cload, 99, 1, 1.234, sector=0)
        self.assertRaises(ValueError, Cload, 99, 1, 1.234, sector=-1)

    def test_submodel_and_step(self):
        c = Cload(99, 1, 1.234, submodel=True, step=1)
        known = '*CLOAD,SUBMODEL,STEP=1\n'
        known += '99,1,1.234\n'
        self.assertEqual(str(c), known) 

    def test_submodel_and_data_set(self):
        c = Cload(99, 1, 1.234, submodel=True, data_set=1)
        known = '*CLOAD,SUBMODEL,DATA SET=1\n'
        known += '99,1,1.234\n'
        self.assertEqual(str(c), known) 

    def test_step_wo_submodel(self):
        self.assertRaises(ValueError, Cload, 99, 1, 1.234, step=1)

    def test_step_lower_1(self):
        self.assertRaises(ValueError, Cload, 99, 1, 1.234, submodel=True, step=0)
        self.assertRaises(ValueError, Cload, 99, 1, 1.234, submodel=True, step=-1)

    def test_data_set_lower_1(self):
        self.assertRaises(ValueError, Cload, 99, 1, 1.234, submodel=True, data_set=0)
        self.assertRaises(ValueError, Cload, 99, 1, 1.234, submodel=True, data_set=-1)

    def test_step_and_data_set(self):
        self.assertRaises(ValueError, Cload, 99, 1, 1.234, submodel=True, data_set=1, step=1)


    def test_data_set_wo_submodel(self):
        self.assertRaises(ValueError, Cload, 99, 1, 1.234, data_set=1)

    def test_submodel_and_amplitude(self):
        a = AmplitudeMock('A1')
        self.assertRaises(ValueError, Cload, 99, 1, 1.234, submodel=True, step=1, amplitude=a)


