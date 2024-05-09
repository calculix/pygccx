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

from pygccx.model_keywords import Creep
from pygccx.protocols import IKeyword

class TestCreep(TestCase):

    def test_is_IKeyword(self):
        c = Creep((1.E-10,5.,0.), temp=100)
        self.assertTrue(isinstance(c, IKeyword))

    def test_norton(self):
        e = Creep((1.E-10,5.,0.), temp=100)
        known = '*CREEP,LAW=NORTON\n'
        known += '1.0000000e-10,5.0000000e+00,0.0000000e+00,1.0000000e+02\n'
        self.assertEqual(str(e), known)


    def test_params_false_length(self):
        self.assertRaises(ValueError, Creep, (1,2,3,4))
        # one param less than required

