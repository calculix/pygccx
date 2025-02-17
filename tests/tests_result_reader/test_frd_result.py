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
from pygccx.enums import EFrdEntities, EFrdAnalysisTypes
from pygccx.result_reader import FrdResult

class TestFrdResult(TestCase):

    def setUp(self) -> None:
        test_data_path = os.path.dirname(os.path.abspath(__file__))
        self.test_data_path = os.path.join(test_data_path, 'test_data')


    def test_from_file(self):
        frd_result = FrdResult.from_file(os.path.join(self.test_data_path, 'beam.frd'))

        # the frd contains 1 step with 3 times 0.34, 0.68, 1.0
        times = sorted({rs.step_time for rs in frd_result.result_sets})
        self.assertEqual(len(times), 3)
        self.assertEqual(times[0], 0.34)
        self.assertEqual(times[1], 0.68)
        self.assertEqual(times[2], 1.0)

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

    # def test_get_result_set_by_entity_and_index(self):

    #     frd_result = FrdResult.from_file(os.path.join(self.test_data_path, 'beam.frd'))
    #     disp_0 = frd_result.get_result_set_by_entity_and_index(EFrdEntities.DISP, 0)
    #     self.assertEqual(disp_0.entity, EFrdEntities.DISP) # type: ignore
    #     self.assertAlmostEqual(disp_0.step_time, 0.34) # type: ignore

    #     disp_1 = frd_result.get_result_set_by_entity_and_index(EFrdEntities.DISP, 1)
    #     self.assertEqual(disp_1.entity, EFrdEntities.DISP) # type: ignore
    #     self.assertAlmostEqual(disp_1.step_time, 0.68) # type: ignore

    #     disp_2 = frd_result.get_result_set_by_entity_and_index(EFrdEntities.DISP, 2)
    #     self.assertEqual(disp_0.entity, EFrdEntities.DISP) # type: ignore
    #     self.assertAlmostEqual(disp_2.step_time, 1) # type: ignore

    #     disp_last = frd_result.get_result_set_by_entity_and_index(EFrdEntities.DISP, -1)
    #     self.assertEqual(disp_last.entity, EFrdEntities.DISP) # type: ignore
    #     self.assertAlmostEqual(disp_last.step_time, 1) # type: ignore

    #     # test with entity not in result
    #     res = frd_result.get_result_set_by_entity_and_index(EFrdEntities.PE, 0)
    #     self.assertIsNone(res)

class Test_beam_buckling_frd(TestCase):
    def setUp(self):
        test_data_path = os.path.dirname(os.path.abspath(__file__))
        self.test_data_path = os.path.join(test_data_path, 'test_data')
        self.frd_result = FrdResult.from_file(os.path.join(self.test_data_path, 'beam_buckling.frd'))

    def test_metadata(self):
        fr = self.frd_result
        # There must be 6 result sets for 1 Step.
        # Disp, Stress and Error for static and buckling step.
        self.assertEqual(len(fr.result_sets), 6)
        self.assertEqual(len(fr.get_result_sets_by(entity=EFrdEntities.DISP)), 2)
        self.assertEqual(len(fr.get_result_sets_by(entity=EFrdEntities.STRESS)), 2)
        self.assertEqual(len(fr.get_result_sets_by(entity=EFrdEntities.ERROR)), 2)

        # All result sets belongs to step 1
        for rs in fr.result_sets: self.assertEqual(rs.step_no, 1)
        
        # All results have an analysis type of USER_NAMED
        for rs in fr.result_sets: self.assertEqual(rs.analysis_type, EFrdAnalysisTypes.USER_NAMED)

        # The frd contains only one buckle step with one requested mode.
        # In this case there is no static perturbation step before and the static analysis is 
        # part of the buckle step. The results of the static analysis have the step_inc_no 1.
        # The results of the first buckling mode have the step_inc_no 2
        self.assertEqual(len(fr.get_result_sets_by(step_inc_no=1)), 3)
        self.assertEqual(len(fr.get_result_sets_by(step_inc_no=2)), 3)

        # Each result must have 4403 nodal values
        for rs in fr.result_sets:
            self.assertEqual(len(rs.values), 4403)

        # Each DISP result nust have 3 components
        for rs in fr.get_result_sets_by(entity=EFrdEntities.DISP):
            self.assertEqual(len(rs.component_names), 3)
        # Each STRESS result nust have 6 components
        for rs in fr.get_result_sets_by(entity=EFrdEntities.STRESS):
            self.assertEqual(len(rs.component_names), 6)
        # Each ERROR result nust have 1 components
        for rs in fr.get_result_sets_by(entity=EFrdEntities.ERROR):
            self.assertEqual(len(rs.component_names), 1)

    def test_values(self):
        fr = self.frd_result

        # Check a random node value for each result set
        # DISP Step 1, Step_inc 1
        #-1       172-2.06959E-02-1.42820E-03 1.42762E-03
        values = fr.get_result_sets_by(step_inc_no=1, entity=EFrdEntities.DISP)[0].get_values_by_ids([172])[0]
        values_known = -2.06959E-02, -1.42820E-03, 1.42762E-03
        for i in range(len(values_known)):
            self.assertEqual(values[i], values_known[i])
        
        # DISP Step 1, Step_inc 2
        # -1       114-2.18448E-03 6.89212E-04-1.18930E-02
        values = fr.get_result_sets_by(step_inc_no=2, entity=EFrdEntities.DISP)[0].get_values_by_ids([114])[0]
        values_known = -2.18448E-03, 6.89212E-04, -1.18930E-02
        for i in range(len(values_known)):
            self.assertEqual(values[i], values_known[i])

        # Check a random node value for each result set
        # STRESS Step 1, Step_inc 1
        #-1       192-1.99998E+02-1.12034E-12-6.33167E-14 2.36271E-12 4.15932E-12 1.28101E-12
        values = fr.get_result_sets_by(step_inc_no=1, entity=EFrdEntities.STRESS)[0].get_values_by_ids([192])[0]
        values_known = -1.99998E+02,-1.12034E-12,-6.33167E-14, 2.36271E-12, 4.15932E-12, 1.28101E-12
        for i in range(len(values_known)):
            self.assertEqual(values[i], values_known[i])
        
        # STRESS Step 1, Step_inc 2
        # -1       253-6.49997E+00 6.10236E-03 6.39582E-03-1.90903E-02 5.80363E-04-3.58040E-02
        values = fr.get_result_sets_by(step_inc_no=2, entity=EFrdEntities.STRESS)[0].get_values_by_ids([253])[0]
        values_known = -6.49997E+00, 6.10236E-03, 6.39582E-03,-1.90903E-02, 5.80363E-04,-3.58040E-02
        for i in range(len(values_known)):
            self.assertEqual(values[i], values_known[i])

        # Check a random node value for each result set
        # ERROR Step 1, Step_inc 1
        #-1       337 3.52968E+00
        values = fr.get_result_sets_by(step_inc_no=1, entity=EFrdEntities.ERROR)[0].get_values_by_ids([337])[0,0]
        values_known = 3.52968E+00
        self.assertEqual(values, values_known)
        
        # STRESS Step 1, Step_inc 2
        # -1        95 8.91982E+00
        values = fr.get_result_sets_by(step_inc_no=2, entity=EFrdEntities.ERROR)[0].get_values_by_ids([95])[0,0]
        values_known = 8.91982E+00
        self.assertEqual(values, values_known)

class Test_beam_buckling_perturbation_frd(TestCase):
    def setUp(self):
        test_data_path = os.path.dirname(os.path.abspath(__file__))
        self.test_data_path = os.path.join(test_data_path, 'test_data')
        self.frd_result = FrdResult.from_file(os.path.join(self.test_data_path, 'beam_buckling_perturbation.frd'))

    def test_metadata(self):
        fr = self.frd_result
        # There must be 9 result sets for 2 Step.
        # Disp, Stress and Error for static and buckling step.
        self.assertEqual(len(fr.result_sets), 9)
        self.assertEqual(len(fr.get_result_sets_by(entity=EFrdEntities.DISP)), 3)
        self.assertEqual(len(fr.get_result_sets_by(entity=EFrdEntities.STRESS)), 3)
        self.assertEqual(len(fr.get_result_sets_by(entity=EFrdEntities.ERROR)), 3)

        # Step 1 (static) has 3 result sets
        self.assertEqual(len(fr.get_result_sets_by(step_no=1)), 3)
        # Step 2 (frequency) has 2 modes with 3 result sets each
        self.assertEqual(len(fr.get_result_sets_by(step_no=2)), 6)
        
        # All results in step 1 have an analysis type of STATIC
        for rs in fr.get_result_sets_by(step_no=1): 
            self.assertEqual(rs.analysis_type, EFrdAnalysisTypes.STATIC)

        # All results in step 2 have an analysis type of USER_NAMED
        for rs in fr.get_result_sets_by(step_no=2): 
            self.assertEqual(rs.analysis_type, EFrdAnalysisTypes.USER_NAMED)

        # Each result must have 4403 nodal values
        for rs in fr.result_sets:
            self.assertEqual(len(rs.values), 4403)

        # Each DISP result nust have 3 components
        for rs in fr.get_result_sets_by(entity=EFrdEntities.DISP):
            self.assertEqual(len(rs.component_names), 3)
        # Each STRESS result nust have 6 components
        for rs in fr.get_result_sets_by(entity=EFrdEntities.STRESS):
            self.assertEqual(len(rs.component_names), 6)
        # Each ERROR result nust have 1 components
        for rs in fr.get_result_sets_by(entity=EFrdEntities.ERROR):
            self.assertEqual(len(rs.component_names), 1)

    def test_values(self):
        fr = self.frd_result

        # Check a random node value for each result set
        # DISP Step 1, Step_inc 1
        #-1       83 2.28714E-01 1.45175E+00 3.78935E-03
        values = fr.get_result_sets_by(step_no=1, step_inc_no=1, entity=EFrdEntities.DISP)[0].get_values_by_ids([83])[0]
        values_known = 2.28714E-01, 1.45175E+00, 3.78935E-03
        for i in range(len(values_known)):
            self.assertEqual(values[i], values_known[i])

        # DISP Step 2, Step_inc 1
        #-1       172 2.39676E-02 1.02587E-01-1.61009E-03
        values = fr.get_result_sets_by(step_no=2, step_inc_no=1, entity=EFrdEntities.DISP)[0].get_values_by_ids([172])[0]
        values_known = 2.39676E-02, 1.02587E-01, -1.61009E-03
        for i in range(len(values_known)):
            self.assertEqual(values[i], values_known[i])
        
        # DISP Step 2, Step_inc 2
        # -1       114-2.55465E-03-1.46353E-03-1.19897E-02
        values = fr.get_result_sets_by(step_no=2, step_inc_no=2, entity=EFrdEntities.DISP)[0].get_values_by_ids([114])[0]
        values_known = -2.55465E-03, -1.46353E-03, -1.19897E-02
        for i in range(len(values_known)):
            self.assertEqual(values[i], values_known[i])

        # Check a random node value for each result set
        # STRESS Step 1, Step_inc 1
        #-1       157 2.81829E+02 9.78665E-02 2.80542E-01 2.21946E+00 6.28556E-02 1.52367E+00
        values = fr.get_result_sets_by(step_no=1, step_inc_no=1, entity=EFrdEntities.STRESS)[0].get_values_by_ids([157])[0]
        values_known = 2.81829E+02, 9.78665E-02, 2.80542E-01, 2.21946E+00, 6.28556E-02, 1.52367E+00
        for i in range(len(values_known)):
            self.assertEqual(values[i], values_known[i])

        # Check a random node value for each result set
        # STRESS Step 2, Step_inc 1
        #-1       192-7.00133E+01-2.92905E-01-2.24079E-01 1.73740E+00-8.83492E-02 9.36157E-01
        values = fr.get_result_sets_by(step_no=2, step_inc_no=1, entity=EFrdEntities.STRESS)[0].get_values_by_ids([192])[0]
        values_known = -7.00133E+01, -2.92905E-01, -2.24079E-01, 1.73740E+00, -8.83492E-02, 9.36157E-01
        for i in range(len(values_known)):
            self.assertEqual(values[i], values_known[i])
        
        # STRESS Step 2, Step_inc 2
        # -1       253-4.57625E+00 7.54065E-01 4.60463E-01-1.03301E-01 1.21146E+00-4.67845E-02
        values = fr.get_result_sets_by(step_no=2, step_inc_no=2, entity=EFrdEntities.STRESS)[0].get_values_by_ids([253])[0]
        values_known = -4.57625E+00, 7.54065E-01, 4.60463E-01, -1.03301E-01, 1.21146E+00, -4.67845E-02
        for i in range(len(values_known)):
            self.assertEqual(values[i], values_known[i])

        # Check a random node value for each result set
        # ERROR Step 1, Step_inc 1
        #-1       1 1.20350E+01
        values = fr.get_result_sets_by(step_no=1, step_inc_no=1, entity=EFrdEntities.ERROR)[0].get_values_by_ids([1])[0,0]
        values_known = 1.20350E+01
        self.assertEqual(values, values_known)

        # Check a random node value for each result set
        # ERROR Step 2, Step_inc 1
        #-1       337 3.20448E+01
        values = fr.get_result_sets_by(step_no=2, step_inc_no=1, entity=EFrdEntities.ERROR)[0].get_values_by_ids([337])[0,0]
        values_known = 3.20448E+01
        self.assertEqual(values, values_known)
        
        # STRESS Step 2, Step_inc 2
        # -1        95 4.34566E-01
        values = fr.get_result_sets_by(step_no=2, step_inc_no=2, entity=EFrdEntities.ERROR)[0].get_values_by_ids([95])[0,0]
        values_known = 4.34566E-01
        self.assertEqual(values, values_known)

class Test_beam_modal_frd(TestCase):
    def setUp(self):
        test_data_path = os.path.dirname(os.path.abspath(__file__))
        self.test_data_path = os.path.join(test_data_path, 'test_data')
        self.frd_result = FrdResult.from_file(os.path.join(self.test_data_path, 'beam_modal.frd'))

    def test_metadata(self):
        fr = self.frd_result
        # There must be 6 result sets for 2 Step.
        # Disp, Stress and Error.
        self.assertEqual(len(fr.result_sets), 6)
        self.assertEqual(len(fr.get_result_sets_by(entity=EFrdEntities.DISP)), 2)
        self.assertEqual(len(fr.get_result_sets_by(entity=EFrdEntities.STRESS)), 2)
        self.assertEqual(len(fr.get_result_sets_by(entity=EFrdEntities.ERROR)), 2)

        # All result sets belongs to step 1
        for rs in fr.result_sets: self.assertEqual(rs.step_no, 1)
        
        # All results have an analysis type of FREQUENCY
        for rs in fr.result_sets: self.assertEqual(rs.analysis_type, EFrdAnalysisTypes.FREQUENCY)

        # Each result must have 4403 nodal values
        for rs in fr.result_sets:
            self.assertEqual(len(rs.values), 4403)

        # Each DISP result nust have 3 components
        for rs in fr.get_result_sets_by(entity=EFrdEntities.DISP):
            self.assertEqual(len(rs.component_names), 3)
        # Each STRESS result nust have 6 components
        for rs in fr.get_result_sets_by(entity=EFrdEntities.STRESS):
            self.assertEqual(len(rs.component_names), 6)
        # Each ERROR result nust have 1 components
        for rs in fr.get_result_sets_by(entity=EFrdEntities.ERROR):
            self.assertEqual(len(rs.component_names), 1)

    def test_values(self):
        fr = self.frd_result

        # Check a random node value for each result set
        # DISP Step 1, Step_inc 1
        #-1       172-5.94785E+00 2.62888E+00 1.71817E+01
        values = fr.get_result_sets_by(step_inc_no=1, entity=EFrdEntities.DISP)[0].get_values_by_ids([172])[0]
        values_known = -5.94785E+00, 2.62888E+00, 1.71817E+01
        for i in range(len(values_known)):
            self.assertEqual(values[i], values_known[i])
        
        # DISP Step 1, Step_inc 2
        # -1       114 1.04094E+01 7.19394E+01-1.24641E+01
        values = fr.get_result_sets_by(step_inc_no=2, entity=EFrdEntities.DISP)[0].get_values_by_ids([114])[0]
        values_known = 1.04094E+01, 7.19394E+01,-1.24641E+01
        for i in range(len(values_known)):
            self.assertEqual(values[i], values_known[i])

        # Check a random node value for each result set
        # STRESS Step 1, Step_inc 1
        #-1       192-3.94634E+03 8.08807E+00 1.63520E+01 9.11063E+01 1.14928E+01 1.39143E+02
        values = fr.get_result_sets_by(step_inc_no=1, entity=EFrdEntities.STRESS)[0].get_values_by_ids([192])[0]
        values_known = -3.94634E+03, 8.08807E+00, 1.63520E+01, 9.11063E+01, 1.14928E+01, 1.39143E+02
        for i in range(len(values_known)):
            self.assertEqual(values[i], values_known[i])
        
        # STRESS Step 1, Step_inc 2
        # -1       253-1.90615E+04 3.60686E+01 3.16017E+01 1.76765E+02 6.84544E+00 7.91043E+01
        values = fr.get_result_sets_by(step_inc_no=2, entity=EFrdEntities.STRESS)[0].get_values_by_ids([253])[0]
        values_known = -1.90615E+04, 3.60686E+01, 3.16017E+01, 1.76765E+02, 6.84544E+00, 7.91043E+01
        for i in range(len(values_known)):
            self.assertEqual(values[i], values_known[i])

        # Check a random node value for each result set
        # ERROR Step 1, Step_inc 1
        #-1       337 3.56969E+01
        values = fr.get_result_sets_by(step_inc_no=1, entity=EFrdEntities.ERROR)[0].get_values_by_ids([337])[0,0]
        values_known = 3.56969E+01
        self.assertEqual(values, values_known)
        
        # STRESS Step 1, Step_inc 2
        # -1        95 9.85539E+00
        values = fr.get_result_sets_by(step_inc_no=2, entity=EFrdEntities.ERROR)[0].get_values_by_ids([95])[0,0]
        values_known = 9.85539E+00
        self.assertEqual(values, values_known)

class Test_beam_modal_perturbation_frd(TestCase):
    def setUp(self):
        test_data_path = os.path.dirname(os.path.abspath(__file__))
        self.test_data_path = os.path.join(test_data_path, 'test_data')
        self.frd_result = FrdResult.from_file(os.path.join(self.test_data_path, 'beam_modal_perturbation.frd'))

    def test_metadata(self):
        fr = self.frd_result
        # There must be 9 result sets for 3 Step.
        # Disp, Stress and Error.
        self.assertEqual(len(fr.result_sets), 9)
        self.assertEqual(len(fr.get_result_sets_by(entity=EFrdEntities.DISP)), 3)
        self.assertEqual(len(fr.get_result_sets_by(entity=EFrdEntities.STRESS)), 3)
        self.assertEqual(len(fr.get_result_sets_by(entity=EFrdEntities.ERROR)), 3)

        # Step 1 (static) has 3 result sets
        self.assertEqual(len(fr.get_result_sets_by(step_no=1)), 3)
        # Step 2 (frequency) has 2 modes with 3 result sets each
        self.assertEqual(len(fr.get_result_sets_by(step_no=2)), 6)
        
        # All results in step 1 have an analysis type of STATIC
        for rs in fr.get_result_sets_by(step_no=1): 
            self.assertEqual(rs.analysis_type, EFrdAnalysisTypes.STATIC)

        # All results in step 2 have an analysis type of FREQUENCY
        for rs in fr.get_result_sets_by(step_no=2): 
            self.assertEqual(rs.analysis_type, EFrdAnalysisTypes.FREQUENCY)

        # Each result must have 4403 nodal values
        for rs in fr.result_sets:
            self.assertEqual(len(rs.values), 4403)

        # Each DISP result nust have 3 components
        for rs in fr.get_result_sets_by(entity=EFrdEntities.DISP):
            self.assertEqual(len(rs.component_names), 3)
        # Each STRESS result nust have 6 components
        for rs in fr.get_result_sets_by(entity=EFrdEntities.STRESS):
            self.assertEqual(len(rs.component_names), 6)
        # Each ERROR result nust have 1 components
        for rs in fr.get_result_sets_by(entity=EFrdEntities.ERROR):
            self.assertEqual(len(rs.component_names), 1)

    def test_values(self):
        fr = self.frd_result

        # Check a random node value for each result set
        # DISP Step 1, Step_inc 1
        #-1       83 5.29094E-02 1.42543E-03 1.43112E-03
        values = fr.get_result_sets_by(step_no=1, step_inc_no=1, entity=EFrdEntities.DISP)[0].get_values_by_ids([83])[0]
        values_known = 5.29094E-02, 1.42543E-03, 1.43112E-03
        for i in range(len(values_known)):
            self.assertEqual(values[i], values_known[i])

        # DISP Step 2, Step_inc 1
        #-1       172-4.12069E+00 6.92609E+00 1.72399E+01
        values = fr.get_result_sets_by(step_no=2, step_inc_no=1, entity=EFrdEntities.DISP)[0].get_values_by_ids([172])[0]
        values_known = -4.12069E+00, 6.92609E+00, 1.72399E+01
        for i in range(len(values_known)):
            self.assertEqual(values[i], values_known[i])
        
        # DISP Step 2, Step_inc 2
        # -1       114 6.84316E+00 6.98345E+01-2.91976E+01
        values = fr.get_result_sets_by(step_no=2, step_inc_no=2, entity=EFrdEntities.DISP)[0].get_values_by_ids([114])[0]
        values_known = 6.84316E+00, 6.98345E+01, -2.91976E+01
        for i in range(len(values_known)):
            self.assertEqual(values[i], values_known[i])

        # Check a random node value for each result set
        # STRESS Step 1, Step_inc 1
        #-1       157 1.99998E+02-3.22024E-12 2.89129E-12-3.66661E-12 2.37198E-12 6.66489E-13
        values = fr.get_result_sets_by(step_no=1, step_inc_no=1, entity=EFrdEntities.STRESS)[0].get_values_by_ids([157])[0]
        values_known = 1.99998E+02, -3.22024E-12, 2.89129E-12, -3.66661E-12, 2.37198E-12, 6.66489E-13
        for i in range(len(values_known)):
            self.assertEqual(values[i], values_known[i])

        # Check a random node value for each result set
        # STRESS Step 2, Step_inc 1
        #-1       192-1.16013E+02 7.27080E-01 1.20767E+01 7.71411E+01 1.01233E+01 1.00587E+02
        values = fr.get_result_sets_by(step_no=2, step_inc_no=1, entity=EFrdEntities.STRESS)[0].get_values_by_ids([192])[0]
        values_known = -1.16013E+02, 7.27080E-01, 1.20767E+01, 7.71411E+01, 1.01233E+01, 1.00587E+02
        for i in range(len(values_known)):
            self.assertEqual(values[i], values_known[i])
        
        # STRESS Step 2, Step_inc 2
        # -1       253-1.36436E+04 4.71766E+01 4.45336E+01 1.37502E+02 8.46567E+00 2.99473E+01
        values = fr.get_result_sets_by(step_no=2, step_inc_no=2, entity=EFrdEntities.STRESS)[0].get_values_by_ids([253])[0]
        values_known = -1.36436E+04, 4.71766E+01, 4.45336E+01, 1.37502E+02, 8.46567E+00, 2.99473E+01
        for i in range(len(values_known)):
            self.assertEqual(values[i], values_known[i])

        # Check a random node value for each result set
        # ERROR Step 1, Step_inc 1
        #-1       1 1.09158E+01
        values = fr.get_result_sets_by(step_no=1, step_inc_no=1, entity=EFrdEntities.ERROR)[0].get_values_by_ids([1])[0,0]
        values_known = 1.09158E+01
        self.assertEqual(values, values_known)

        # Check a random node value for each result set
        # ERROR Step 2, Step_inc 1
        #-1       337 3.24010E+01
        values = fr.get_result_sets_by(step_no=2, step_inc_no=1, entity=EFrdEntities.ERROR)[0].get_values_by_ids([337])[0,0]
        values_known = 3.24010E+01
        self.assertEqual(values, values_known)
        
        # STRESS Step 2, Step_inc 2
        # -1        95 2.06129E+01
        values = fr.get_result_sets_by(step_no=2, step_inc_no=2, entity=EFrdEntities.ERROR)[0].get_values_by_ids([95])[0,0]
        values_known = 2.06129E+01
        self.assertEqual(values, values_known)