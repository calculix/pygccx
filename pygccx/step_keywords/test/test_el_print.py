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

from pygccx.step_keywords import ElPrint, TimePoints
from pygccx.enums import EElPrintResults, ESetTypes, EPrintTotals
from pygccx.protocols import IKeyword

@dataclass()
class SetMock():
    name:str
    type:ESetTypes
    dim:int
    ids:set[int]

class TestElPrint(TestCase):

    def setUp(self) -> None:
        self.nset = SetMock('N1', ESetTypes.NODE, 2, set([1,2,3,4]))
        self.eset = SetMock('E1', ESetTypes.ELEMENT, 2, set([1,2,3,4]))

    def test_is_IKeyword(self):
        ep = ElPrint(self.eset,[EElPrintResults.S])
        self.assertTrue(isinstance(ep, IKeyword))

    def test_default(self):

        ep = ElPrint(self.eset,[EElPrintResults.S])
        known = '*EL PRINT,ELSET=E1\n'
        known +='S\n'
        self.assertEqual(str(ep), known)

    def test_frequency(self):

        ep = ElPrint(self.eset,[EElPrintResults.S], frequency=2)
        known = '*EL PRINT,ELSET=E1,FREQUENCY=2\n'
        known +='S\n'
        self.assertEqual(str(ep), known)

    def test_time_points(self):
        tp = TimePoints('TP1', (1,2,3,4))
        ep = ElPrint(self.eset,[EElPrintResults.S], time_points=tp)
        known = '*EL PRINT,ELSET=E1,TIME POINTS=TP1\n'
        known +='S\n'
        self.assertEqual(str(ep), known)

    def test_totals(self):
        ep = ElPrint(self.eset,[EElPrintResults.S], totals=EPrintTotals.YES)
        known = '*EL PRINT,ELSET=E1,TOTALS=YES\n'
        known +='S\n'
        self.assertEqual(str(ep), known)
        ep = ElPrint(self.eset,[EElPrintResults.S], totals=EPrintTotals.ONLY)
        known = '*EL PRINT,ELSET=E1,TOTALS=ONLY\n'
        known +='S\n'
        self.assertEqual(str(ep), known)

    def test_global_no(self):

        ep = ElPrint(self.eset,[EElPrintResults.S], global_=False)
        known = '*EL PRINT,ELSET=E1,GLOBAL=NO\n'
        known +='S\n'
        self.assertEqual(str(ep), known)

    def test_empty_entities(self):
        self.assertRaises(ValueError, ElPrint, self.eset, [])

    def test_time_points_and_frequency(self):
        tp = TimePoints('TP1', (1,2,3,4))
        self.assertRaises(ValueError, ElPrint, self.eset, [EElPrintResults.S], time_points=tp, frequency=2)

    def test_wrong_set_type(self):
        self.assertRaises(ValueError, ElPrint, self.nset, [EElPrintResults.S])