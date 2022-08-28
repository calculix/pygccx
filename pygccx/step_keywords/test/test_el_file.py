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

from pygccx.step_keywords import ElFile, TimePoints
from pygccx.enums import EElFileResults, EResultOutputs, ESetTypes
from pygccx.protocols import IKeyword

@dataclass()
class SetMock():
    name:str
    type:ESetTypes
    dim:int
    ids:set[int]

class TestElFile(TestCase):

    def setUp(self) -> None:
        self.nset = SetMock('N1', ESetTypes.NODE, 2, set([1,2,3,4]))
        self.eset = SetMock('E1', ESetTypes.ELEMENT, 2, set([1,2,3,4]))

    def test_is_IKeyword(self):
        ef = ElFile([EElFileResults.S, EElFileResults.E])
        self.assertTrue(isinstance(ef, IKeyword))

    def test_default(self):

        ef = ElFile([EElFileResults.S, EElFileResults.E])
        known = '*EL FILE\n'
        known +='S,E\n'
        self.assertEqual(str(ef), known)

    def test_frequency(self):

        ef = ElFile([EElFileResults.S], frequency=2)
        known = '*EL FILE,FREQUENCY=2\n'
        known +='S\n'
        self.assertEqual(str(ef), known)

    def test_time_points(self):
        tp = TimePoints('TP1', (1,2,3,4))
        ef = ElFile([EElFileResults.S], time_points=tp)
        known = '*EL FILE,TIME POINTS=TP1\n'
        known +='S\n'
        self.assertEqual(str(ef), known)

    def test_last_iteration(self):

        ef = ElFile([EElFileResults.S], last_Iterations=True)
        known = '*EL FILE,LAST ITERATIONS\n'
        known +='S\n'
        self.assertEqual(str(ef), known)

    def test_contact_elements(self):

        ef = ElFile([EElFileResults.S], contact_elements=True)
        known = '*EL FILE,CONTACT ELEMENTS\n'
        known +='S\n'
        self.assertEqual(str(ef), known)

    def test_global_no(self):

        ef = ElFile([EElFileResults.S], global_=False)
        known = '*EL FILE,GLOBAL=NO\n'
        known +='S\n'
        self.assertEqual(str(ef), known)

    def test_output_all(self):

        ef = ElFile([EElFileResults.S], output_all=True)
        known = '*EL FILE,OUTPUT ALL\n'
        known +='S\n'
        self.assertEqual(str(ef), known)

    def test_output_2D(self):

        ef = ElFile([EElFileResults.S], output=EResultOutputs._2D)
        known = '*EL FILE,OUTPUT=2D\n'
        known +='S\n'
        self.assertEqual(str(ef), known)

    def test_section_forces(self):

        ef = ElFile([EElFileResults.S], section_forces=True)
        known = '*EL FILE,SECTION FORCES\n'
        known +='S\n'
        self.assertEqual(str(ef), known)

    def test_nset(self):

        nf = ElFile([EElFileResults.S], nset=self.nset)
        known = '*EL FILE,NSET=N1\n'
        known +='S\n'
        self.assertEqual(str(nf), known)

    def test_empty_entities(self):
        self.assertRaises(ValueError, ElFile, [])

    def test_time_points_and_frequency(self):
        tp = TimePoints('TP1', (1,2,3,4))
        self.assertRaises(ValueError, ElFile, [EElFileResults.S], time_points=tp, frequency=2)

    def test_section_forces_and_output_3D(self):
        self.assertRaises(ValueError, ElFile, [EElFileResults.S], section_forces=True, output=EResultOutputs._3D)

    def test_wrong_set_type(self):
        self.assertRaises(ValueError, ElFile, [EElFileResults.S], nset=self.eset)