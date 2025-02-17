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

from pygccx.step_keywords import Visco
from pygccx.enums import ESolvers
from pygccx.protocols import IKeyword

class TestVisco(TestCase):

    def test_is_IKeyword(self):
        s = Visco(8.e-4)
        self.assertTrue(isinstance(s, IKeyword))

    def test_default(self):
        s = Visco(8.e-4)
        known = '*VISCO,CETOL=8.0000000e-04\n'
        known += '1.0000000e+00,1.0000000e+00\n'
        self.assertEqual(str(s), known)

    def test_solver(self):
        s = Visco(8.e-4, solver=ESolvers.SPOOLES)
        known = '*VISCO,CETOL=8.0000000e-04,SOLVER=SPOOLES\n'
        known += '1.0000000e+00,1.0000000e+00\n'
        self.assertEqual(str(s), known)

        s = Visco(8.e-4, solver=ESolvers.ITERATIVE_SCALING)
        known = '*VISCO,CETOL=8.0000000e-04,SOLVER=ITERATIVE SCALING\n'
        known += '1.0000000e+00,1.0000000e+00\n'
        self.assertEqual(str(s), known)

        s = Visco(8.e-4, solver=ESolvers.ITERATIVE_CHOLESKY)
        known = '*VISCO,CETOL=8.0000000e-04,SOLVER=ITERATIVE CHOLESKY\n'
        known += '1.0000000e+00,1.0000000e+00\n'
        self.assertEqual(str(s), known)

        s = Visco(8.e-4, solver=ESolvers.PASTIX)
        known = '*VISCO,CETOL=8.0000000e-04,SOLVER=PASTIX\n'
        known += '1.0000000e+00,1.0000000e+00\n'
        self.assertEqual(str(s), known)

        self.assertRaises(ValueError, Visco, 8.e-4, solver=ESolvers.MATRIXSTORAGE)

        err = ''
        try: Visco(8.e-4, solver=ESolvers.MATRIXSTORAGE)
        except ValueError as ve: err = str(ve)
        self.assertEqual(err, 'Solver MATRIXSTORAGE can not be used for a *VISCO step.')


    def test_direct(self):
        s = Visco(8.e-4, direct=True)
        known = '*VISCO,CETOL=8.0000000e-04,DIRECT\n'
        known += '1.0000000e+00,1.0000000e+00\n'
        self.assertEqual(str(s), known)

    def test_time_reset(self):
        s = Visco(8.e-4, time_reset=True)
        known = '*VISCO,CETOL=8.0000000e-04,TIME RESET\n'
        known += '1.0000000e+00,1.0000000e+00\n'
        self.assertEqual(str(s), known)

    def test_time_at_start(self):
        s = Visco(8.e-4, total_time_at_start=2.2)
        known = '*VISCO,CETOL=8.0000000e-04,TOTAL TIME AT START=2.2000000e+00\n'
        known += '1.0000000e+00,1.0000000e+00\n'
        self.assertEqual(str(s), known)

    def test_time_period(self):
        s = Visco(8.e-4, time_period=2.2)
        known = '*VISCO,CETOL=8.0000000e-04\n'
        known += '1.0000000e+00,2.2000000e+00\n'
        self.assertEqual(str(s), known)

    def test_time_inc(self):
        s = Visco(8.e-4, init_time_inc=0.3, time_period=2.0, min_time_inc=0.02, max_time_inc=0.5)
        known = '*VISCO,CETOL=8.0000000e-04\n'
        known += '3.0000000e-01,2.0000000e+00,2.0000000e-02,5.0000000e-01\n'
        self.assertEqual(str(s), known)

    def test_time_inc_wo_min_time_inc(self):
        s = Visco(8.e-4, init_time_inc=0.3, time_period=2.0, max_time_inc=0.5)
        known = '*VISCO,CETOL=8.0000000e-04\n'
        known += '3.0000000e-01,2.0000000e+00,,5.0000000e-01\n'
        self.assertEqual(str(s), known)

    def test_time_inc_wo_max_time_inc(self):
        s = Visco(8.e-4, init_time_inc=0.3, time_period=2.0, min_time_inc=0.02)
        known = '*VISCO,CETOL=8.0000000e-04\n'
        known += '3.0000000e-01,2.0000000e+00,2.0000000e-02\n'
        self.assertEqual(str(s), known)
