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
from helper_features import CoordinateSystem

import numpy as np

class TestCoordinateSystem(TestCase):

    def test_default(self):
        c = CoordinateSystem('C1')
        known_mat = np.array([[1,0,0],[0,1,0],[0,0,1]], dtype=float)
        known_ori = np.zeros(3)
        self.assertTrue(np.allclose(known_mat, c.get_matrix()))
        self.assertTrue(np.allclose(known_ori, c.get_origin()))

    def test_origin_param(self):
        # tests also set_origin(), because its called in __post_init__
        known_ori = np.array([2, 4, 6])
        c = CoordinateSystem('C1', origin=known_ori)
        self.assertTrue(np.allclose(known_ori, c.get_origin()))

    def test_origin_param_wrong_length(self):
        self.assertRaises(ValueError, CoordinateSystem, 'C1', origin=[2, 4, 6, 8])

    def test_matrix_param_wrong_length(self):
        self.assertRaises(ValueError, CoordinateSystem, 'C1', matrix=[[1,0,0],[0,1,0],[0,0,1],[0,0,0]])

    def test_matrix_param_not_all_rows_length_3(self):
        self.assertRaises(ValueError, CoordinateSystem, 'C1', matrix=[[1,0,0],[0,1,0],[0,0,1,0]])

    def test_matrix_param(self):
        # tests also set_matrix(), because its called in __post_init__
        known_mat = np.array([[0,1,0],[-1,0,0],[0,0,1]], dtype=float)
        c = CoordinateSystem('C1', matrix=known_mat)
        self.assertTrue(np.allclose(known_mat, c.get_matrix()))

    def test_move(self):
        c = CoordinateSystem('C1')
        c.move([1,2,3])
        self.assertTrue(np.allclose([1,2,3], c.get_origin()))
        c.move([1,2,3])
        self.assertTrue(np.allclose([2,4,6], c.get_origin()))

    def test_rotate(self):
        c = CoordinateSystem('C1')
        c.rotate_x(90, degrees=True)
        known_mat = np.array([[1, 0, 0],
                              [0, 0, 1],
                              [0, -1, 0]])
        self.assertTrue(np.allclose(known_mat, c.get_matrix()))

        c.rotate_y(90, degrees=True)
        known_mat = np.array([[0, 1, 0],
                              [0, 0, 1],
                              [1, 0, 0]])
        self.assertTrue(np.allclose(known_mat, c.get_matrix()))

        c.rotate_z(90, degrees=True)
        known_mat = np.array([[0, 0, 1],
                              [0, -1, 0],
                              [1, 0, 0]])
        self.assertTrue(np.allclose(known_mat, c.get_matrix()))


    # def test_is_IModelFeature(self):
    #     a = Amplitude('TestAmp', times = [0.,.1,.2,.3], amps=[0,1,-1,3])
    #     self.assertTrue(isinstance(a, IModelFeature))

    # def test_only_mandatory_params(self):
    #     a = Amplitude('TestAmp', times = [0.,.1,.2,.3], amps=[0,1,-1,3])
    #     known = '*AMPLITUDE,NAME=TestAmp\n'
    #     known += '  0.0000000e+00,  0.0000000e+00\n'
    #     known += '  1.0000000e-01,  1.0000000e+00\n'
    #     known += '  2.0000000e-01, -1.0000000e+00\n'
    #     known += '  3.0000000e-01,  3.0000000e+00\n'
    #     self.assertEqual(str(a), known)

    # def test_total_time(self):
    #     a = Amplitude('TestAmp', times = [0.,.1,.2,.3], amps=[0,1,-1,3], use_total_time=True)
    #     known = '*AMPLITUDE,NAME=TestAmp,TIME=TOTAL TIME\n'
    #     known += '  0.0000000e+00,  0.0000000e+00\n'
    #     known += '  1.0000000e-01,  1.0000000e+00\n'
    #     known += '  2.0000000e-01, -1.0000000e+00\n'
    #     known += '  3.0000000e-01,  3.0000000e+00\n'
    #     self.assertEqual(str(a), known)

    # def test_shift_x(self):
    #     a = Amplitude('TestAmp', times = [0.,.1,.2,.3], amps=[0,1,-1,3], shift_x=0.5)
    #     known = '*AMPLITUDE,NAME=TestAmp,SHIFTX=0.5\n'
    #     known += '  0.0000000e+00,  0.0000000e+00\n'
    #     known += '  1.0000000e-01,  1.0000000e+00\n'
    #     known += '  2.0000000e-01, -1.0000000e+00\n'
    #     known += '  3.0000000e-01,  3.0000000e+00\n'
    #     self.assertEqual(str(a), known)

    # def test_shift_y(self):
    #     a = Amplitude('TestAmp', times = [0.,.1,.2,.3], amps=[0,1,-1,3], shift_y=0.5)
    #     known = '*AMPLITUDE,NAME=TestAmp,SHIFTY=0.5\n'
    #     known += '  0.0000000e+00,  0.0000000e+00\n'
    #     known += '  1.0000000e-01,  1.0000000e+00\n'
    #     known += '  2.0000000e-01, -1.0000000e+00\n'
    #     known += '  3.0000000e-01,  3.0000000e+00\n'
    #     self.assertEqual(str(a), known)

    # def test_total_time_shift_x_shift_y(self):
    #     a = Amplitude('TestAmp', times = [0.,.1,.2,.3], amps=[0,1,-1,3], use_total_time=True, shift_x=0.25, shift_y=0.5)
    #     known = '*AMPLITUDE,NAME=TestAmp,TIME=TOTAL TIME,SHIFTX=0.25,SHIFTY=0.5\n'
    #     known += '  0.0000000e+00,  0.0000000e+00\n'
    #     known += '  1.0000000e-01,  1.0000000e+00\n'
    #     known += '  2.0000000e-01, -1.0000000e+00\n'
    #     known += '  3.0000000e-01,  3.0000000e+00\n'
    #     self.assertEqual(str(a), known)
