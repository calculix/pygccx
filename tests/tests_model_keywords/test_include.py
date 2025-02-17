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

from pygccx.model_keywords import Include
from pygccx.protocols import IKeyword

class TestInclude(TestCase):

    def test_is_IKeyword(self):
        i = Include('testfile')
        self.assertTrue(isinstance(i, IKeyword))

    def test_happy_case(self):
        i = Include('testfile')

        known = '*INCLUDE,INPUT="testfile"\n'
        self.assertEqual(str(i), known)