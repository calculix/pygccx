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
from unittest import TestCase
from pygccx.enums import EDatEntities, EResultLocations
from pygccx.result_reader import DatResult#, FrdResultSet

class TestDatResult(TestCase):

    def setUp(self) -> None:
        test_data_path = os.path.dirname(os.path.abspath(__file__))
        self.test_data_path = os.path.join(test_data_path, 'test_data')


    def test_from_file(self):
        dat_result = DatResult.from_file(os.path.join(self.test_data_path, 'beam.dat'))

        # the dat contains 1 step with 3 times 0.34, 0.68, 1.0
        self.assertEqual(len(dat_result.step_times), 3)
        self.assertEqual(dat_result.step_times[0], 0.34)
        self.assertEqual(dat_result.step_times[1], 0.68)
        self.assertEqual(dat_result.step_times[2], 1.0)

            #         sk.NodePrint(mesh.get_node_set_by_name('BEAM'),[enums.ENodePrintResults.U,
            #                                                 enums.ENodePrintResults.RF]),
            # sk.ElPrint(mesh.get_el_set_by_name('BEAM'),[enums.EElPrintResults.S,
            #                                             enums.EElPrintResults.EVOL,
            #                                             enums.EElPrintResults.COORD,
            #                                             enums.EElPrintResults.E,
            #                                             enums.EElPrintResults.ME,
            #                                             enums.EElPrintResults.ENER,
            #                                             enums.EElPrintResults.ELKE,
            #                                             enums.EElPrintResults.ELSE,
            #                                             enums.EElPrintResults.EMAS])

        # the dat contains 11 result entities: U, RF, S, EVOL, COORD, E, ME, ENER, ELKE, ELSE, EMAS 
        # multiplied with number of times gives 33 result sets
        self.assertEqual(len(dat_result.result_sets), 33)
        # check if result entities what they should be
        re = {rs.entity for rs in dat_result.result_sets}
        self.assertEqual(len(re), 11)
        re_diff = re - {EDatEntities.U, EDatEntities.RF, EDatEntities.S, EDatEntities.EVOL,
                        EDatEntities.COORD, EDatEntities.E, EDatEntities.ME, EDatEntities.ENER,
                        EDatEntities.ELKE, EDatEntities.ELSE, EDatEntities.EMAS}
        self.assertEqual(len(re_diff), 0)

        # check if there are 2 * 3 = 6 results with entity_location == NODAL
        no_nodel = len([rs for rs in dat_result.result_sets if rs.entity_location == EResultLocations.NODAL])
        self.assertEqual(no_nodel, 6)
        # there are 467 nodes in the frd. Check if every node result set has 467 values
        for rs in dat_result.result_sets:
            if rs.entity_location == EResultLocations.NODAL:
                self.assertEqual(len(rs.values), 467)

        # check component names of each result set
        for rs in dat_result.result_sets:
            if rs.entity == EDatEntities.U:
                self.assertEqual(rs.component_names, ('vx', 'vy','vz'))
                self.assertEqual(rs.no_components, 3)
            if rs.entity == EDatEntities.RF:
                self.assertEqual(rs.component_names, ('fx', 'fy','fz'))
                self.assertEqual(rs.no_components, 3)
            if rs.entity == EDatEntities.S:
                self.assertEqual(rs.component_names, ('sxx','syy','szz','sxy','sxz','syz'))
                self.assertEqual(rs.no_components, 6)
            if rs.entity == EDatEntities.EVOL:
                self.assertEqual(rs.component_names, ('volume',))
                self.assertEqual(rs.no_components, 1)
            if rs.entity == EDatEntities.COORD:
                self.assertEqual(rs.component_names, ('x', 'y','z'))
                self.assertEqual(rs.no_components, 3)
            if rs.entity == EDatEntities.E:
                self.assertEqual(rs.component_names, ('exx','eyy','ezz','exy','exz','eyz'))
                self.assertEqual(rs.no_components, 6)
            if rs.entity == EDatEntities.ME:
                self.assertEqual(rs.component_names, ('exx','eyy','ezz','exy','exz','eyz'))
                self.assertEqual(rs.no_components, 6)
            if rs.entity == EDatEntities.ENER:
                self.assertEqual(rs.component_names, ('energy',))
                self.assertEqual(rs.no_components, 1)
            if rs.entity == EDatEntities.ELKE:
                self.assertEqual(rs.component_names, ('energy',))
                self.assertEqual(rs.no_components, 1)
            if rs.entity == EDatEntities.ELSE:
                self.assertEqual(rs.component_names, ('energy',))
                self.assertEqual(rs.no_components, 1)
            if rs.entity == EDatEntities.EMAS:
                self.assertEqual(rs.component_names, ('mass','xx','yy','zz','xy','xz','yz'))
                self.assertEqual(rs.no_components, 7)

            # check if every value in values has a length of no_components
            for value in rs.values.values():
                self.assertEqual(value.shape[-1], rs.no_components)

    def test_get_result_sets_by_entity(self):
        dat_result = DatResult.from_file(os.path.join(self.test_data_path, 'beam.dat'))
        disp_sets = dat_result.get_result_sets_by_entity(EDatEntities.U)
        self.assertEqual(len(disp_sets), 3)

        # check if all sets are U
        re = {rs.entity for rs in disp_sets}
        self.assertEqual(len(re), 1)
        self.assertEqual(re.pop(), EDatEntities.U)

        # test with entity not in result
        sets = dat_result.get_result_sets_by_entity(EDatEntities.CDIS)
        self.assertEqual(len(sets), 0)

    def test_get_result_set_by_entity_and_time(self):

        dat_result = DatResult.from_file(os.path.join(self.test_data_path, 'beam.dat'))
        disp_034 = dat_result.get_result_set_by_entity_and_time(EDatEntities.U, 0.34)
        self.assertEqual(disp_034.entity, EDatEntities.U) # type: ignore
        self.assertAlmostEqual(disp_034.step_time, 0.34) # type: ignore

        # time 0.5 should return result set for timwe 0.34 because its closest
        disp_034 = dat_result.get_result_set_by_entity_and_time(EDatEntities.U, 0.5)
        self.assertEqual(disp_034.entity, EDatEntities.U) # type: ignore
        self.assertAlmostEqual(disp_034.step_time, 0.34) # type: ignore

        # time 0 should return the first result set for timwe 0.34 because its closest
        disp_034 = dat_result.get_result_set_by_entity_and_time(EDatEntities.U, 0)
        self.assertEqual(disp_034.entity, EDatEntities.U) # type: ignore
        self.assertAlmostEqual(disp_034.step_time, 0.34) # type: ignore

        # time 100 should return the last result set for timwe 1.0 because its closest
        disp_1 = dat_result.get_result_set_by_entity_and_time(EDatEntities.U, 100)
        self.assertEqual(disp_1.entity, EDatEntities.U) # type: ignore
        self.assertAlmostEqual(disp_1.step_time, 1) # type: ignore

        # test with entity not in result
        res = dat_result.get_result_set_by_entity_and_time(EDatEntities.CDIS, 0.34)
        self.assertIsNone(res)

    def test_get_result_set_by_entity_and_index(self):

        dat_result = DatResult.from_file(os.path.join(self.test_data_path, 'beam.dat'))
        disp_0 = dat_result.get_result_set_by_entity_and_index(EDatEntities.U, 0)
        self.assertEqual(disp_0.entity, EDatEntities.U) # type: ignore
        self.assertAlmostEqual(disp_0.step_time, 0.34) # type: ignore

        disp_1 = dat_result.get_result_set_by_entity_and_index(EDatEntities.U, 1)
        self.assertEqual(disp_1.entity, EDatEntities.U) # type: ignore
        self.assertAlmostEqual(disp_1.step_time, 0.68) # type: ignore

        disp_2 = dat_result.get_result_set_by_entity_and_index(EDatEntities.U, 2)
        self.assertEqual(disp_0.entity, EDatEntities.U) # type: ignore
        self.assertAlmostEqual(disp_2.step_time, 1) # type: ignore

        disp_last = dat_result.get_result_set_by_entity_and_index(EDatEntities.U, -1)
        self.assertEqual(disp_last.entity, EDatEntities.U) # type: ignore
        self.assertAlmostEqual(disp_last.step_time, 1) # type: ignore

        # test with entity not in result
        res = dat_result.get_result_set_by_entity_and_index(EDatEntities.CDIS, 0)
        self.assertIsNone(res)

