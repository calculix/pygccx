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

from pygccx.model_keywords import HyperElastic
from pygccx.enums import EHyperELasticTypes
from pygccx.protocols import IKeyword

class TestHyperElastic(TestCase):

    def test_is_IKeyword(self):
        e = HyperElastic((110., 12., 1e-3))
        self.assertTrue(isinstance(e, IKeyword))

    def test_arruda_boyce(self):
        e = HyperElastic((1,2,3), EHyperELasticTypes.ARRUDA_BOYCE)
        known = '*HYPERELASTIC,ARRUDA-BOYCE\n'
        known += '1.0000000e+00,2.0000000e+00,3.0000000e+00,2.9400000e+02\n'
        self.assertEqual(str(e), known)

        # must have exactly 3 params
        self.assertRaises(ValueError, HyperElastic, (1,2), EHyperELasticTypes.ARRUDA_BOYCE)
        self.assertRaises(ValueError, HyperElastic, (1,2,3,4), EHyperELasticTypes.ARRUDA_BOYCE)

    def test_mooney_rivlin(self):
        e = HyperElastic((1,2,3), EHyperELasticTypes.MOONEY_RIVLIN)
        known = '*HYPERELASTIC,MOONEY-RIVLIN\n'
        known += '1.0000000e+00,2.0000000e+00,3.0000000e+00,2.9400000e+02\n'
        self.assertEqual(str(e), known)

        # must have exactly 3 params
        self.assertRaises(ValueError, HyperElastic, (1,2), EHyperELasticTypes.MOONEY_RIVLIN)
        self.assertRaises(ValueError, HyperElastic, (1,2,3,4), EHyperELasticTypes.MOONEY_RIVLIN)

    def test_neo_hooke(self):
        e = HyperElastic((1,2), EHyperELasticTypes.NEO_HOOKE)
        known = '*HYPERELASTIC,NEO HOOKE\n'
        known += '1.0000000e+00,2.0000000e+00,2.9400000e+02\n'
        self.assertEqual(str(e), known)

        # must have exactly 2 params
        self.assertRaises(ValueError, HyperElastic, (1,), EHyperELasticTypes.NEO_HOOKE)
        self.assertRaises(ValueError, HyperElastic, (1,2,3), EHyperELasticTypes.NEO_HOOKE)

    def test_ogden_1(self):
        e = HyperElastic((1,2,3), EHyperELasticTypes.OGDEN_1)
        known = '*HYPERELASTIC,OGDEN,N=1\n'
        known += '1.0000000e+00,2.0000000e+00,3.0000000e+00,2.9400000e+02\n'
        self.assertEqual(str(e), known)

        # must have exactly 3 params
        self.assertRaises(ValueError, HyperElastic, (1,2), EHyperELasticTypes.OGDEN_1)
        self.assertRaises(ValueError, HyperElastic, (1,2,3,4), EHyperELasticTypes.OGDEN_1)

    def test_ogden_2(self):
        e = HyperElastic((1,2,3,4,5,6), EHyperELasticTypes.OGDEN_2)
        known = '*HYPERELASTIC,OGDEN,N=2\n'
        known += '1.0000000e+00,2.0000000e+00,3.0000000e+00,4.0000000e+00,5.0000000e+00,6.0000000e+00,2.9400000e+02\n'
        self.assertEqual(str(e), known)

        # must have exactly 6 params
        self.assertRaises(ValueError, HyperElastic, (1,2,3,4,5), EHyperELasticTypes.OGDEN_2)
        self.assertRaises(ValueError, HyperElastic, (1,2,3,4,5,6,7), EHyperELasticTypes.OGDEN_2)

    def test_ogden_3(self):
        e = HyperElastic((1,2,3,4,5,6,7,8,9), EHyperELasticTypes.OGDEN_3)
        known = '*HYPERELASTIC,OGDEN,N=3\n'
        known += '1.0000000e+00,2.0000000e+00,3.0000000e+00,4.0000000e+00,5.0000000e+00,6.0000000e+00,7.0000000e+00,8.0000000e+00,\n'
        known += '9.0000000e+00,2.9400000e+02\n'
        self.assertEqual(str(e), known)

        # must have exactly 9 params
        self.assertRaises(ValueError, HyperElastic, (1,2,3,4,5,6,7,8), EHyperELasticTypes.OGDEN_3)
        self.assertRaises(ValueError, HyperElastic, (1,2,3,4,5,6,7,8,9,20), EHyperELasticTypes.OGDEN_3)

    def test_poly_1(self):
        e = HyperElastic((1,2,3), EHyperELasticTypes.POLYNOMIAL_1)
        known = '*HYPERELASTIC,POLYNOMIAL,N=1\n'
        known += '1.0000000e+00,2.0000000e+00,3.0000000e+00,2.9400000e+02\n'
        self.assertEqual(str(e), known)

        # must have exactly 3 params
        self.assertRaises(ValueError, HyperElastic, (1,2), EHyperELasticTypes.POLYNOMIAL_1)
        self.assertRaises(ValueError, HyperElastic, (1,2,3,4), EHyperELasticTypes.POLYNOMIAL_1)

    def test_poly_2(self):
        e = HyperElastic((1,2,3,4,5,6,7), EHyperELasticTypes.POLYNOMIAL_2)
        known = '*HYPERELASTIC,POLYNOMIAL,N=2\n'
        known += '1.0000000e+00,2.0000000e+00,3.0000000e+00,4.0000000e+00,5.0000000e+00,6.0000000e+00,7.0000000e+00,2.9400000e+02\n'
        self.assertEqual(str(e), known)

        # must have exactly 7 params
        self.assertRaises(ValueError, HyperElastic, (1,2,3,4,5,6), EHyperELasticTypes.POLYNOMIAL_2)
        self.assertRaises(ValueError, HyperElastic, (1,2,3,4,5,6,7,8), EHyperELasticTypes.POLYNOMIAL_2)

    def test_poly_3(self):
        e = HyperElastic((1,2,3,4,5,6,7,8,9,10,11,12), EHyperELasticTypes.POLYNOMIAL_3)
        known = '*HYPERELASTIC,POLYNOMIAL,N=3\n'
        known += '1.0000000e+00,2.0000000e+00,3.0000000e+00,4.0000000e+00,5.0000000e+00,6.0000000e+00,7.0000000e+00,8.0000000e+00,\n'
        known += '9.0000000e+00,1.0000000e+01,1.1000000e+01,1.2000000e+01,2.9400000e+02\n'
        self.assertEqual(str(e), known)

        # must have exactly 12 params
        self.assertRaises(ValueError, HyperElastic, (1,2,3,4,5,6,7,8,9,10,11), EHyperELasticTypes.POLYNOMIAL_3)
        self.assertRaises(ValueError, HyperElastic, (1,2,3,4,5,6,7,8,9,10,11,12,13), EHyperELasticTypes.POLYNOMIAL_3)

    def test_red_poly_1(self):
        e = HyperElastic((1,2), EHyperELasticTypes.REDUCED_POLYNOMIAL_1)
        known = '*HYPERELASTIC,REDUCED POLYNOMIAL,N=1\n'
        known += '1.0000000e+00,2.0000000e+00,2.9400000e+02\n'
        self.assertEqual(str(e), known)

        # must have exactly 2 params
        self.assertRaises(ValueError, HyperElastic, (1,), EHyperELasticTypes.REDUCED_POLYNOMIAL_1)
        self.assertRaises(ValueError, HyperElastic, (1,2,3), EHyperELasticTypes.REDUCED_POLYNOMIAL_1)

    def test_red_poly_2(self):
        e = HyperElastic((1,2,3,4), EHyperELasticTypes.REDUCED_POLYNOMIAL_2)
        known = '*HYPERELASTIC,REDUCED POLYNOMIAL,N=2\n'
        known += '1.0000000e+00,2.0000000e+00,3.0000000e+00,4.0000000e+00,2.9400000e+02\n'
        self.assertEqual(str(e), known)

        # must have exactly 4 params
        self.assertRaises(ValueError, HyperElastic, (1,2,3), EHyperELasticTypes.REDUCED_POLYNOMIAL_2)
        self.assertRaises(ValueError, HyperElastic, (1,2,3,4,5), EHyperELasticTypes.REDUCED_POLYNOMIAL_2)

    def test_red_poly_3(self):
        e = HyperElastic((1,2,3,4,5,6), EHyperELasticTypes.REDUCED_POLYNOMIAL_3)
        known = '*HYPERELASTIC,REDUCED POLYNOMIAL,N=3\n'
        known += '1.0000000e+00,2.0000000e+00,3.0000000e+00,4.0000000e+00,5.0000000e+00,6.0000000e+00,2.9400000e+02\n'
        self.assertEqual(str(e), known)

        # must have exactly 4 params
        self.assertRaises(ValueError, HyperElastic, (1,2,3,4,5), EHyperELasticTypes.REDUCED_POLYNOMIAL_3)
        self.assertRaises(ValueError, HyperElastic, (1,2,3,4,5,6,7), EHyperELasticTypes.REDUCED_POLYNOMIAL_3)

    def test_yeoh(self):
        e = HyperElastic((1,2,3,4,5,6), EHyperELasticTypes.YEOH)
        known = '*HYPERELASTIC,YEOH\n'
        known += '1.0000000e+00,2.0000000e+00,3.0000000e+00,4.0000000e+00,5.0000000e+00,6.0000000e+00,2.9400000e+02\n'
        self.assertEqual(str(e), known)

        # must have exactly 4 params
        self.assertRaises(ValueError, HyperElastic, (1,2,3,4,5), EHyperELasticTypes.YEOH)
        self.assertRaises(ValueError, HyperElastic, (1,2,3,4,5,6,7), EHyperELasticTypes.YEOH)
