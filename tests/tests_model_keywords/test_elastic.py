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

from pygccx.model_keywords import Elastic
from pygccx.enums import EELasticTypes
from pygccx.protocols import IKeyword

class TestElastic(TestCase):

    def test_is_IKeyword(self):
        e = Elastic((210000., 0.3))
        self.assertTrue(isinstance(e, IKeyword))

    def test_iso(self):
        e = Elastic((210000., 0.3))
        known = '*ELASTIC,TYPE=ISO\n'
        known += '2.1000000e+05,3.0000000e-01,2.9400000e+02\n'
        self.assertEqual(str(e), known)

    def test_ortho(self):
        e = Elastic((500000.,157200.,400000.,157200.,
                     157200.,300000.,126200.,126200.,
                     126200.), EELasticTypes.ORTHO)
        known = '*ELASTIC,TYPE=ORTHO\n'
        known += '5.0000000e+05,1.5720000e+05,4.0000000e+05,1.5720000e+05,1.5720000e+05,3.0000000e+05,1.2620000e+05,1.2620000e+05,\n'
        known += '1.2620000e+05,2.9400000e+02\n'
        self.assertEqual(str(e), known)

    def test_aniso(self):
        e = Elastic((1,2,3,4,5,6,7,8,9,10,
                     11,12,13,14,15,16,17,18,19,20,21),
                     EELasticTypes.ANISO, )
        known = '*ELASTIC,TYPE=ANISO\n'
        known += '1.0000000e+00,2.0000000e+00,3.0000000e+00,4.0000000e+00,5.0000000e+00,6.0000000e+00,7.0000000e+00,8.0000000e+00,\n'
        known += '9.0000000e+00,1.0000000e+01,1.1000000e+01,1.2000000e+01,1.3000000e+01,1.4000000e+01,1.5000000e+01,1.6000000e+01,\n'
        known += '1.7000000e+01,1.8000000e+01,1.9000000e+01,2.0000000e+01,2.1000000e+01,2.9400000e+02\n'
        self.assertEqual(str(e), known)

    def test_ortho_two_temps(self):
        e = Elastic((500000.,157200.,400000.,157200.,
                     157200.,300000.,126200.,126200.,
                     126200.), EELasticTypes.ORTHO)
        e.add_elastic_params_for_temp(300.,
            500000.,157200.,400000.,157200.,
            157200.,300000.,126200.,126200.,
            126200.
        )
        known = '*ELASTIC,TYPE=ORTHO\n'
        known += '5.0000000e+05,1.5720000e+05,4.0000000e+05,1.5720000e+05,1.5720000e+05,3.0000000e+05,1.2620000e+05,1.2620000e+05,\n'
        known += '1.2620000e+05,2.9400000e+02\n'
        known += '5.0000000e+05,1.5720000e+05,4.0000000e+05,1.5720000e+05,1.5720000e+05,3.0000000e+05,1.2620000e+05,1.2620000e+05,\n'
        known += '1.2620000e+05,3.0000000e+02\n'
        self.assertEqual(str(e), known)

    def test_params_false_length(self):
        self.assertRaises(ValueError, Elastic, (500000.,157200.,400000.,157200.,
                                                157200.,300000.,126200.,126200.), EELasticTypes.ORTHO)
        # one param less than required

