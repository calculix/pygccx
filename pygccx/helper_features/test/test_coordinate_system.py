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

from pygccx.helper_features import CoordinateSystem
from pygccx.enums import EOrientationSystems
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

    def test_transform_point_from_global_exception(self):
        c = CoordinateSystem('C1')

        self.assertRaises(ValueError, c.transform_point_from_global, [0.])
        self.assertRaises(ValueError, c.transform_point_from_global, [0., 0.])
        self.assertRaises(ValueError, c.transform_point_from_global, [0., 0., 0., 0.])
        self.assertRaises(ValueError, c.transform_point_from_global, [[0., 0., 0.]])

    def test_transform_point_from_global_into_rectangular(self):

        # Test coincident cosy
        # ------------------------------------------------------------------
        # outpu must be input, because local and global system are coincident.
        c = CoordinateSystem('C1')

        # test one point
        glob_pnt = np.array([-6,4,7], dtype=float)
        loc_pnt = c.transform_point_from_global(glob_pnt)
        self.assertTrue(np.allclose(glob_pnt, loc_pnt))

        # Test translated and rotated Cosy
        # ------------------------------------------------------------------
        c.move([1., 2., -4.])
        c.rotate_x(10, degrees=True)
        c.rotate_y(20, degrees=True)
        c.rotate_z(30, degrees=True)
        glob_pnts = [[0,0,0],
                     [1,1,1],
                     [1,2,3],
                     [-6,4,7]]
        loc_pnts = [c.transform_point_from_global(glob_pnt) for glob_pnt in glob_pnts]
        loc_pnts_ref = [[-2.7209705, 9.8683531e-002, 3.685998],
                        [-1.5682088, 0.77080594, 4.7902588],
                        [-1.4341189, 2.2315704, 6.477916],
                        [-6.8625229, 8.4420236, 7.4590895]] 
                    # calculated with ANSYS Workbench Mechanical
        
        for p1, p2 in zip(loc_pnts, loc_pnts_ref):
            for c1, c2 in zip(p1, p2):
                self.assertAlmostEqual(c1, c2, 7)

    def test_transform_point_from_global_into_cylindrical(self):

        c = CoordinateSystem('C1', type=EOrientationSystems.CYLINDRICAL)

        # test one point
        glob_pnt = np.array([-6,4,7], dtype=float)
        loc_pnt = c.transform_point_from_global(glob_pnt)
        loc_pnt_ref = np.array([7.2111026, np.deg2rad(146.30993), 7.])
                      # calculated with ANSYS Workbench Mechanical

        for c1, c2 in zip(loc_pnt, loc_pnt_ref):
            self.assertAlmostEqual(c1, c2, 7) #type: ignore

        # test multiple points
        glob_pnts = [[0,0,0],
                    [1,1,1],
                    [1,2,3],
                    [-6,4,7]]
        
        loc_pnts = [c.transform_point_from_global(glob_pnt) for glob_pnt in glob_pnts]

        loc_pnts_ref =[[0.,	0.,	0.],
                        [1.4142136,	np.deg2rad(45.),	1.],
                        [2.236068,	np.deg2rad(63.434949),	3.],
                        [7.2111026,	np.deg2rad(146.30993),	7.]]
                    # calculated with ANSYS Workbench Mechanical
        for p1, p2 in zip(loc_pnts, loc_pnts_ref):
            for c1, c2 in zip(p1, p2):
                self.assertAlmostEqual(c1, c2, 6)

        # Test translated and rotated Cosy
        # ------------------------------------------------------------------
        c.move([1., 2., -4.])
        c.rotate_x(10, degrees=True)
        c.rotate_y(20, degrees=True)
        c.rotate_z(30, degrees=True)
        loc_pnts = [c.transform_point_from_global(glob_pnt) for glob_pnt in glob_pnts]
        
        loc_pnts_ref =[[2.7227594,	np.deg2rad(177.92292),	3.685998],
                        [1.747404,	np.deg2rad(153.82496),	4.7902588],
                        [2.6526597,	np.deg2rad(122.72683),	6.477916],
                        [10.879429,	np.deg2rad(129.10767),	7.4590895]]
                       # calculated with ANSYS Workbench Mechanical

        for p1, p2 in zip(loc_pnts, loc_pnts_ref):
            for c1, c2 in zip(p1, p2):
                self.assertAlmostEqual(c1, c2, 6)

    def test_transform_point_to_global_exception(self):
        c = CoordinateSystem('C1')

        self.assertRaises(ValueError, c.transform_point_to_global, [0.])
        self.assertRaises(ValueError, c.transform_point_to_global, [0., 0.])
        self.assertRaises(ValueError, c.transform_point_to_global, [0., 0., 0., 0.])
        self.assertRaises(ValueError, c.transform_point_to_global, [[0., 0., 0.]])

    def test_transform_point_to_global_from_rectangular(self):

        c = CoordinateSystem('C1')

        # test one point
        loc_pnt = np.array([-6,4,7], dtype=float)
        glob_pnt = c.transform_point_to_global(loc_pnt)
        self.assertTrue(np.allclose(glob_pnt, loc_pnt))

        # test multiple points
        loc_pnts = [[-2.7209705, 9.8683531e-2, 3.685998],
                    [-1.5682088, 0.77080594,   4.7902588],
                    [-1.4341189, 2.23157040,   6.477916],
                    [-6.8625229, 8.44202360,   7.4590895]]
                    # calculated with ANSYS Workbench Mechanical
        
        glob_pnts = [c.transform_point_to_global(loc_pnt) for loc_pnt in loc_pnts]

        self.assertTrue(np.allclose(glob_pnts, loc_pnts))

        # Test translated and rotated Cosy
        # ------------------------------------------------------------------
        c.move([1., 2., -4.])
        c.rotate_x(10, degrees=True)
        c.rotate_y(20, degrees=True)
        c.rotate_z(30, degrees=True)
        glob_pnts = [c.transform_point_to_global(loc_pnt) for loc_pnt in loc_pnts]
        glob_pnts_ref = [[ 0., 0., 0.],
                        [ 1., 1., 1.],
                        [ 1., 2., 3.],
                        [-6., 4., 7.]] 
                    # calculated with ANSYS Workbench Mechanical
        
        for p1, p2 in zip(glob_pnts, glob_pnts_ref):
            for c1, c2 in zip(p1, p2):
                self.assertAlmostEqual(c1, c2, 6)

    def test_transform_point_to_global_from_cylindrical(self):

        c = CoordinateSystem('C1', type=EOrientationSystems.CYLINDRICAL)

        # test one point
        loc_pnt = [7.2111026, np.deg2rad(146.30993), 7.]
        # calculated with ANSYS Workbench Mechanical

        glob_pnt = c.transform_point_to_global(loc_pnt)
        glob_pnt_ref = np.array([-6,4,7], dtype=float)
                      
        for c1, c2 in zip(glob_pnt, glob_pnt_ref):
            self.assertAlmostEqual(c1, c2, 6) #type: ignore

        # test multiple points
        loc_pnts = [[0.,	0.,	0.],
                    [1.4142136,	np.deg2rad(45.),	1.],
                    [2.236068,	np.deg2rad(63.434949),	3.],
                    [7.2111026,	np.deg2rad(146.30993),	7.]]
                    # calculated with ANSYS Workbench Mechanical
        
        glob_pnts = [c.transform_point_to_global(loc_pnt) for loc_pnt in loc_pnts]

        glob_pnts_ref = [[ 0., 0., 0.],
                        [ 1., 1., 1.],
                        [ 1., 2., 3.],
                        [-6., 4., 7.]]

        for p1, p2 in zip(glob_pnts, glob_pnts_ref):
            for c1, c2 in zip(p1, p2):
                self.assertAlmostEqual(c1, c2, 6)

        # Test translated and rotated Cosy
        # ------------------------------------------------------------------
        c.move([1., 2., -4.])
        c.rotate_x(10, degrees=True)
        c.rotate_y(20, degrees=True)
        c.rotate_z(30, degrees=True)

        loc_pnts = [[2.7227594,	np.deg2rad(177.92292),	3.685998],
                    [1.747404,	np.deg2rad(153.82496),	4.7902588],
                    [2.6526597,	np.deg2rad(122.72683),	6.477916],
                    [10.879429,	np.deg2rad(129.10767),	7.4590895]] 
                    # calculated with ANSYS Workbench Mechanical
        
        glob_pnts = [c.transform_point_to_global(loc_pnt) for loc_pnt in loc_pnts]

        for p1, p2 in zip(glob_pnts, glob_pnts_ref):
            for c1, c2 in zip(p1, p2):
                self.assertAlmostEqual(c1, c2, 6)

    def test_transform_point_to_other_from_rectangular_to_rectangular(self):

        c1 = CoordinateSystem('C1')
        c1.move([1., 2., -4.])
        c1.rotate_x(10, degrees=True)
        c1.rotate_y(20, degrees=True)
        c1.rotate_z(30, degrees=True)

        c2 = CoordinateSystem('C2')
        c2.move([8., -3., 5.])
        c2.rotate_x(30, degrees=True)
        c2.rotate_y(40, degrees=True)
        c2.rotate_z(50, degrees=True)

        c1_pnts = [[-2.7209705, 9.8683531e-2, 3.685998],
                    [-1.5682088, 0.77080594,   4.7902588],
                    [-1.4341189, 2.23157040,   6.477916],
                    [-6.8625229, 8.44202360,   7.4590895]]
                    # calculated with ANSYS Workbench Mechanical

        c2_pnts_ref =  [[-1.4552322,    1.8868577, -9.6084373],
                        [-6.7625066e-2, 2.3583302, -8.6852579],
                        [ 0.85277961,   4.1644548, -7.7414523],
                        [-0.75323817,  11.884473, -10.353354]]
                    # calculated with ANSYS Workbench Mechanical

        c2_pnts = [c1.transform_point_to_other(c1_pnt, c2) for c1_pnt in c1_pnts]
        
        for p1, p2 in zip(c2_pnts, c2_pnts_ref):
            for c1, c2 in zip(p1, p2):
                self.assertAlmostEqual(c1, c2, 6)

    def test_transform_point_to_other_from_rectangular_to_cylindrical(self):

        c1 = CoordinateSystem('C1')
        c1.move([1., 2., -4.])
        c1.rotate_x(10, degrees=True)
        c1.rotate_y(20, degrees=True)
        c1.rotate_z(30, degrees=True)

        c2 = CoordinateSystem('C2', type=EOrientationSystems.CYLINDRICAL)
        c2.move([8., -3., 5.])
        c2.rotate_x(30, degrees=True)
        c2.rotate_y(40, degrees=True)
        c2.rotate_z(50, degrees=True)

        c1_pnts = [[-2.7209705, 9.8683531e-2, 3.685998],
                    [-1.5682088, 0.77080594,   4.7902588],
                    [-1.4341189, 2.23157040,   6.477916],
                    [-6.8625229, 8.44202360,   7.4590895]]
                    # calculated with ANSYS Workbench Mechanical

        c2_pnts_ref = [[2.3828414,	np.deg2rad(127.64108),	-9.6084373],
                        [2.3592996,	np.deg2rad(91.642505),	-8.6852579],
                        [4.2508725,	np.deg2rad(78.427201),	-7.7414523],
                        [11.908319,	np.deg2rad(93.626557),	-10.353354]]
                    # calculated with ANSYS Workbench Mechanical

        c2_pnts = [c1.transform_point_to_other(c1_pnt, c2) for c1_pnt in c1_pnts]
        
        for p1, p2 in zip(c2_pnts, c2_pnts_ref):
            for c1, c2 in zip(p1, p2):
                self.assertAlmostEqual(c1, c2, 6)

    def test_transform_point_to_other_from_cylindrical_to_rectangular(self):

        c1 = CoordinateSystem('C1', type=EOrientationSystems.CYLINDRICAL)
        c1.move([1., 2., -4.])
        c1.rotate_x(10, degrees=True)
        c1.rotate_y(20, degrees=True)
        c1.rotate_z(30, degrees=True)

        c2 = CoordinateSystem('C2')
        c2.move([8., -3., 5.])
        c2.rotate_x(30, degrees=True)
        c2.rotate_y(40, degrees=True)
        c2.rotate_z(50, degrees=True)

        c1_pnts = [[2.7227594,	np.deg2rad(177.92292),	3.685998],
                    [1.747404, np.deg2rad(153.82496),	4.7902588],
                    [2.6526597,	np.deg2rad(122.72683),	6.477916],
                    [10.879429,	np.deg2rad(129.10767),	7.4590895]]
                    # calculated with ANSYS Workbench Mechanical

        c2_pnts_ref =  [[-1.4552322,    1.8868577, -9.6084373],
                        [-6.7625066e-2, 2.3583302, -8.6852579],
                        [ 0.85277961,   4.1644548, -7.7414523],
                        [-0.75323817,  11.884473, -10.353354]]
                    # calculated with ANSYS Workbench Mechanical

        c2_pnts = [c1.transform_point_to_other(c1_pnt, c2) for c1_pnt in c1_pnts]
        
        for p1, p2 in zip(c2_pnts, c2_pnts_ref):
            for c1, c2 in zip(p1, p2):
                self.assertAlmostEqual(c1, c2, 5)

    def test_transform_point_to_other_from_cylindrical_to_cylindrical(self):

        c1 = CoordinateSystem('C1', type=EOrientationSystems.CYLINDRICAL)
        c1.move([1., 2., -4.])
        c1.rotate_x(10, degrees=True)
        c1.rotate_y(20, degrees=True)
        c1.rotate_z(30, degrees=True)

        c2 = CoordinateSystem('C2', type=EOrientationSystems.CYLINDRICAL)
        c2.move([8., -3., 5.])
        c2.rotate_x(30, degrees=True)
        c2.rotate_y(40, degrees=True)
        c2.rotate_z(50, degrees=True)

        c1_pnts = [[2.7227594,	np.deg2rad(177.92292),	3.685998],
                    [1.747404, np.deg2rad(153.82496),	4.7902588],
                    [2.6526597,	np.deg2rad(122.72683),	6.477916],
                    [10.879429,	np.deg2rad(129.10767),	7.4590895]]
                    # calculated with ANSYS Workbench Mechanical

        c2_pnts_ref = [[2.3828414,	np.deg2rad(127.64108),	-9.6084373],
                        [2.3592996,	np.deg2rad(91.642505),	-8.6852579],
                        [4.2508725,	np.deg2rad(78.427201),	-7.7414523],
                        [11.908319,	np.deg2rad(93.626557),	-10.353354]]
                    # calculated with ANSYS Workbench Mechanical

        c2_pnts = [c1.transform_point_to_other(c1_pnt, c2) for c1_pnt in c1_pnts]
        
        for p1, p2 in zip(c2_pnts, c2_pnts_ref):
            for c1, c2 in zip(p1, p2):
                self.assertAlmostEqual(c1, c2, 5)

    def test_transform_vector_from_global_into_rectangular(self):

        c = CoordinateSystem('C1')
        c.move([1., 2., -4.])
        c.rotate_x(10, degrees=True)
        c.rotate_y(20, degrees=True)
        c.rotate_z(30, degrees=True)
        # test one point
        glob_vec = [1.,1.,1.]
        loc_vec = c.transform_vector_from_global(glob_vec)
        loc_vec_ref = [1.1527617, 0.67212241, 1.1042608]

        for c1, c2 in zip(loc_vec, loc_vec_ref):
            self.assertAlmostEqual(c1, c2, 6)

        # # test multiple points
        glob_vecs = [[1.,1.,1.],[3.,4.,5.]]
        loc_vec = [c.transform_vector_from_global(glob_vec) for glob_vec in glob_vecs]
        loc_vec_ref = [[1.1527617, 0.67212241, 1.1042608],
                       [3.592375, 3.4771317, 5.0004397]]
        for v1, v2 in zip(loc_vec, loc_vec_ref):
            for c1, c2 in zip(v1, v2):
                self.assertAlmostEqual(c1, c2, 6)

    def test_transform_vector_from_global_into_cylindrical(self):

        c = CoordinateSystem('C1', type=EOrientationSystems.CYLINDRICAL)
        c.move([1., 2., -4.])
        c.rotate_x(10, degrees=True)
        c.rotate_y(20, degrees=True)
        c.rotate_z(30, degrees=True)
        # test one vector, one ref point
        glob_vec = [1.,1.,1.]
        glob_pnt = [-6.,4.,7.]
        loc_vec = c.transform_vector_from_global(glob_vec, glob_pnt)
        loc_vec_ref = [-0.2055972, -1.3184604, 1.1042608]

        for c1, c2 in zip(loc_vec, loc_vec_ref):
            self.assertAlmostEqual(c1, c2, 6)

        # test multiple vectors, one ref point
        glob_vecs = [[1.,1.,1.],[3.,4.,5.]]
        glob_pnt = [-6.,4.,7.]
        loc_vec = [c.transform_vector_from_global(glob_vec, glob_pnt) for glob_vec in glob_vecs]
        loc_vec_ref = [[-0.2055972, -1.3184604, 1.1042608],
                       [0.43212494, -4.9808504, 5.0004397]]
        for v1, v2 in zip(loc_vec, loc_vec_ref):
            for c1, c2 in zip(v1, v2):
                self.assertAlmostEqual(c1, c2, 6)

        # test multiple vectors, multiple ref points
        glob_vecs = [[1.,1.,1.],[3.,4.,5.]]
        glob_pnts = [[-6.,4.,7.], [-6.,4.,7.]]
        loc_vec = [c.transform_vector_from_global(glob_vec, glob_pnt) 
                   for glob_vec, glob_pnt in zip(glob_vecs, glob_pnts)]
        
        loc_vec_ref = [[-0.2055972, -1.3184604, 1.1042608],
                       [0.43212494, -4.9808504, 5.0004397]]
        for v1, v2 in zip(loc_vec, loc_vec_ref):
            for c1, c2 in zip(v1, v2):
                self.assertAlmostEqual(c1, c2, 6)

    def test_transform_vector_to_global_from_rectangular(self):

        c = CoordinateSystem('C1')
        c.move([1., 2., -4.])
        c.rotate_x(10, degrees=True)
        c.rotate_y(20, degrees=True)
        c.rotate_z(30, degrees=True)
        # test one point
        loc_vec = [1.1527617, 0.67212241, 1.1042608]
        glob_vec = c.transform_vector_to_global(loc_vec)
        glob_vec_ref = [1.,1.,1.]
        
        for c1, c2 in zip(glob_vec, glob_vec_ref):
            self.assertAlmostEqual(c1, c2, 6)

        # test multiple points
        loc_vecs = [[1.1527617, 0.67212241, 1.1042608],
                       [3.592375, 3.4771317, 5.0004397]]
        glob_vecs = [c.transform_vector_to_global(loc_vec) for loc_vec in loc_vecs]
        glob_vecs_ref = [[1.,1.,1.],[3.,4.,5.]]

        for v1, v2 in zip(glob_vecs, glob_vecs_ref):
            for c1, c2 in zip(v1, v2):
                self.assertAlmostEqual(c1, c2, 6)

    def test_transform_vector_to_global_from_cylindrical(self):

        c = CoordinateSystem('C1', type=EOrientationSystems.CYLINDRICAL)
        c.move([1., 2., -4.])
        c.rotate_x(10, degrees=True)
        c.rotate_y(20, degrees=True)
        c.rotate_z(30, degrees=True)
        # test one vector, one ref point
        loc_vec = [-0.2055972, -1.3184604, 1.1042608]
        loc_pnt = [10.879429,	np.deg2rad(129.10767),	7.4590895]
        glob_vec = c.transform_vector_to_global(loc_vec, loc_pnt)
        glob_vec_ref = [1.,1.,1.]
        for c1, c2 in zip(glob_vec, glob_vec_ref):
            self.assertAlmostEqual(c1, c2, 6)

        # test multiple vectors, one ref point     
        loc_vecs = [[-0.2055972, -1.3184604, 1.1042608],
                       [0.43212494, -4.9808504, 5.0004397]]
        loc_pnt = [10.879429,	np.deg2rad(129.10767),	7.4590895]
        glob_vecs = [c.transform_vector_to_global(loc_vec, loc_pnt) for loc_vec in loc_vecs]
        glob_vecs_ref = [[1.,1.,1.],[3.,4.,5.]]
        for v1, v2 in zip(glob_vecs, glob_vecs_ref):
            for c1, c2 in zip(v1, v2):
                self.assertAlmostEqual(c1, c2, 6)

        # test multiple vectors, multiple ref points
        
        loc_vecs = [[-0.2055972, -1.3184604, 1.1042608],
                    [0.43212494, -4.9808504, 5.0004397]]
        loc_pnts = [[10.879429,	np.deg2rad(129.10767),	7.4590895], 
                     [10.879429,	np.deg2rad(129.10767),	7.4590895]]
        glob_vecs = [c.transform_vector_to_global(loc_vec, loc_pnt) 
                   for loc_vec, loc_pnt in zip(loc_vecs, loc_pnts)]
        glob_vecs_ref = [[1.,1.,1.],[3.,4.,5.]]

        for v1, v2 in zip(glob_vecs, glob_vecs_ref):
            for c1, c2 in zip(v1, v2):
                self.assertAlmostEqual(c1, c2, 6)

    def test_transform_vector_to_other_from_rectangular_to_rectangular(self):

        c1 = CoordinateSystem('C1')
        c1.move([1., 2., -4.])
        c1.rotate_x(10, degrees=True)
        c1.rotate_y(20, degrees=True)
        c1.rotate_z(30, degrees=True)

        c2 = CoordinateSystem('C2')
        c2.move([8., -3., 5.])
        c2.rotate_x(30, degrees=True)
        c2.rotate_y(40, degrees=True)
        c2.rotate_z(50, degrees=True)

        c1_vecs = [[6, 7, 8],
                   [6, -7, 8]]

        c2_vecs_ref =  [[9.060223, 6.1417899, 5.4028489],
                        [2.1604354, -4.6338814, 11.084208]]
                    # calculated with ANSYS Workbench Mechanical

        c2_vecs = [c1.transform_vector_to_other(c2, c1_vec) for c1_vec in c1_vecs]
        
        for v1, v2 in zip(c2_vecs, c2_vecs_ref):
            for c1, c2 in zip(v1, v2):
                self.assertAlmostEqual(c1, c2, 6)

    def test_transform_vector_to_other_from_rectangular_to_cylindrical(self):

        c1 = CoordinateSystem('C1')
        c1.move([1., 2., -4.])
        c1.rotate_x(10, degrees=True)
        c1.rotate_y(20, degrees=True)
        c1.rotate_z(30, degrees=True)

        c2 = CoordinateSystem('C2', type=EOrientationSystems.CYLINDRICAL)
        c2.move([8., -3., 5.])
        c2.rotate_x(30, degrees=True)
        c2.rotate_y(40, degrees=True)
        c2.rotate_z(50, degrees=True)

        ref_point = [-6.8625229, 8.4420236, 7.4590895]
        # ref point in c1 at global [-6, 4, 7]. Transformed with ANSYS Workbench Mechanical

        c1_vecs = [[6, 7, 8],
                   [6, -7, 8]]

        c2_vecs_ref =  [[5.5564038, -9.4305674, 5.4028489],
                        [-4.7612564, -1.8630018, 11.084208]]
                    # calculated with ANSYS Workbench Mechanical

        c2_vecs = [c1.transform_vector_to_other(c2, c1_vec, ref_point) for c1_vec in c1_vecs]
        
        for v1, v2 in zip(c2_vecs, c2_vecs_ref):
            for c1, c2 in zip(v1, v2):
                self.assertAlmostEqual(c1, c2, 6)

    def test_transform_vector_to_other_from_cylindrical_to_rectangular(self):

        c1 = CoordinateSystem('C1', type=EOrientationSystems.CYLINDRICAL)
        c1.move([1., 2., -4.])
        c1.rotate_x(10, degrees=True)
        c1.rotate_y(20, degrees=True)
        c1.rotate_z(30, degrees=True)

        c2 = CoordinateSystem('C2')
        c2.move([8., -3., 5.])
        c2.rotate_x(30, degrees=True)
        c2.rotate_y(40, degrees=True)
        c2.rotate_z(50, degrees=True)

        ref_point = [10.879429,	np.deg2rad(129.10767),	7.4590895]
        # ref point in c1_cyl at global [-6, 4, 7]. Transformed with ANSYS Workbench Mechanical

        c1_vecs = [[6, 7, 8],
                   [6, -7, 8]]

        c2_vecs_ref =  [[-7.4896431, 7.9677196, 5.4240843],
                        [6.2996349, 9.7467169, 3.7836636]]
                    # calculated with ANSYS Workbench Mechanical

        c2_vecs = [c1.transform_vector_to_other(c2, c1_vec, ref_point) for c1_vec in c1_vecs]
        
        for v1, v2 in zip(c2_vecs, c2_vecs_ref):
            for c1, c2 in zip(v1, v2):
                self.assertAlmostEqual(c1, c2, 5)

    def test_transform_vector_to_other_from_cylindrical_to_cylindrical(self):

        c1 = CoordinateSystem('C1', type=EOrientationSystems.CYLINDRICAL)
        c1.move([1., 2., -4.])
        c1.rotate_x(10, degrees=True)
        c1.rotate_y(20, degrees=True)
        c1.rotate_z(30, degrees=True)

        c2 = CoordinateSystem('C2', type=EOrientationSystems.CYLINDRICAL)
        c2.move([8., -3., 5.])
        c2.rotate_x(30, degrees=True)
        c2.rotate_y(40, degrees=True)
        c2.rotate_z(50, degrees=True)

        ref_point = [10.879429,	np.deg2rad(129.10767),	7.4590895]
        # ref point in c1_cyl at global [-6, 4, 7]. Transformed with ANSYS Workbench Mechanical

        c1_vecs = [[6, 7, 8],
                   [6, -7, 8]]

        c2_vecs_ref =  [[8.4255076, 6.9706622, 5.4240843],
                        [9.3287278, -6.9035301, 3.7836636]]
                    # calculated with ANSYS Workbench Mechanical

        c2_vecs = [c1.transform_vector_to_other(c2, c1_vec, ref_point) for c1_vec in c1_vecs]
        
        for v1, v2 in zip(c2_vecs, c2_vecs_ref):
            for c1, c2 in zip(v1, v2):
                self.assertAlmostEqual(c1, c2, 5)

    def test_transform_tensor_from_global_into_rectangular(self):

        c = CoordinateSystem('C1')
        c.move([1., 2., -4.])
        c.rotate_x(10, degrees=True)
        c.rotate_y(20, degrees=True)
        c.rotate_z(30, degrees=True)
        # test as vector
        glob_tens = [0., -1., 0., 0., 0.,0.]
        loc_tens = c.transform_tensor_from_global(glob_tens)
        loc_tens_ref = [-0.29575993, -0.6776137, -2.6626378e-002, -0.44767285, 0.134322, 8.8741284e-002]

        for c1, c2 in zip(loc_tens, loc_tens_ref):
            self.assertAlmostEqual(c1, c2, 6)

        # test as matrix
        glob_tens = [[0, 0, 0],
                     [0,-1, 0],
                     [0, 0, 0]]
        loc_tens = c.transform_tensor_from_global(glob_tens)
        loc_tens_ref = [[-0.29575993, -0.44767285, 0.088741284],
                        [-0.44767285, -0.6776137,  0.134322],
                        [0.088741284,  0.134322,  -0.026626378]]
        
        for row, row_ref in zip(loc_tens, loc_tens_ref):
            for c1, c2 in zip(row, row_ref):
                self.assertAlmostEqual(c1, c2, 6) 

    def test_transform_tensor_from_global_into_cylindrical(self):

        c = CoordinateSystem('C1', type= EOrientationSystems.CYLINDRICAL)
        c.move([1., 2., -4.])
        c.rotate_x(10, degrees=True)
        c.rotate_y(20, degrees=True)
        c.rotate_z(30, degrees=True)
        # test as vector
        glob_tens = [0., -1., 0., 0., 0.,0.]
        ref_pnt = [30,30,30]
        loc_tens = c.transform_tensor_from_global(glob_tens, ref_pnt)
        loc_tens_ref = [-0.81114565, -0.16222797, -2.6626378e-002, -0.36275406, 6.5723232e-002, 0.14696214]

        for c1, c2 in zip(loc_tens, loc_tens_ref):
            self.assertAlmostEqual(c1, c2, 6)

    def test_transform_tensor_to_global_from_rectangular(self):

        c = CoordinateSystem('C1')
        c.move([1., 2., -4.])
        c.rotate_x(10, degrees=True)
        c.rotate_y(20, degrees=True)
        c.rotate_z(30, degrees=True)
        # test as vector
        glob_tens_ref = [0., -1., 0., 0., 0.,0.]
        loc_tens = [-0.29575993, -0.6776137, -2.6626378e-002, -0.44767285, 0.134322, 8.8741284e-002]
        glob_tens = c.transform_tensor_to_global(loc_tens)
        

        for c1, c2 in zip(glob_tens, glob_tens_ref):
            self.assertAlmostEqual(c1, c2, 6)

        # test as matrix
        glob_tens_ref = [[0, 0, 0],
                        [0,-1, 0],
                        [0, 0, 0]]
        loc_tens = [[-0.29575993, -0.44767285, 0.088741284],
                        [-0.44767285, -0.6776137,  0.134322],
                        [0.088741284,  0.134322,  -0.026626378]]
        glob_tens = c.transform_tensor_to_global(loc_tens)
        
        for row, row_ref in zip(glob_tens, glob_tens_ref):
            for c1, c2 in zip(row, row_ref):
                self.assertAlmostEqual(c1, c2, 6) 

    def test_transform_tensor_to_global_from_cylindrical(self):

        c = CoordinateSystem('C1', type= EOrientationSystems.CYLINDRICAL)
        c.move([1., 2., -4.])
        c.rotate_x(10, degrees=True)
        c.rotate_y(20, degrees=True)
        c.rotate_z(30, degrees=True)
        # test as vector
        glob_tens_ref = [0., -1., 0., 0., 0.,0.]
        ref_pnt = [37.759005, 0.56643013, 36.813822]
        loc_tens = [-0.81114565, -0.16222797, -2.6626378e-002, -0.36275406, 6.5723232e-002, 0.14696214]
        glob_tens = c.transform_tensor_to_global(loc_tens, ref_pnt)
        

        for c1, c2 in zip(glob_tens, glob_tens_ref):
            self.assertAlmostEqual(c1, c2, 6)

    def test_transform_tensor_to_other_from_rectangular_to_rectangular(self):

        c1 = CoordinateSystem('C1')
        c1.move([1., 2., -4.])
        c1.rotate_x(10, degrees=True)
        c1.rotate_y(20, degrees=True)
        c1.rotate_z(30, degrees=True)

        c2 = CoordinateSystem('C2')
        c2.move([8., -3., 5.])
        c2.rotate_x(30, degrees=True)
        c2.rotate_y(40, degrees=True)
        c2.rotate_z(50, degrees=True)

        c1_tens = [-0.29575993, -0.6776137, -2.6626378e-002, -0.44767285, 0.134322, 8.8741284e-002]

        c2_tens_ref =  [-0.75690331, -9.6390665e-002, -0.14670602, -0.27010815, 0.11891632, 0.33323006]
                    # calculated with ANSYS Workbench Mechanical

        c2_tens = c1.transform_tensor_to_other(c2, c1_tens)
        
        for v1, v2 in zip(c2_tens, c2_tens_ref):
            self.assertAlmostEqual(v1, v2, 6)

    def test_transform_tensor_to_other_from_rectangular_to_cylindrical(self):

        c1 = CoordinateSystem('C1')
        c1.move([1., 2., -4.])
        c1.rotate_x(10, degrees=True)
        c1.rotate_y(20, degrees=True)
        c1.rotate_z(30, degrees=True)

        c2 = CoordinateSystem('C2', type=EOrientationSystems.CYLINDRICAL)
        c2.move([8., -3., 5.])
        c2.rotate_x(30, degrees=True)
        c2.rotate_y(40, degrees=True)
        c2.rotate_z(50, degrees=True)

        c1_tens = [-0.29575993, -0.6776137, -2.6626378e-002, -0.44767285, 0.134322, 8.8741284e-002]
        ref_pnt = [31.86188, 20.262356, 36.813822]


        c2_tens_ref =  [-0.85213174, -1.1622426e-003, -0.14670602, 3.1470364e-002, -1.3057871e-002, 0.35357157]
                    # calculated with ANSYS Workbench Mechanical

        c2_tens = c1.transform_tensor_to_other(c2, c1_tens, ref_pnt)
        
        for v1, v2 in zip(c2_tens, c2_tens_ref):
            self.assertAlmostEqual(v1, v2, 6)

    def test_transform_tensor_to_other_from_cylindrical_to_rectangular(self):

        c1 = CoordinateSystem('C1', type=EOrientationSystems.CYLINDRICAL)
        c1.move([1., 2., -4.])
        c1.rotate_x(10, degrees=True)
        c1.rotate_y(20, degrees=True)
        c1.rotate_z(30, degrees=True)

        c2 = CoordinateSystem('C2')
        c2.move([8., -3., 5.])
        c2.rotate_x(30, degrees=True)
        c2.rotate_y(40, degrees=True)
        c2.rotate_z(50, degrees=True)

        c1_tens = [-0.81114565, -0.16222797, -2.6626378e-002, -0.36275406, 6.5723232e-002, 0.14696214]
        ref_pnt = [37.759005, 0.56643013, 36.813822]
        c2_tens_ref =  [-0.75690331, -9.6390665e-002, -0.14670602, -0.27010815, 0.11891632, 0.33323006]
                    # calculated with ANSYS Workbench Mechanical

        c2_tens = c1.transform_tensor_to_other(c2, c1_tens, ref_pnt)
        
        for v1, v2 in zip(c2_tens, c2_tens_ref):
            self.assertAlmostEqual(v1, v2, 6)

    def test_transform_tensor_to_other_from_cylindrical_to_cylindrical(self):

        c1 = CoordinateSystem('C1', type=EOrientationSystems.CYLINDRICAL)
        c1.move([1., 2., -4.])
        c1.rotate_x(10, degrees=True)
        c1.rotate_y(20, degrees=True)
        c1.rotate_z(30, degrees=True)

        c2 = CoordinateSystem('C2', type=EOrientationSystems.CYLINDRICAL)
        c2.move([8., -3., 5.])
        c2.rotate_x(30, degrees=True)
        c2.rotate_y(40, degrees=True)
        c2.rotate_z(50, degrees=True)

        c1_tens = [-0.81114565, -0.16222797, -2.6626378e-002, -0.36275406, 6.5723232e-002, 0.14696214]
        ref_pnt = [37.759005, 0.56643013, 36.813822]
        c2_tens_ref =  c2_tens_ref =  [-0.85213174, -1.1622426e-003, -0.14670602, 3.1470364e-002, -1.3057871e-002, 0.35357157]
                    # calculated with ANSYS Workbench Mechanical

        c2_tens = c1.transform_tensor_to_other(c2, c1_tens, ref_pnt)
        
        for v1, v2 in zip(c2_tens, c2_tens_ref):
            self.assertAlmostEqual(v1, v2, 6)