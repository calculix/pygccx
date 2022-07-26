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
from model_features import Material
from protocols import IModelFeature

class TestMaterial(TestCase):

    def test_is_IModelFeature(self):
        m = Material('Steel')
        self.assertTrue(isinstance(m, IModelFeature))

    def test_happy_case(self):
        m = Material('Steel')

        known = '*MATERIAL,NAME=Steel\n'
        self.assertEqual(str(m), known)

    def test_name_too_long(self):
        name = 'a' * 81
        self.assertRaises(ValueError, Material, name)