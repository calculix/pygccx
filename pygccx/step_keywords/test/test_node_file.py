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
from step_keywords import NodeFile, TimePoints
from enums import ENodeFileResults, EResultOutputs, ESetTypes
from protocols import IKeyword

@dataclass()
class SetMock():
    name:str
    type:ESetTypes
    dim:int
    ids:set[int]
class TestNodeFile(TestCase):

    def setUp(self) -> None:
        self.nset = SetMock('N1', ESetTypes.NODE, 2, set([1,2,3,4]))
        self.eset = SetMock('E1', ESetTypes.ELEMENT, 2, set([1,2,3,4]))

    def test_is_IKeyword(self):
        nf = NodeFile([ENodeFileResults.U, ENodeFileResults.RF])
        self.assertTrue(isinstance(nf, IKeyword))

    def test_default(self):

        nf = NodeFile([ENodeFileResults.U, ENodeFileResults.RF])
        known = '*NODE FILE\n'
        known +='U,RF\n'
        self.assertEqual(str(nf), known)

    def test_frequency(self):

        nf = NodeFile([ENodeFileResults.U, ENodeFileResults.RF], frequency=2)
        known = '*NODE FILE,FREQUENCY=2\n'
        known +='U,RF\n'
        self.assertEqual(str(nf), known)

    def test_time_points(self):
        tp = TimePoints('TP1', (1,2,3,4))
        nf = NodeFile([ENodeFileResults.U, ENodeFileResults.RF], time_points=tp)
        known = '*NODE FILE,TIME POINTS=TP1\n'
        known +='U,RF\n'
        self.assertEqual(str(nf), known)

    def test_last_iteration(self):

        nf = NodeFile([ENodeFileResults.U, ENodeFileResults.RF], last_Iterations=True)
        known = '*NODE FILE,LAST ITERATIONS\n'
        known +='U,RF\n'
        self.assertEqual(str(nf), known)

    def test_contact_elements(self):

        nf = NodeFile([ENodeFileResults.U, ENodeFileResults.RF], contact_elements=True)
        known = '*NODE FILE,CONTACT ELEMENTS\n'
        known +='U,RF\n'
        self.assertEqual(str(nf), known)

    def test_global_no(self):

        nf = NodeFile([ENodeFileResults.U, ENodeFileResults.RF], global_=False)
        known = '*NODE FILE,GLOBAL=NO\n'
        known +='U,RF\n'
        self.assertEqual(str(nf), known)

    def test_output_all(self):

        nf = NodeFile([ENodeFileResults.U, ENodeFileResults.RF], output_all=True)
        known = '*NODE FILE,OUTPUT ALL\n'
        known +='U,RF\n'
        self.assertEqual(str(nf), known)

    def test_output_2D(self):

        nf = NodeFile([ENodeFileResults.U, ENodeFileResults.RF], output=EResultOutputs._2D)
        known = '*NODE FILE,OUTPUT=2D\n'
        known +='U,RF\n'
        self.assertEqual(str(nf), known)

    def test_nset(self):

        nf = NodeFile([ENodeFileResults.U, ENodeFileResults.RF], nset=self.nset)
        known = '*NODE FILE,NSET=N1\n'
        known +='U,RF\n'
        self.assertEqual(str(nf), known)

    def test_empty_entities(self):
        self.assertRaises(ValueError, NodeFile, [])

    def test_time_points_and_frequency(self):
        tp = TimePoints('TP1', (1,2,3,4))
        self.assertRaises(ValueError, NodeFile, [ENodeFileResults.U], time_points=tp, frequency=2)

    def test_wrong_set_type(self):
        self.assertRaises(ValueError, NodeFile, [ENodeFileResults.U], nset=self.eset)
