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
from step_keywords import ContactFile, TimePoints
from enums import EContactResults
from protocols import IKeyword

class TestContactFile(TestCase):

    def test_is_IKeyword(self):
        cf = ContactFile([EContactResults.CDIS, EContactResults.CELS])
        self.assertTrue(isinstance(cf, IKeyword))

    def test_default(self):

        cf = ContactFile([EContactResults.CDIS, EContactResults.CELS])
        known = '*CONTACT FILE\n'
        known +='CDIS,CELS\n'
        self.assertEqual(str(cf), known)

    def test_frequency(self):

        cf = ContactFile([EContactResults.CDIS, EContactResults.CELS], frequency=2)
        known = '*CONTACT FILE,FREQUENCY=2\n'
        known +='CDIS,CELS\n'
        self.assertEqual(str(cf), known)

    def test_time_points(self):
        tp = TimePoints('TP1', (1,2,3,4))
        cf = ContactFile([EContactResults.CDIS, EContactResults.CELS], time_points=tp)
        known = '*CONTACT FILE,TIME POINTS=TP1\n'
        known +='CDIS,CELS\n'
        self.assertEqual(str(cf), known)

    def test_last_iteration(self):

        cf = ContactFile([EContactResults.CDIS, EContactResults.CELS], last_Iterations=True)
        known = '*CONTACT FILE,LAST ITERATIONS\n'
        known +='CDIS,CELS\n'
        self.assertEqual(str(cf), known)

    def test_contact_elements(self):

        cf = ContactFile([EContactResults.CDIS, EContactResults.CELS], contact_elements=True)
        known = '*CONTACT FILE,CONTACT ELEMENTS\n'
        known +='CDIS,CELS\n'
        self.assertEqual(str(cf), known)

    def test_empty_entities(self):
        self.assertRaises(ValueError, ContactFile, [])

    def test_time_points_and_frequency(self):
        tp = TimePoints('TP1', (1,2,3,4))
        self.assertRaises(ValueError, ContactFile, [EContactResults.CDIS], time_points=tp, frequency=2)
