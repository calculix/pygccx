'''
Copyright Matthias Sedlmaier 2024
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

from pygccx.model_keywords import Heading
from pygccx.protocols import IKeyword

class TestHeading(TestCase):

    def test_is_IKeyword(self):
        m = Heading('This is the model description')
        self.assertTrue(isinstance(m, IKeyword))

    def test_happy_case(self):
        h = Heading('This is the model description')

        known = '*HEADING\n'
        known += 'This is the model description\n'
        self.assertEqual(str(h), known)
