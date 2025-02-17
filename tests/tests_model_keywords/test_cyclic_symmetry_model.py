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
from dataclasses import dataclass

from pygccx.model_keywords import CyclicSymmetryModel
from pygccx.enums import EOrientationSystems
from pygccx.protocols import IKeyword

import numpy as np

@dataclass
class CoordinateSystemMock:
    name:str
    type:EOrientationSystems

    def get_origin(self):
        return np.array([1,2,3])

    def get_matrix(self):
        return np.array([[0, 0, 1],
                        [0, -1, 0],
                        [1, 0, 0]])
    
@dataclass
class TieMock:
    name:str = 'Test Tie'
    cyclic_symmetry:bool = True

class TestCyclicSymmetryModel(TestCase):

    def test_is_IKeyword(self):
        c = CyclicSymmetryModel(3, TieMock(), (0,0,1), (1,0,0))
        self.assertTrue(isinstance(c, IKeyword))

    def test_w_check(self): 
        c = CyclicSymmetryModel(3, TieMock(), (0,0,1), (1,0,0))
        known = '*CYCLIC SYMMETRY MODEL,N=3,TIE=Test Tie\n'
        known += '0.0000000e+00,0.0000000e+00,1.0000000e+00,1.0000000e+00,0.0000000e+00,0.0000000e+00\n'
        self.assertEqual(str(c), known)

    def test_wo_check(self): 
        c = CyclicSymmetryModel(3, TieMock(), (0,0,1), (1,0,0), check=False)
        known = '*CYCLIC SYMMETRY MODEL,N=3,TIE=Test Tie,CHECK=NO\n'
        known += '0.0000000e+00,0.0000000e+00,1.0000000e+00,1.0000000e+00,0.0000000e+00,0.0000000e+00\n'
        self.assertEqual(str(c), known)

    def test_pnt_a_false_length(self):
        tie = TieMock()
        self.assertRaises(ValueError, CyclicSymmetryModel, 3, tie, (0,1), (1,0,0))

    def test_pnt_b_false_length(self):
        tie = TieMock()
        self.assertRaises(ValueError, CyclicSymmetryModel, 3, tie, (0,0,1), (1,0))

    def test_tie_not_cylindrical(self):
        tie = TieMock(cyclic_symmetry=False)
        self.assertRaises(ValueError, CyclicSymmetryModel, 3, tie, (0,0,1), (1,0,0))

    def test_n_lower_1(self):
        tie = TieMock()
        self.assertRaises(ValueError, CyclicSymmetryModel, 0, tie, (0,0,1), (1,0,0))
        self.assertRaises(ValueError, CyclicSymmetryModel, -1, tie, (0,0,1), (1,0,0))

    def test_from_coordinate_system_cylindrical(self):
        cs = CoordinateSystemMock('C1', EOrientationSystems.CYLINDRICAL)
        c = CyclicSymmetryModel.from_coordinate_system(3, TieMock(), cs)
        known = '*CYCLIC SYMMETRY MODEL,N=3,TIE=Test Tie\n'
        known += '1.0000000e+00,2.0000000e+00,3.0000000e+00,2.0000000e+00,2.0000000e+00,3.0000000e+00\n'
        self.assertEqual(str(c), known)

        c = CyclicSymmetryModel.from_coordinate_system(3, TieMock(), cs, False)
        known = '*CYCLIC SYMMETRY MODEL,N=3,TIE=Test Tie,CHECK=NO\n'
        known += '1.0000000e+00,2.0000000e+00,3.0000000e+00,2.0000000e+00,2.0000000e+00,3.0000000e+00\n'
        self.assertEqual(str(c), known)

    def test_from_coordinate_system_rectangular(self):
        cs = CoordinateSystemMock('C1', EOrientationSystems.RECTANGULAR)
        self.assertRaises(ValueError, CyclicSymmetryModel.from_coordinate_system, 3, TieMock(), cs)

    