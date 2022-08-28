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

from pygccx.step_keywords import Static
from pygccx.enums import ESolvers
from pygccx.protocols import IKeyword

class TestStatic(TestCase):

    def test_is_IKeyword(self):
        s = Static()
        self.assertTrue(isinstance(s, IKeyword))

    def test_default(self):
        s = Static()
        known = '*STATIC\n'
        known += '1.0000000e+00,1.0000000e+00\n'
        self.assertEqual(str(s), known)

    def test_solver(self):
        s = Static(solver=ESolvers.SPOOLES)
        known = '*STATIC,SOLVER=SPOOLES\n'
        known += '1.0000000e+00,1.0000000e+00\n'
        self.assertEqual(str(s), known)

        s = Static(solver=ESolvers.ITERATIVE_SCALING)
        known = '*STATIC,SOLVER=ITERATIVE SCALING\n'
        known += '1.0000000e+00,1.0000000e+00\n'
        self.assertEqual(str(s), known)

        s = Static(solver=ESolvers.ITERATIVE_CHOLESKY)
        known = '*STATIC,SOLVER=ITERATIVE CHOLESKY\n'
        known += '1.0000000e+00,1.0000000e+00\n'
        self.assertEqual(str(s), known)

        s = Static(solver=ESolvers.PASTIX)
        known = '*STATIC,SOLVER=PASTIX\n'
        known += '1.0000000e+00,1.0000000e+00\n'
        self.assertEqual(str(s), known)

    def test_direct(self):
        s = Static(direct=True)
        known = '*STATIC,DIRECT\n'
        known += '1.0000000e+00,1.0000000e+00\n'
        self.assertEqual(str(s), known)

    def test_time_reset(self):
        s = Static(time_reset=True)
        known = '*STATIC,TIME RESET\n'
        known += '1.0000000e+00,1.0000000e+00\n'
        self.assertEqual(str(s), known)

    def test_time_at_start(self):
        s = Static(total_time_at_start=2.2)
        known = '*STATIC,TOTAL TIME AT START=2.2000000e+00\n'
        known += '1.0000000e+00,1.0000000e+00\n'
        self.assertEqual(str(s), known)

    def test_time_period(self):
        s = Static(time_period=2.2)
        known = '*STATIC\n'
        known += '1.0000000e+00,2.2000000e+00\n'
        self.assertEqual(str(s), known)

    def test_time_inc(self):
        s = Static(init_time_inc=0.3, time_period=2.0, min_time_inc=0.02, max_time_inc=0.5)
        known = '*STATIC\n'
        known += '3.0000000e-01,2.0000000e+00,2.0000000e-02,5.0000000e-01\n'
        self.assertEqual(str(s), known)

    def test_time_inc_wo_min_time_inc(self):
        s = Static(init_time_inc=0.3, time_period=2.0, max_time_inc=0.5)
        known = '*STATIC\n'
        known += '3.0000000e-01,2.0000000e+00,,5.0000000e-01\n'
        self.assertEqual(str(s), known)

    def test_time_inc_wo_max_time_inc(self):
        s = Static(init_time_inc=0.3, time_period=2.0, min_time_inc=0.02)
        known = '*STATIC\n'
        known += '3.0000000e-01,2.0000000e+00,2.0000000e-02\n'
        self.assertEqual(str(s), known)
