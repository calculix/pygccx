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

from pygccx.model_keywords import Equation
from pygccx.protocols import IKeyword

class TestEquation(TestCase):

    def test_is_IKeyword(self):
        e = Equation([(1,1,1)])
        self.assertTrue(isinstance(e, IKeyword))

    def test_happy_case(self):
        e = Equation([(3, 2, 2.3),
                      (28, 1, 4.05),
                      (17, 1, -8.22)])

        known = '*EQUATION\n'
        known += '3\n'
        known += '3,2,2.3000000e+00,\n'
        known += '28,1,4.0500000e+00,\n'
        known += '17,1,-8.2200000e+00\n'
        self.assertEqual(str(e), known)
