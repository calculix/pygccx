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

import os
import unittest
from dataclasses import dataclass
from pygccx.mesh.mesh_factory import mesh_from_inp, mesh_from_frd
from pygccx.enums import ESetTypes, EEtypes, ESurfTypes
from pygccx.exceptions import ElementTypeNotSupportedError

@dataclass()
class SetMock():
    name:str
    type:ESetTypes
    dim:int
    ids:set[int]

class TestInpFactory(unittest.TestCase):
    
    def setUp(self) -> None:
        data_path = os.path.dirname(os.path.abspath(__file__))
        self.data_path = os.path.join(data_path, 'test_data')

    def test_beam_and_gap(self):
        # reads beam_and_gap.inp
        # file contains *NODE, *ELEMENT, *NSET, *ELSET, *SURFACE (face based)
        # in file:
        #   no nodes: 4405
        #   no elems: 2342 one of them is unsupported (B32)
        #   no nset: 4
        #       NALL: 4405 nodes
        #       FIX: 105 nodes
        #       LOAD: 105 nodes
        #       BEAM: 4403 nodes
        #   no elset: 3
        #       EALL: 2341 elems
        #       GAP: 1 elem
        #       BEAM: 2340 elems
        #   no surface: 3
        #       LOAD_SURF: 44 faces
        #       NODE_SURF: 4 nodes
        #       ELEM_SURF: 9 faces (TYPE not specified)
        mesh = mesh_from_inp(
            os.path.join(self.data_path, 'beam_and_gap.inp'),
            ignore_unsup_elems= True
        )

        self.assertEqual(len(mesh.nodes), 4405)
        self.assertEqual(len(mesh.elements), 2341)
        self.assertEqual(len(mesh.node_sets), 4)
        self.assertEqual(len(mesh.element_sets), 3)
        self.assertEqual(len(mesh.surfaces), 3)

        nall = mesh.get_node_set_by_name('NALL')
        self.assertIsNotNone(nall)
        self.assertEqual(len(nall.ids), 4405)

        fix = mesh.get_node_set_by_name('FIX')
        self.assertIsNotNone(fix)
        self.assertEqual(len(fix.ids), 105)

        load = mesh.get_node_set_by_name('LOAD')
        self.assertIsNotNone(load)
        self.assertEqual(len(load.ids), 105)

        beam = mesh.get_node_set_by_name('BEAM')
        self.assertIsNotNone(beam)
        self.assertEqual(len(beam.ids), 4403)

        eall = mesh.get_el_set_by_name('EALL')
        self.assertIsNotNone(eall)
        self.assertEqual(len(eall.ids), 2341)

        beam = mesh.get_el_set_by_name('BEAM')
        self.assertIsNotNone(beam)
        self.assertEqual(len(beam.ids), 2340)

        load_surf = mesh.get_surface_by_name('LOAD_SURF')
        self.assertIsNotNone(load_surf)
        self.assertEqual(len(load_surf.element_faces), 44)  # type: ignore
        self.assertEqual(load_surf.type, ESurfTypes.EL_FACE)

        node_surf = mesh.get_surface_by_name('NODE_SURF')
        self.assertIsNotNone(node_surf)
        self.assertEqual(len(node_surf.node_ids), 3)  # type: ignore
        self.assertEqual(len(node_surf.node_set_names), 1)  # type: ignore
        self.assertEqual(node_surf.type, ESurfTypes.NODE)

        elem_surf = mesh.get_surface_by_name('ELEM_SURF')
        self.assertIsNotNone(elem_surf)
        self.assertEqual(len(elem_surf.element_faces), 9)  # type: ignore
        self.assertEqual(elem_surf.type, ESurfTypes.EL_FACE)

        for e in mesh.elements.values():
            self.assertTrue(e.type in [EEtypes.C3D10, EEtypes.GAPUNI])   

    def test_beam_and_gap_unsupported_element(self):   
        # reads beam_and_gap.inp
        # file contains one unsupported element
        self.assertRaises(
            ElementTypeNotSupportedError,
            mesh_from_inp, 
            os.path.join(self.data_path, 'beam_and_gap.inp')
        )

    
    def test_beam_and_gap_clear_mesh(self):  
        # clear.inp
        # file contains *NODE (with NSET), *ELEMENT (with ELSET), 
        #               *SURFACE (face based), *SURFACE (node based)
        # in file:
        #   no nodes: 7, 3 of them are attached only to beams
        #   no elems: 2, 1 C3D4 and 1 B32
        #   no nset: 1
        #       NALL: 7 nodes
        #   no elset: 2
        #       TET: 1 elems
        #       BEAM: 1 elem
        #   no surface: 2
        #       EL_SURF: 2 faces, one tet-face, 1 beam face
        #       NODE_SURF: 4 nodes, one tet node, 3 beam nodes

        mesh = mesh_from_inp(
            os.path.join(self.data_path, 'clear.inp'),
            ignore_unsup_elems= True,
            clear_mesh=True
        )

        self.assertEqual(len(mesh.nodes), 4) # only tet nodes
        self.assertEqual(len(mesh.elements), 1) # only the tet
        self.assertEqual(len(mesh.node_sets), 1) # but with 4 nodes
        self.assertEqual(len(mesh.element_sets), 1) # only the tet set
        self.assertEqual(len(mesh.surfaces), 2) # but with removed entities

class TestFrdFactory(unittest.TestCase):

    def setUp(self) -> None:
        data_path = os.path.dirname(os.path.abspath(__file__))
        self.data_path = os.path.join(data_path, 'test_data')

    def test_beam_and_gap_w_skip_wo_clean(self):
        # reads beam_and_gap.frd
        # in file:
        #   no nodes: 4405
        #   no elems: 2341 one of them is unsupported (GAP)
        # after reading file:
        #   no nodes: 4405
        #   no elems: 2340

        mesh = mesh_from_frd(
            os.path.join(self.data_path, 'beam_and_gap.frd'),
            ignore_unsup_elems=True)
        
        self.assertEqual(len(mesh.nodes), 4405)
        self.assertEqual(len(mesh.elements), 2340)

    def test_beam_and_gap_w_skip_w_clean(self):
        # reads beam_and_gap.frd
        # in file:
        #   no nodes: 4405
        #   no elems: 2341 one of them is unsupported (GAP)
        # after reading file:
        #   no nodes: 4403 # the two nodes of the GAP are deleted
        #   no elems: 2340

        mesh = mesh_from_frd(
            os.path.join(self.data_path, 'beam_and_gap.frd'),
            ignore_unsup_elems=True, clear_mesh=True)
        
        self.assertEqual(len(mesh.nodes), 4403)
        self.assertEqual(len(mesh.elements), 2340)

    def test_beam_and_gap_wo_skip(self):
        # reads beam_and_gap.frd
        # The unsupported GAP-element raises an exception

        path = os.path.join(self.data_path, 'beam_and_gap.frd')
        self.assertRaises(ElementTypeNotSupportedError, mesh_from_frd, path, ignore_unsup_elems=False)