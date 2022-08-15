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
from step_keywords import ContactPrint, TimePoints
from enums import EContactPrintResults, ESurfTypes, EPrintTotals
from protocols import IKeyword

@dataclass()
class SurfaceMock:
    name:str
    type: ESurfTypes
    def write_ccx(self, buffer:list[str]): pass

class TestContactPrint(TestCase):

    def setUp(self) -> None:
        self.slave = SurfaceMock('S1', ESurfTypes.EL_FACE)
        self.master = SurfaceMock('M1', ESurfTypes.EL_FACE)


    def test_is_IKeyword(self):
        cp = ContactPrint([EContactPrintResults.CDIS, EContactPrintResults.CSTR])
        self.assertTrue(isinstance(cp, IKeyword))

    def test_default(self):

        cp = ContactPrint([EContactPrintResults.CDIS, EContactPrintResults.CSTR])
        known = '*CONTACT PRINT\n'
        known +='CDIS,CSTR\n'
        self.assertEqual(str(cp), known)

    def test_frequency(self):

        cp = ContactPrint([EContactPrintResults.CDIS, EContactPrintResults.CSTR], frequency=2)
        known = '*CONTACT PRINT,FREQUENCY=2\n'
        known +='CDIS,CSTR\n'
        self.assertEqual(str(cp), known)

    def test_time_points(self):
        tp = TimePoints('TP1', (1,2,3,4))
        cp = ContactPrint([EContactPrintResults.CDIS, EContactPrintResults.CSTR], time_points=tp)
        known = '*CONTACT PRINT,TIME POINTS=TP1\n'
        known +='CDIS,CSTR\n'
        self.assertEqual(str(cp), known)

    def test_totals(self):
        cp = ContactPrint([EContactPrintResults.CDIS, EContactPrintResults.CSTR], totals=EPrintTotals.YES)
        known = '*CONTACT PRINT,TOTALS=YES\n'
        known +='CDIS,CSTR\n'
        self.assertEqual(str(cp), known)
        cp = ContactPrint([EContactPrintResults.CDIS, EContactPrintResults.CSTR], totals=EPrintTotals.ONLY)
        known = '*CONTACT PRINT,TOTALS=ONLY\n'
        known +='CDIS,CSTR\n'
        self.assertEqual(str(cp), known)

    def test_slave_master(self):

        np = ContactPrint([EContactPrintResults.CDIS, EContactPrintResults.CSTR], slave=self.slave, master=self.master)
        known = '*CONTACT PRINT,SLAVE=S1,MASTER=M1\n'
        known +='CDIS,CSTR\n'
        self.assertEqual(str(np), known)

    def test_empty_entities(self):
        self.assertRaises(ValueError, ContactPrint, [])

    def test_time_points_and_frequency(self):
        tp = TimePoints('TP1', (1,2,3,4))
        self.assertRaises(ValueError, ContactPrint, [EContactPrintResults.CDIS], time_points=tp, frequency=2)

    def test_only_master(self):
        self.assertRaises(ValueError, ContactPrint, [EContactPrintResults.CDIS], master=self.master)

    def test_only_slave(self):
        self.assertRaises(ValueError, ContactPrint, [EContactPrintResults.CDIS], slave=self.slave)

    def test_no_master_or_self_when_required(self):
        self.assertRaises(ValueError, ContactPrint, [EContactPrintResults.CF])
