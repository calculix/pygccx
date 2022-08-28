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
from pygccx.enums import EFrdEntities
from pygccx.result_reader import FrdResult#, FrdResultSet

class TestFrdResult(TestCase):

    def setUp(self) -> None:
        test_data_path = os.path.dirname(os.path.abspath(__file__))
        self.test_data_path = os.path.join(test_data_path, 'test_data')


    def test_from_file(self):
        frd_result = FrdResult.from_file(os.path.join(self.test_data_path, 'beam.frd'))

        # the frd contains 1 step with 3 times 0.34, 0.68, 1.0
        self.assertEqual(len(frd_result.step_times), 3)
        self.assertEqual(frd_result.step_times[0], 0.34)
        self.assertEqual(frd_result.step_times[1], 0.68)
        self.assertEqual(frd_result.step_times[2], 1.0)

        # the frd contains 4 result entities: DISP, STRESS, FORC, ERROR
        # multiplied with number of times gives 12 result sets
        self.assertEqual(len(frd_result.result_sets), 12)
        # check if result entities what they should be
        re = {rs.entity for rs in frd_result.result_sets}
        self.assertEqual(len(re), 4)
        re_diff = re - {EFrdEntities.DISP, EFrdEntities.STRESS, EFrdEntities.ERROR, EFrdEntities.FORC}
        self.assertEqual(len(re_diff), 0)

        # there are 467 nodes in the frd. Check if every result set has 467 values
        for rs in frd_result.result_sets:
            self.assertEqual(len(rs.values), 467)

        # check component names of each result set
        for rs in frd_result.result_sets:
            if rs.entity == EFrdEntities.DISP:
                self.assertEqual(rs.component_names, ('D1','D2','D3'))
                self.assertEqual(rs.no_components, 3)
            if rs.entity == EFrdEntities.FORC:
                self.assertEqual(rs.component_names, ('F1','F2','F3'))
                self.assertEqual(rs.no_components, 3)
            if rs.entity == EFrdEntities.STRESS:
                self.assertEqual(rs.component_names, ('SXX','SYY','SZZ','SXY','SYZ','SZX'))
                self.assertEqual(rs.no_components, 6)
            if rs.entity == EFrdEntities.ERROR:
                self.assertEqual(rs.component_names, ('STR(%)',))
                self.assertEqual(rs.no_components, 1)

            # check if every value in values has a length of no_components
            for value in rs.values.values():
                self.assertEqual(len(value), rs.no_components)

    def test_get_result_sets_by_entity(self):
        frd_result = FrdResult.from_file(os.path.join(self.test_data_path, 'beam.frd'))
        disp_sets = frd_result.get_result_sets_by_entity(EFrdEntities.DISP)
        self.assertEqual(len(disp_sets), 3)

        # check if all sets are DISP
        re = {rs.entity for rs in disp_sets}
        self.assertEqual(len(re), 1)
        self.assertEqual(re.pop(), EFrdEntities.DISP)

        # test with entity not in result
        sets = frd_result.get_result_sets_by_entity(EFrdEntities.PE)
        self.assertEqual(len(sets), 0)

    def test_get_result_set_by_entity_and_time(self):

        frd_result = FrdResult.from_file(os.path.join(self.test_data_path, 'beam.frd'))
        disp_034 = frd_result.get_result_set_by_entity_and_time(EFrdEntities.DISP, 0.34)
        self.assertEqual(disp_034.entity, EFrdEntities.DISP) # type: ignore
        self.assertAlmostEqual(disp_034.step_time, 0.34) # type: ignore

        # time 0.5 should return result set for timwe 0.34 because its closest
        disp_034 = frd_result.get_result_set_by_entity_and_time(EFrdEntities.DISP, 0.5)
        self.assertEqual(disp_034.entity, EFrdEntities.DISP) # type: ignore
        self.assertAlmostEqual(disp_034.step_time, 0.34) # type: ignore

        # time 0 should return the first result set for timwe 0.34 because its closest
        disp_034 = frd_result.get_result_set_by_entity_and_time(EFrdEntities.DISP, 0)
        self.assertEqual(disp_034.entity, EFrdEntities.DISP) # type: ignore
        self.assertAlmostEqual(disp_034.step_time, 0.34) # type: ignore

        # time 100 should return the last result set for timwe 1.0 because its closest
        disp_1 = frd_result.get_result_set_by_entity_and_time(EFrdEntities.DISP, 100)
        self.assertEqual(disp_1.entity, EFrdEntities.DISP) # type: ignore
        self.assertAlmostEqual(disp_1.step_time, 1) # type: ignore

        # test with entity not in result
        res = frd_result.get_result_set_by_entity_and_time(EFrdEntities.PE, 0.34)
        self.assertIsNone(res)

    def test_get_result_set_by_entity_and_index(self):

        frd_result = FrdResult.from_file(os.path.join(self.test_data_path, 'beam.frd'))
        disp_0 = frd_result.get_result_set_by_entity_and_index(EFrdEntities.DISP, 0)
        self.assertEqual(disp_0.entity, EFrdEntities.DISP) # type: ignore
        self.assertAlmostEqual(disp_0.step_time, 0.34) # type: ignore

        disp_1 = frd_result.get_result_set_by_entity_and_index(EFrdEntities.DISP, 1)
        self.assertEqual(disp_1.entity, EFrdEntities.DISP) # type: ignore
        self.assertAlmostEqual(disp_1.step_time, 0.68) # type: ignore

        disp_2 = frd_result.get_result_set_by_entity_and_index(EFrdEntities.DISP, 2)
        self.assertEqual(disp_0.entity, EFrdEntities.DISP) # type: ignore
        self.assertAlmostEqual(disp_2.step_time, 1) # type: ignore

        disp_last = frd_result.get_result_set_by_entity_and_index(EFrdEntities.DISP, -1)
        self.assertEqual(disp_last.entity, EFrdEntities.DISP) # type: ignore
        self.assertAlmostEqual(disp_last.step_time, 1) # type: ignore

        # test with entity not in result
        res = frd_result.get_result_set_by_entity_and_index(EFrdEntities.PE, 0)
        self.assertIsNone(res)

