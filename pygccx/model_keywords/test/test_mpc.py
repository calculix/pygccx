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

from pygccx.model_keywords import Mpc
from pygccx.enums import EMpcTypes, ESetTypes
from pygccx.protocols import IKeyword

@dataclass()
class SetMock():
    name:str
    type:ESetTypes
    dim:int
    ids:set[int]

class TestMpc(TestCase):

    def test_is_IKeyword(self):
        m = Mpc(EMpcTypes.PLANE,[1,2,3])
        self.assertTrue(isinstance(m, IKeyword))

    def test_beam(self):
        m = Mpc(EMpcTypes.BEAM, [1,2])
        known = '*MPC\n'
        known += 'BEAM,1,2\n'
        self.assertEqual(str(m), known)

    def test_exception_beam(self):
        # number of nids must be exacly 2
        self.assertRaises(ValueError, Mpc, EMpcTypes.BEAM, [])
        self.assertRaises(ValueError, Mpc, EMpcTypes.BEAM, [1])
        self.assertRaises(ValueError, Mpc, EMpcTypes.BEAM, [1,2,3])

    def test_straight(self):
        m = Mpc(EMpcTypes.STRAIGHT, [1,2])
        known = '*MPC\n'
        known += 'STRAIGHT,1,2\n'
        self.assertEqual(str(m), known)

        m = Mpc(EMpcTypes.STRAIGHT, [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17])
        known = '*MPC\n'
        known += 'STRAIGHT,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,\n'
        known += '16,17\n'
        self.assertEqual(str(m), known)

    def test_exception_straight(self):
        # number of nids must be at least 2
        self.assertRaises(ValueError, Mpc, EMpcTypes.STRAIGHT, [])
        self.assertRaises(ValueError, Mpc, EMpcTypes.STRAIGHT, [1])

    def test_plane(self):
        m = Mpc(EMpcTypes.PLANE, [1,2,3])
        known = '*MPC\n'
        known += 'PLANE,1,2,3\n'
        self.assertEqual(str(m), known)

        m = Mpc(EMpcTypes.PLANE, [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17])
        known = '*MPC\n'
        known += 'PLANE,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,\n'
        known += '16,17\n'
        self.assertEqual(str(m), known)

    def test_exception_plane(self):
        # number of nids must be at least 3
        self.assertRaises(ValueError, Mpc, EMpcTypes.PLANE, [])
        self.assertRaises(ValueError, Mpc, EMpcTypes.PLANE, [1])
        self.assertRaises(ValueError, Mpc, EMpcTypes.PLANE, [1,2])

    def test_meanrot(self):
        m = Mpc(EMpcTypes.MEANROT, [1,1,1,2,2,2,3,3,3,100])
        known = '*MPC\n'
        known += 'MEANROT,1,1,1,2,2,2,3,3,3,100\n'
        self.assertEqual(str(m), known)

    def test_exception_meanrot(self):
        # number of nids must be at least 4
        for i in range(4):
            self.assertRaises(ValueError, Mpc, EMpcTypes.MEANROT, [1]*i)
        # nids not listed 3 times
        self.assertRaises(ValueError, Mpc, EMpcTypes.MEANROT, [1,1,1,2,2,3])
        # no last pilot node
        self.assertRaises(ValueError, Mpc, EMpcTypes.MEANROT, [1,1,1,2,2,2])
        # nodes not listed in equal tuples
        self.assertRaises(ValueError, Mpc, EMpcTypes.MEANROT, [1,2,2,1,1,2,100])

    def test_dist(self):
        m = Mpc(EMpcTypes.DIST, [1,1,1,2,2,2,100])
        known = '*MPC\n'
        known += 'DIST,1,1,1,2,2,2,100\n'
        self.assertEqual(str(m), known)

    def test_exception_dist(self):
        # number of nids must be exactly 7
        self.assertRaises(ValueError, Mpc, EMpcTypes.DIST, [1]*6)
        self.assertRaises(ValueError, Mpc, EMpcTypes.DIST, [1]*8)
        # nids not listed 3 times
        self.assertRaises(ValueError, Mpc, EMpcTypes.DIST, [1,1,1,2,2,3,100])
        # no last pilot node
        self.assertRaises(ValueError, Mpc, EMpcTypes.DIST, [1,1,1,2,2,2])
        # nodes not listed in equal tuples
        self.assertRaises(ValueError, Mpc, EMpcTypes.DIST, [1,2,2,1,1,2,100])

    def test_meanrot_from_node_set(self):

        s = SetMock('', ESetTypes.NODE, 2, [1,2,3])
        m = Mpc.meanrot_from_node_set(s, 100)
        known = '*MPC\n'
        known += 'MEANROT,1,1,1,2,2,2,3,3,3,100\n'
        self.assertEqual(str(m), known)

        s = SetMock('', ESetTypes.ELEMENT, 2, [1,2,3])
        self.assertRaises(ValueError, Mpc.meanrot_from_node_set, s, 100)

    def test_straight_from_node_set(self):

        s = SetMock('', ESetTypes.NODE, 2, [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17])
        m = Mpc.straight_from_node_set(s, 100)
        known = '*MPC\n'
        known += 'STRAIGHT,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,\n'
        known += '16,17\n'
        self.assertEqual(str(m), known)

        s = SetMock('', ESetTypes.ELEMENT, 2, [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17])
        self.assertRaises(ValueError, Mpc.straight_from_node_set, s, 100)

    def test_plane_from_node_set(self):

        s = SetMock('', ESetTypes.NODE, 2, [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17])
        m = Mpc.plane_from_node_set(s, 100)
        known = '*MPC\n'
        known += 'PLANE,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,\n'
        known += '16,17\n'
        self.assertEqual(str(m), known)

        s = SetMock('', ESetTypes.ELEMENT, 2, [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17])
        self.assertRaises(ValueError, Mpc.plane_from_node_set, s, 100)

    def test_beam_from_2_nodes(self):

        m = Mpc.beam_from_2_nodes(1,2)
        known = '*MPC\n'
        known += 'BEAM,1,2\n'
        self.assertEqual(str(m), known)

    def test_dist_from_3_nodes(self):

        m = Mpc.dist_from_3_nodes(1,2,100)
        known = '*MPC\n'
        known += 'DIST,1,1,1,2,2,2,100\n'
        self.assertEqual(str(m), known)
