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
from step_features import NodeFile, TimePoints
from enums import ENodeResults, EResultOutputs

class TestNodeFile(TestCase):

    def test_default(self):

        nf = NodeFile([ENodeResults.U, ENodeResults.RF])
        known = '*NODE FILE\n'
        known +='U,RF\n'
        self.assertEqual(str(nf), known)

    def test_frequency(self):

        nf = NodeFile([ENodeResults.U, ENodeResults.RF], frequency=2)
        known = '*NODE FILE,FREQUENCY=2\n'
        known +='U,RF\n'
        self.assertEqual(str(nf), known)

    def test_time_points(self):
        tp = TimePoints('TP1', (1,2,3,4))
        nf = NodeFile([ENodeResults.U, ENodeResults.RF], time_points=tp)
        known = '*NODE FILE,TIME POINTS=TP1\n'
        known +='U,RF\n'
        self.assertEqual(str(nf), known)

    def test_last_iteration(self):

        nf = NodeFile([ENodeResults.U, ENodeResults.RF], last_Iterations=True)
        known = '*NODE FILE,LAST ITERATIONS\n'
        known +='U,RF\n'
        self.assertEqual(str(nf), known)

    def test_contact_elements(self):

        nf = NodeFile([ENodeResults.U, ENodeResults.RF], contact_elements=True)
        known = '*NODE FILE,CONTACT ELEMENTS\n'
        known +='U,RF\n'
        self.assertEqual(str(nf), known)

    def test_global_no(self):

        nf = NodeFile([ENodeResults.U, ENodeResults.RF], global_=False)
        known = '*NODE FILE,GLOBAL=NO\n'
        known +='U,RF\n'
        self.assertEqual(str(nf), known)

    def test_output_all(self):

        nf = NodeFile([ENodeResults.U, ENodeResults.RF], output_all=True)
        known = '*NODE FILE,OUTPUT ALL\n'
        known +='U,RF\n'
        self.assertEqual(str(nf), known)

    def test_output_2D(self):

        nf = NodeFile([ENodeResults.U, ENodeResults.RF], output=EResultOutputs._2D)
        known = '*NODE FILE,OUTPUT=2D\n'
        known +='U,RF\n'
        self.assertEqual(str(nf), known)

    def test_empty_entities(self):
        self.assertRaises(ValueError, NodeFile, [])

    def test_time_points_and_frequency(self):
        tp = TimePoints('TP1', (1,2,3,4))
        self.assertRaises(ValueError, NodeFile, [ENodeResults.U], time_points=tp, frequency=2)
