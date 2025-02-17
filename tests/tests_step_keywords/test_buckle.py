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

from pygccx.step_keywords import Buckle
from pygccx.enums import ESolvers
from pygccx.protocols import IKeyword

class TestBuckle(TestCase):

    def test_is_IKeyword(self):
        s = Buckle()
        self.assertTrue(isinstance(s, IKeyword))

    def test_default(self):
        s = Buckle()
        known = '*BUCKLE\n'
        known += '1\n'
        self.assertEqual(str(s), known)

    def test_solver(self):
        s = Buckle(solver=ESolvers.SPOOLES)
        known = '*BUCKLE,SOLVER=SPOOLES\n'
        known += '1\n'
        self.assertEqual(str(s), known)

        s = Buckle(solver=ESolvers.PASTIX)
        known = '*BUCKLE,SOLVER=PASTIX\n'
        known += '1\n'
        self.assertEqual(str(s), known)

        s = Buckle(solver=ESolvers.MATRIXSTORAGE)
        known = '*BUCKLE,SOLVER=MATRIXSTORAGE\n'
        known += '1\n'
        self.assertEqual(str(s), known)

        self.assertRaises(ValueError, Buckle, solver=ESolvers.ITERATIVE_SCALING)
        self.assertRaises(ValueError, Buckle, solver=ESolvers.ITERATIVE_CHOLESKY)

        err = ''
        try: Buckle(solver=ESolvers.ITERATIVE_SCALING)
        except ValueError as ve: err = str(ve)
        self.assertEqual(err, 'Solver ITERATIVE SCALING can not be used for a *BUCKLE step.')

        err = ''
        try: Buckle(solver=ESolvers.ITERATIVE_CHOLESKY)
        except ValueError as ve: err = str(ve)
        self.assertEqual(err, 'Solver ITERATIVE CHOLESKY can not be used for a *BUCKLE step.')

    def test_no_factors(self):
        s = Buckle(no_buckling_factors=10)
        known = '*BUCKLE\n'
        known += '10\n'
        self.assertEqual(str(s), known)

    def test_accuracy(self):
        s = Buckle(accuracy=0.05)
        known = '*BUCKLE\n'
        known += '1,5.0000000e-02\n'
        self.assertEqual(str(s), known)
        self.assertRaises(ValueError, Buckle, accuracy=0)  
        self.assertRaises(ValueError, Buckle, accuracy=-0.001)  

    def test_no_lanczos(self):
        s = Buckle(no_lanczos_vectors=10)
        known = '*BUCKLE\n'
        known += '1,,10\n'
        self.assertEqual(str(s), known)
        self.assertRaises(ValueError, Buckle, no_lanczos_vectors=0)  
        self.assertRaises(ValueError, Buckle, no_lanczos_vectors=-1)  

    def test_max_iters(self):
        s = Buckle(max_iterations=10)
        known = '*BUCKLE\n'
        known += '1,,,10\n'
        self.assertEqual(str(s), known)
        self.assertRaises(ValueError, Buckle, max_iterations=0)  
        self.assertRaises(ValueError, Buckle, max_iterations=-1)  


