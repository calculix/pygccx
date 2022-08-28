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

import unittest
from dataclasses import dataclass
from pygccx.mesh import Mesh
from pygccx.enums import ESetTypes, EEtypes

@dataclass()
class SetMock():
    name:str
    type:ESetTypes
    dim:int
    ids:set[int]

class TestMesh(unittest.TestCase):

    def setUp(self) -> None:
        self.mesh = Mesh(nodes={}, elements={}, node_sets=[], element_sets=[])
    
    def _make_4_nodes(self):
        self.mesh.add_node([0,0,0])
        self.mesh.add_node([1,0,0])
        self.mesh.add_node([1,1,0])
        self.mesh.add_node([0,1,0])

    def test_add_node_wo_id(self):
        id = self.mesh.add_node([1,2,3])
        self.assertEqual(len(self.mesh.nodes), 1)
        self.assertEqual(id, 1)
        for c1, c2 in zip(self.mesh.nodes[id], [1,2,3]):
            self.assertEqual(c1, c2)

    def test_add_node_w_id(self):
        id = self.mesh.add_node([1,2,3], id=5)
        self.assertEqual(len(self.mesh.nodes), 1)
        self.assertEqual(id, 5)
        for c1, c2 in zip(self.mesh.nodes[id], [1,2,3]):
            self.assertEqual(c1, c2)

    def test_add_node_w_set(self):
        s = SetMock('S1', ESetTypes.NODE, 2, set())
        self.mesh.add_node([1,2,3], id=5, node_set=s)
        self.assertEqual(len(s.ids), 1)
        self.assertTrue(5 in s.ids)

    def test_add_node_id_lower_1(self):
        self.assertRaises(ValueError, self.mesh.add_node, [1,2,3], id=0)
        self.assertRaises(ValueError, self.mesh.add_node, [1,2,3], id=-1)

    def test_add_node_coords_not_len_3(self):
        self.assertRaises(ValueError, self.mesh.add_node, [1,2])

    def test_add_node_coords_not_numeric(self):
        self.assertRaises(ValueError, self.mesh.add_node, [1,'a'])

    def test_add_node_wrong_set_type(self):
        s = SetMock('S1', ESetTypes.ELEMENT, 2, set())
        self.assertRaises(ValueError, self.mesh.add_node, [1, 2], node_set=s)


    def test_add_element_wo_id(self):
        id = self.mesh.add_element(EEtypes.C3D4, (1,2,3,4))
        self.assertEqual(len(self.mesh.elements), 1)
        self.assertEqual(id, 1)
        self.assertEqual(self.mesh.elements[id].type, EEtypes.C3D4)
        for c1, c2 in zip(self.mesh.elements[id].node_ids, [1,2,3,4]):
            self.assertEqual(c1, c2)

    def test_add_element_w_id(self):
        id = self.mesh.add_element(EEtypes.C3D4, (1,2,3,4), id=5)
        self.assertEqual(len(self.mesh.elements), 1)
        self.assertEqual(id, 5)
        self.assertEqual(self.mesh.elements[id].type, EEtypes.C3D4)
        for c1, c2 in zip(self.mesh.elements[id].node_ids, [1,2,3]):
            self.assertEqual(c1, c2)

    def test_add_element_w_set(self):
        s = SetMock('S1', ESetTypes.ELEMENT, 2, set())
        self.mesh.add_element(EEtypes.C3D4, (1,2,3,4), id=5, el_set=s)
        self.assertEqual(len(s.ids), 1)
        self.assertTrue(5 in s.ids)

    def test_add_element_id_lower_1(self):
        self.assertRaises(ValueError, self.mesh.add_element, EEtypes.C3D4, (1,2,3,4), id=0)
        self.assertRaises(ValueError, self.mesh.add_element, EEtypes.C3D4, (1,2,3,4), id=-1)

    def test_add_element_wrong_node_number(self):
        self.assertRaises(ValueError, self.mesh.add_element, EEtypes.C3D4, (1,2,3), id=0)

    def test_add_element_wrong_set_type(self):
        s = SetMock('S1', ESetTypes.NODE, 2, set())
        self.assertRaises(ValueError, self.mesh.add_element, EEtypes.C3D4, (1,2,3,4), el_set=s)

    def test_get_nodes_by_ids(self):
        # make some nodes
        self.mesh.add_node([0,0,0])
        self.mesh.add_node([1,0,0])
        self.mesh.add_node([1,1,0])
        self.mesh.add_node([0,1,0])

        nds = self.mesh.get_nodes_by_ids()
        self.assertEqual(len(nds), 0)

        nds = self.mesh.get_nodes_by_ids(1)
        self.assertEqual(nds, ((0,0,0),))

        nds = self.mesh.get_nodes_by_ids(1,3)
        self.assertEqual(nds, ((0,0,0),(1,1,0)))

        self.assertRaises(KeyError, self.mesh.get_nodes_by_ids, 5)

    def test_get_elements_by_ids(self):

        # make some elements (nodes dont need to exist for making an lement)
        self.mesh.add_element(EEtypes.SPRING2, (1,2))
        self.mesh.add_element(EEtypes.SPRING2, (2,3))
        self.mesh.add_element(EEtypes.SPRING2, (3,4))
        self.mesh.add_element(EEtypes.SPRING2, (4,1))

        els = self.mesh.get_elements_by_ids()
        self.assertEqual(len(els), 0)

        els = self.mesh.get_elements_by_ids(1,3)
        self.assertEqual(len(els), 2)
        self.assertEqual(els[0].node_ids, (1,2))
        self.assertEqual(els[1].node_ids, (3,4))

        self.assertRaises(KeyError, self.mesh.get_elements_by_ids, 5)

    def test_get_elements_by_type(self):

        # make some elements (nodes dont need to exist for making an lement)
        self.mesh.add_element(EEtypes.SPRING2, (1,2))
        self.mesh.add_element(EEtypes.SPRINGA, (2,3))
        self.mesh.add_element(EEtypes.GAPUNI, (3,4))
        self.mesh.add_element(EEtypes.GAPUNI, (4,1))

        els = self.mesh.get_elements_by_type(EEtypes.C3D10)
        self.assertEqual(len(els), 0)

        els = self.mesh.get_elements_by_type(EEtypes.SPRINGA)
        self.assertEqual(len(els), 1)

        els = self.mesh.get_elements_by_type(EEtypes.GAPUNI)
        self.assertEqual(len(els), 2)

    def test_get_set_by_name_and_type(self):

        self.mesh.add_set('N1', ESetTypes.NODE, [1,2,3,4])
        self.mesh.add_set('N2', ESetTypes.NODE, [5,6,7,8])
        self.mesh.add_set('N3', ESetTypes.NODE, [9,10,11,12])
        self.mesh.add_set('E1', ESetTypes.ELEMENT, [1,2,3,4])
        self.mesh.add_set('E2', ESetTypes.ELEMENT, [5,6,7,8])
        self.mesh.add_set('E3', ESetTypes.ELEMENT, [9,10,11,12])

        s = self.mesh.get_set_by_name_and_type('N2', ESetTypes.NODE)
        self.assertEqual('N2', s.name)

        s = self.mesh.get_set_by_name_and_type('E2', ESetTypes.ELEMENT)
        self.assertEqual('E2', s.name)

        self.assertRaises(ValueError, self.mesh.get_set_by_name_and_type, 'Foo', ESetTypes.NODE)

    def test_get_max_node_id_and_get_next_node_id(self):

        self.assertEqual(self.mesh.get_max_node_id(), 0)
        self.assertEqual(self.mesh.get_next_node_id(), 1)

        self.mesh.add_node([0,0,0])
        self.mesh.add_node([1,0,0])
        self.mesh.add_node([1,1,0])
        self.mesh.add_node([0,1,0])

        self.assertEqual(self.mesh.get_max_node_id(), 4)
        self.assertEqual(self.mesh.get_next_node_id(), 5)

    def test_get_max_element_id_and_get_next_element_id(self):

        self.assertEqual(self.mesh.get_max_element_id(), 0)
        self.assertEqual(self.mesh.get_next_element_id(), 1)

        self.mesh.add_element(EEtypes.SPRING2, (1,2))
        self.mesh.add_element(EEtypes.SPRINGA, (2,3))
        self.mesh.add_element(EEtypes.GAPUNI, (3,4))
        self.mesh.add_element(EEtypes.GAPUNI, (4,1))

        self.assertEqual(self.mesh.get_max_element_id(), 4)
        self.assertEqual(self.mesh.get_next_element_id(), 5)

    def test_add_set(self):

        # happy case, add node set
        self.mesh.add_set("N1", ESetTypes.NODE, ids=[1,2,3,4])
        self.assertEqual(len(self.mesh.node_sets), 1)
        self.assertEqual(self.mesh.node_sets[-1].name, 'N1')
        # happy case, add element set
        self.mesh.add_set("E1", ESetTypes.ELEMENT, ids=[1,2,3,4])
        self.assertEqual(len(self.mesh.element_sets), 1)
        self.assertEqual(self.mesh.element_sets[-1].name, 'E1')
        # Add a node set with an existing name
        self.assertRaises(ValueError, self.mesh.add_set, "N1", ESetTypes.NODE, ids=[5,6,7,8])
        # Add an element set with an existing name
        self.assertRaises(ValueError, self.mesh.add_set, "E1", ESetTypes.ELEMENT, ids=[5,6,7,8])   

    def test_change_element_type(self):

        self.mesh.add_element(EEtypes.SPRING2, (1,2))
        self.mesh.change_element_type(EEtypes.SPRINGA, 1)
        self.assertEqual(self.mesh.elements[1].type, EEtypes.SPRINGA)

        self.assertRaises(ValueError, self.mesh.change_element_type, EEtypes.C3D4, 1)

