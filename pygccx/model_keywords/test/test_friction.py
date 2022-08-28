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

from pygccx.model_keywords import Friction
from pygccx.protocols import IKeyword

class TestFriction(TestCase):

    def test_is_IKeyword(self):
        f = Friction(0.3, 50000.)
        self.assertTrue(isinstance(f, IKeyword))

    def test_happy_case(self):
        f = Friction(0.3, 50000.)
        known = '*FRICTION\n'
        known += '3.0000000e-01,5.0000000e+04\n'
        self.assertEqual(str(f), known)

    def test_mue_lower_zero(self):
        self.assertRaises(ValueError, Friction, 0, 50000)
        self.assertRaises(ValueError, Friction, -1, 50000)

    def test_lam_lower_zero(self):
        self.assertRaises(ValueError, Friction, 0.3, 0)
        self.assertRaises(ValueError, Friction, 0.3, -1)
