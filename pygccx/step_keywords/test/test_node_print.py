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
from step_keywords import NodePrint, TimePoints
from enums import ENodePrintResults, ESetTypes, EPrintTotals
from protocols import IKeyword

@dataclass()
class SetMock():
    name:str
    type:ESetTypes
    dim:int
    ids:set[int]

class TestNodePrint(TestCase):

    def setUp(self) -> None:
        self.nset = SetMock('N1', ESetTypes.NODE, 2, set([1,2,3,4]))
        self.eset = SetMock('E1', ESetTypes.ELEMENT, 2, set([1,2,3,4]))

    def test_is_IKeyword(self):
        np = NodePrint(self.nset,[ENodePrintResults.U, ENodePrintResults.RF])
        self.assertTrue(isinstance(np, IKeyword))

    def test_default(self):

        np = NodePrint(self.nset,[ENodePrintResults.U, ENodePrintResults.RF])
        known = '*NODE PRINT,NSET=N1\n'
        known +='U,RF\n'
        self.assertEqual(str(np), known)

    def test_frequency(self):

        np = NodePrint(self.nset,[ENodePrintResults.U, ENodePrintResults.RF], frequency=2)
        known = '*NODE PRINT,NSET=N1,FREQUENCY=2\n'
        known +='U,RF\n'
        self.assertEqual(str(np), known)

    def test_time_points(self):
        tp = TimePoints('TP1', (1,2,3,4))
        np = NodePrint(self.nset,[ENodePrintResults.U, ENodePrintResults.RF], time_points=tp)
        known = '*NODE PRINT,NSET=N1,TIME POINTS=TP1\n'
        known +='U,RF\n'
        self.assertEqual(str(np), known)

    def test_totals(self):
        np = NodePrint(self.nset,[ENodePrintResults.U, ENodePrintResults.RF], totals=EPrintTotals.YES)
        known = '*NODE PRINT,NSET=N1,TOTALS=YES\n'
        known +='U,RF\n'
        self.assertEqual(str(np), known)
        np = NodePrint(self.nset,[ENodePrintResults.U, ENodePrintResults.RF], totals=EPrintTotals.ONLY)
        known = '*NODE PRINT,NSET=N1,TOTALS=ONLY\n'
        known +='U,RF\n'
        self.assertEqual(str(np), known)

    def test_global_no(self):

        np = NodePrint(self.nset,[ENodePrintResults.U, ENodePrintResults.RF], global_=False)
        known = '*NODE PRINT,NSET=N1,GLOBAL=NO\n'
        known +='U,RF\n'
        self.assertEqual(str(np), known)

    def test_empty_entities(self):
        self.assertRaises(ValueError, NodePrint, self.nset, [])

    def test_time_points_and_frequency(self):
        tp = TimePoints('TP1', (1,2,3,4))
        self.assertRaises(ValueError, NodePrint, self.nset, [ENodePrintResults.U], time_points=tp, frequency=2)

    def test_wrong_set_type(self):
        self.assertRaises(ValueError, NodePrint, self.eset, [ENodePrintResults.U])