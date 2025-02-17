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

from pygccx.step_keywords import Frequency
from pygccx.enums import ESolvers
from pygccx.protocols import IKeyword

class TestFrequency(TestCase):

    def test_is_IKeyword(self):
        s = Frequency()
        self.assertTrue(isinstance(s, IKeyword))

    def test_default(self):
        s = Frequency()
        known = '*FREQUENCY\n'
        known += '1\n'
        self.assertEqual(str(s), known)

    def test_solver(self):
        s = Frequency(solver=ESolvers.SPOOLES)
        known = '*FREQUENCY,SOLVER=SPOOLES\n'
        known += '1\n'
        self.assertEqual(str(s), known)

        s = Frequency(solver=ESolvers.PASTIX)
        known = '*FREQUENCY,SOLVER=PASTIX\n'
        known += '1\n'
        self.assertEqual(str(s), known)

        s = Frequency(solver=ESolvers.MATRIXSTORAGE)
        known = '*FREQUENCY,SOLVER=MATRIXSTORAGE\n'
        known += '1\n'
        self.assertEqual(str(s), known)

        self.assertRaises(ValueError, Frequency, solver=ESolvers.ITERATIVE_SCALING)
        self.assertRaises(ValueError, Frequency, solver=ESolvers.ITERATIVE_CHOLESKY)

        err = ''
        try: Frequency(solver=ESolvers.ITERATIVE_SCALING)
        except ValueError as ve: err = str(ve)
        self.assertEqual(err, 'Solver ITERATIVE SCALING can not be used for a *FREQUENCY step.')

        err = ''
        try: Frequency(solver=ESolvers.ITERATIVE_CHOLESKY)
        except ValueError as ve: err = str(ve)
        self.assertEqual(err, 'Solver ITERATIVE CHOLESKY can not be used for a *FREQUENCY step.')

    def test_no_frequencies(self):
        s = Frequency(no_frequencies=10)
        known = '*FREQUENCY\n'
        known += '10\n'
        self.assertEqual(str(s), known)

        self.assertRaises(ValueError, Frequency, no_frequencies=-0)

    def test_lower_frequency_value(self):
        s = Frequency(lower_frequency_value=10)
        known = '*FREQUENCY\n'
        known += '1,1.0000000e+01\n'
        self.assertEqual(str(s), known)
        self.assertRaises(ValueError, Frequency, lower_frequency_value=-0.0001)

    def test_upper_frequency_value(self):
        s = Frequency(upper_frequency_value=10)
        known = '*FREQUENCY\n'
        known += '1,,1.0000000e+01\n'
        self.assertEqual(str(s), known)

        s = Frequency(lower_frequency_value=10, upper_frequency_value=100)
        known = '*FREQUENCY\n'
        known += '1,1.0000000e+01,1.0000000e+02\n'
        self.assertEqual(str(s), known)

        self.assertRaises(ValueError, Frequency, upper_frequency_value=-0.0001)
        self.assertRaises(ValueError, Frequency, lower_frequency_value=10, upper_frequency_value=10)
        self.assertRaises(ValueError, Frequency, lower_frequency_value=10, upper_frequency_value=-9.999)

    def test_alpha(self):
        s = Frequency(alpha=-0.1)
        known = '*FREQUENCY,ALPHA=-1.0000000e-01\n'
        known += '1\n'
        self.assertEqual(str(s), known)   
        self.assertRaises(ValueError, Frequency, alpha=0.0001)   
        self.assertRaises(ValueError, Frequency, alpha=-1/3-0.0001)   

    def test_storage(self):
        s = Frequency(storage=True)
        known = '*FREQUENCY,STORAGE=YES\n'
        known += '1\n'
        self.assertEqual(str(s), known)  

    def test_global(self):
        s = Frequency(global_=False)
        known = '*FREQUENCY,GLOBAL=NO\n'
        known += '1\n'
        self.assertEqual(str(s), known) 

    def test_cycmpc(self):
        s = Frequency(cycmpc=False)
        known = '*FREQUENCY,CYCMPC=INACTIVE\n'
        known += '1\n'
        self.assertEqual(str(s), known) 

    def test_min_time_step(self):
        s = Frequency(min_time_step=0.001)
        known = '*FREQUENCY\n'
        known += '1,,,1.0000000e-03\n'
        self.assertEqual(str(s), known) 
        self.assertRaises(ValueError, Frequency, min_time_step=0)  
        self.assertRaises(ValueError, Frequency, min_time_step=-0.001)  
 