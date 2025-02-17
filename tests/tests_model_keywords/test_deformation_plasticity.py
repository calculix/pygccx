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

from pygccx.model_keywords import DeformationPlasticity
from pygccx.enums import EELasticTypes
from pygccx.protocols import IKeyword

class TestDeformationPlasticity(TestCase):

    def test_is_IKeyword(self):
        d = DeformationPlasticity(210000., 0.3, 800, 12, 0.4)
        self.assertTrue(isinstance(d, IKeyword))

    def test_happy_case(self):
        d = DeformationPlasticity(210000., 0.3, 800, 12, 0.4)
        known = '*DEFORMATION PLASTICITY\n'
        known += '2.1000000e+05,3.0000000e-01,8.0000000e+02,1.2000000e+01,4.0000000e-01,2.9400000e+02\n'
        self.assertEqual(str(d), known)

    def test_add_params(self):
        d = DeformationPlasticity(210000., 0.3, 800, 12, 0.4)
        d.add_params_for_temp(220000, 0.3, 900, 13, 0.5, 400)
        known = '*DEFORMATION PLASTICITY\n'
        known += '2.1000000e+05,3.0000000e-01,8.0000000e+02,1.2000000e+01,4.0000000e-01,2.9400000e+02\n'
        known += '2.2000000e+05,3.0000000e-01,9.0000000e+02,1.3000000e+01,5.0000000e-01,4.0000000e+02\n'
        self.assertEqual(str(d), known)

    def test_exceptions(self):
        self.assertRaises(ValueError, DeformationPlasticity, 0, 0.3, 800, 12, 0.4)
        self.assertRaises(ValueError, DeformationPlasticity, -1, 0.3, 800, 12, 0.4)

        self.assertRaises(ValueError, DeformationPlasticity, 210000, -1, 800, 12, 0.4)
        self.assertRaises(ValueError, DeformationPlasticity, 210000, 0.5, 800, 12, 0.4)
        self.assertRaises(ValueError, DeformationPlasticity, 210000, 0.6, 800, 12, 0.4)

        self.assertRaises(ValueError, DeformationPlasticity, 210000, 0.3, 0, 12, 0.4)
        self.assertRaises(ValueError, DeformationPlasticity, 210000, 0.3, -1, 12, 0.4)

        self.assertRaises(ValueError, DeformationPlasticity, 210000, 0.3, 800, 1, 0.4)
        self.assertRaises(ValueError, DeformationPlasticity, 210000, 0.3, 800, 0.9, 0.4)

        self.assertRaises(ValueError, DeformationPlasticity, 210000, 0.3, 800, 12, 0)
        self.assertRaises(ValueError, DeformationPlasticity, 210000, 0.3, 800, 12, -1)