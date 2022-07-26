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
from model_features import SurfaceInteraction
from protocols import IModelFeature

class TestSurfaceInteraction(TestCase):

    def test_is_IModelFeature(self):
        si = SurfaceInteraction('SI1')
        self.assertTrue(isinstance(si, IModelFeature))

    def test_happy_case(self):
        si = SurfaceInteraction('SI1')
        known = '*SURFACE INTERACTION,NAME=SI1\n'
        self.assertEqual(str(si), known)

    def test_name_too_long(self):
        name = 'a' * 81
        self.assertRaises(ValueError, SurfaceInteraction, name)
