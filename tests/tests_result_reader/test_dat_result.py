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
from pygccx.result_reader import DatResult
from pygccx import enums

import numpy as np

class TestDatResult(TestCase):

    def setUp(self) -> None:
        test_data_path = os.path.dirname(os.path.abspath(__file__))
        self.test_data_path = os.path.join(test_data_path, 'test_data')


    def test_from_file(self):
        dat_result = DatResult.from_file(os.path.join(self.test_data_path, 'beam.dat'))

        # the dat contains 1 step with 3 times 0.34, 0.68, 1.0
        times = dat_result.get_available_times()
        self.assertEqual(len(times), 3)
        self.assertEqual(times[0], 0.34)
        self.assertEqual(times[1], 0.68)
        self.assertEqual(times[2], 1.0)

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
        disp_sets = dat_result.get_result_sets_by(entity=EDatEntities.U)
        self.assertEqual(len(disp_sets), 3)

        # check if all sets are U
        re = {rs.entity for rs in disp_sets}
        self.assertEqual(len(re), 1)
        self.assertEqual(re.pop(), EDatEntities.U)

        # test with entity not in result
        sets = dat_result.get_result_sets_by(entity=EDatEntities.CDIS)
        self.assertEqual(len(sets), 0)

    def test_get_result_sets_by_entity_and_time(self):

        dat_result = DatResult.from_file(os.path.join(self.test_data_path, 'beam.dat'))
        disp_034 = dat_result.get_result_sets_by(entity=EDatEntities.U, step_time=0.34)
        self.assertEqual(len(disp_034),1)
        self.assertEqual(disp_034[0].entity, EDatEntities.U) # type: ignore
        self.assertAlmostEqual(disp_034[0].step_time, 0.34) # type: ignore

        # time 0.5 should return result set for timwe 0.34 because its closest
        disp_034 = dat_result.get_result_sets_by(entity=EDatEntities.U, step_time=0.5)
        self.assertEqual(len(disp_034),1)
        self.assertEqual(disp_034[0].entity, EDatEntities.U) # type: ignore
        self.assertAlmostEqual(disp_034[0].step_time, 0.34) # type: ignore

        # time 0 should return the first result set for timwe 0.34 because its closest
        disp_034 = dat_result.get_result_sets_by(entity=EDatEntities.U, step_time=0)
        self.assertEqual(len(disp_034),1)
        self.assertEqual(disp_034[0].entity, EDatEntities.U) # type: ignore
        self.assertAlmostEqual(disp_034[0].step_time, 0.34) # type: ignore

        # time 100 should return the last result set for timwe 1.0 because its closest
        disp_1 = dat_result.get_result_sets_by(entity=EDatEntities.U, step_time=100)
        self.assertEqual(len(disp_1),1)
        self.assertEqual(disp_1[0].entity, EDatEntities.U) # type: ignore
        self.assertAlmostEqual(disp_1[0].step_time, 1) # type: ignore

        # test with entity not in result
        res = dat_result.get_result_sets_by(entity=EDatEntities.CDIS, step_time=0.34)
        self.assertEqual(len(res),0)

    def test_get_result_sets_by_entity_and_index(self):

        #Test get by entity and index
        dat_result = DatResult.from_file(os.path.join(self.test_data_path, 'beam.dat'))
        disp_0 = dat_result.get_result_sets_by(entity=EDatEntities.U)[0]
        self.assertEqual(disp_0.entity, EDatEntities.U) # type: ignore
        self.assertAlmostEqual(disp_0.step_time, 0.34) # type: ignore

        disp_1 = dat_result.get_result_sets_by(entity=EDatEntities.U)[1]
        self.assertEqual(disp_1.entity, EDatEntities.U) # type: ignore
        self.assertAlmostEqual(disp_1.step_time, 0.68) # type: ignore

        disp_2 = dat_result.get_result_sets_by(entity=EDatEntities.U)[2]
        self.assertEqual(disp_0.entity, EDatEntities.U) # type: ignore
        self.assertAlmostEqual(disp_2.step_time, 1) # type: ignore

        disp_last = dat_result.get_result_sets_by(entity=EDatEntities.U)[-1]
        self.assertEqual(disp_last.entity, EDatEntities.U) # type: ignore
        self.assertAlmostEqual(disp_last.step_time, 1) # type: ignore

        # test with entity not in result
        res = dat_result.get_result_sets_by(entity=EDatEntities.CDIS)
        self.assertEqual(len(res),0)

    def test_get_result_set_by_entity_and_index_same_ent_same_time_diff_setnames(self):
        dat_result = DatResult.from_file(
            os.path.join(self.test_data_path, 'same_ent_same_time_diff_setnames.dat')
        )

        # no set name specified. Should return result for set "SET1" and "SET2". "SET1" is at index 0
        disp = dat_result.get_result_sets_by(entity=EDatEntities.U)[0]
        self.assertEqual(disp.set_name, 'SET1') # type: ignore

        # no set name specified. Should return result for set "SET1" and "SET2". "SET1" is at index 2
        disp = dat_result.get_result_sets_by(entity=EDatEntities.U)[1]
        self.assertEqual(disp.set_name, 'SET2') # type: ignore

        # set name 'SET1' specified. Should return result for set "SET1"
        disp = dat_result.get_result_sets_by(entity=EDatEntities.U, set_name='SET1')[0]
        self.assertEqual(disp.set_name, 'SET1') # type: ignore

        # set name 'SET2' specified. Should return result for set "SET1"
        disp = dat_result.get_result_sets_by(entity=EDatEntities.U, set_name='SET2')[0]
        self.assertEqual(disp.set_name, 'SET2') # type: ignore

    def test_get_result_set_by_entity_and_time_same_ent_same_time_diff_setnames(self):
        dat_result = DatResult.from_file(
            os.path.join(self.test_data_path, 'same_ent_same_time_diff_setnames.dat')
        )

        # no set name specified. Should return result for set "SET1" and "SET2". "SET1" is at index 0
        disp = dat_result.get_result_sets_by(entity=EDatEntities.U, step_time=1)[0]
        self.assertEqual(disp.set_name, 'SET1') # type: ignore

        # no set name specified. Should return result for set "SET1" and "SET2". "SET1" is at index 0
        disp = dat_result.get_result_sets_by(entity=EDatEntities.U, step_time=1)[1]
        self.assertEqual(disp.set_name, 'SET2') # type: ignore

        # set name 'SET1' specified. Should return result for set "SET1"
        disp = dat_result.get_result_sets_by(entity=EDatEntities.U, step_time=1, set_name='SET1')[0]
        self.assertEqual(disp.set_name, 'SET1') # type: ignore

        # set name 'SET2' specified. Should return result for set "SET1"
        disp = dat_result.get_result_sets_by(entity=EDatEntities.U, step_time=1, set_name='SET2')[0]
        self.assertEqual(disp.set_name, 'SET2') # type: ignore

    def test_step_infos(self):
        dat_result = DatResult.from_file(
            os.path.join(self.test_data_path, 'same_ent_same_time_diff_setnames.dat')
        )
        dr = dat_result
        si = dr.get_step_info(1)

        self.assertIsNone(si)

class Test_achtel2_dat_ref(TestCase):
    def setUp(self) -> None:
        test_data_path = os.path.dirname(os.path.abspath(__file__))
        self.test_data_path = os.path.join(test_data_path, 'test_data')
        self.dat_result = DatResult.from_file(os.path.join(self.test_data_path, 'achtel2.dat.ref'))

    def test_result_sets_meta_data(self):
        dr = self.dat_result
        # test number of result sets. there must be 2. 
        self.assertEqual(len(dr.result_sets), 2)
        # test step number. there is only one static step with one increment and one time
        for rs in dr.result_sets:
            self.assertEqual(rs.step_no, 1)
            self.assertEqual(rs.step_inc_no, 1)
            self.assertEqual(rs.step_time, 1.0)
            self.assertEqual(rs.analysis_type, enums.EDatAnalysisTypes.STATIC)
        # Test entities. There mst be one displacement and one stress result
        self.assertEqual(dr.result_sets[0].entity, enums.EDatEntities.U)
        self.assertEqual(dr.result_sets[1].entity, enums.EDatEntities.S)
        # Test entity location
        self.assertEqual(dr.result_sets[0].entity_location, enums.EResultLocations.NODAL)
        self.assertEqual(dr.result_sets[1].entity_location, enums.EResultLocations.INT_PNT)
        # Both result sets have different names. "SET1" and "SET2"
        self.assertEqual(dr.result_sets[0].set_name, "SET1")
        self.assertEqual(dr.result_sets[1].set_name, "SET2")
        # Test Component names
        self.assertEqual(dr.result_sets[0].component_names, ('vx', 'vy', 'vz'))
        self.assertEqual(dr.result_sets[1].component_names, ('sxx', 'syy', 'szz', 'sxy','sxz','syz'))

    def test_values(self):
        dr = self.dat_result

        # test displ. values for node 1
        # 1  0.000000E+00  0.000000E+00  0.000000E+00
        displ = dr.result_sets[0].get_values_by_ids([1])
        known = np.array([[0.000000E+00,  0.000000E+00,  0.000000E+00]])
        self.assertTrue(np.allclose(displ, known))

        # test displ. values for node 72
        # 72 -1.902397E-04 -2.197600E-04  2.385701E-04
        displ = dr.result_sets[0].get_values_by_ids([72])
        known = np.array([[-1.902397E-04, -2.197600E-04,  2.385701E-04]])
        self.assertTrue(np.allclose(displ, known))

        # test stress values for element 1
        #  1   1 -2.600167E+00 -2.600167E+00  3.625318E+00  3.062590E+00  1.358358E+00  1.358358E+00
        #  1   2 -5.200285E+00  5.231693E+00  3.297180E+00  2.988195E+00 -1.315433E+01  4.019350E+00
        #  1   3  5.231693E+00 -5.200285E+00  3.297180E+00  2.988195E+00  4.019350E+00 -1.315433E+01
        #  1   4 -8.986443E+00 -8.986443E+00  1.153378E+01  1.323712E+01  6.548194E+00  6.548194E+00
        #  1   5 -4.917874E-01 -4.917874E-01  4.084941E+00 -5.691371E-01 -1.728330E+00 -1.728330E+00
        #  1   6  2.701717E+00  4.607920E+00  5.340509E+00 -4.774403E+00  5.357368E+00 -2.796545E+00
        #  1   7  4.607920E+00  2.701717E+00  5.340509E+00 -4.774403E+00 -2.796545E+00  5.357368E+00
        #  1   8  1.170018E+01  1.170018E+01  2.543981E+01 -8.562821E+00  9.692790E+00  9.692790E+00
        stress = dr.result_sets[1].get_values_by_ids([1])
        known = np.array([[[-2.600167E+00, -2.600167E+00,  3.625318E+00,  3.062590E+00,  1.358358E+00,  1.358358E+00],
                          [-5.200285E+00,  5.231693E+00,  3.297180E+00,  2.988195E+00, -1.315433E+01,  4.019350E+00],
                          [ 5.231693E+00, -5.200285E+00,  3.297180E+00,  2.988195E+00,  4.019350E+00, -1.315433E+01],
                          [-8.986443E+00, -8.986443E+00,  1.153378E+01,  1.323712E+01,  6.548194E+00,  6.548194E+00],
                          [-4.917874E-01, -4.917874E-01,  4.084941E+00, -5.691371E-01, -1.728330E+00, -1.728330E+00],
                          [ 2.701717E+00,  4.607920E+00,  5.340509E+00, -4.774403E+00,  5.357368E+00, -2.796545E+00],
                          [ 4.607920E+00,  2.701717E+00,  5.340509E+00, -4.774403E+00, -2.796545E+00,  5.357368E+00],
                          [ 1.170018E+01,  1.170018E+01,  2.543981E+01, -8.562821E+00,  9.692790E+00,  9.692790E+00]]])

        self.assertTrue(np.allclose(stress, known))

    def test_step_infos(self):
        dr = self.dat_result
        si = dr.get_step_info(1)

        self.assertIsNone(si)

class Test_beam8f_dat_ref(TestCase):
    def setUp(self) -> None:
        test_data_path = os.path.dirname(os.path.abspath(__file__))
        self.test_data_path = os.path.join(test_data_path, 'test_data')
        self.dat_result = DatResult.from_file(os.path.join(self.test_data_path, 'beam8f.dat.ref'))

    def test_step_infos(self):
        dr = self.dat_result
        si = dr.get_step_info(1)

        self.assertIsNone(si.axis_reference_direction)

        sii = si.get_increment_infos()
        self.assertEqual(len(sii), 10)

        sii6 = sii[5]
        self.assertEqual(sii6, dr.get_step_info(1).get_increment_infos(6)[0])
        self.assertIsNone(sii6.eigenmode_turning_direction)
        self.assertAlmostEqual(sii6.frequencies.eigen_value, 0.1054103E+13)
        self.assertAlmostEqual(sii6.frequencies.omega_real, 0.1026695E+07)
        self.assertAlmostEqual(sii6.frequencies.freq_real, 0.1634036E+06)
        self.assertAlmostEqual(sii6.frequencies.omega_imag, 0)
        self.assertIsNone(sii6.frequencies.nodal_diameter)
           
        self.assertAlmostEqual(sii6.participation_factors, 
                               (0.4393173E-18, -0.1332534E-18, -0.2739949E-03, 
                                -0.2054962E-03, 0.1369974E-03, -0.6182618E-18))

        self.assertAlmostEqual(sii6.effective_modal_mass, 
                               (0.1929997E-36, 0.1775647E-37, 0.7507320E-07, 
                                0.4222867E-07, 0.1876830E-07, 0.3822477E-36))

class Test_segmenttestsms_dat_ref(TestCase):
    def setUp(self) -> None:
        test_data_path = os.path.dirname(os.path.abspath(__file__))
        self.test_data_path = os.path.join(test_data_path, 'test_data')
        self.dat_result = DatResult.from_file(os.path.join(self.test_data_path, 'segmenttetsms.dat.ref'))

    def test_step_infos(self):
        dr = self.dat_result
        si = dr.get_step_info(1)

        self.assertAlmostEqual(si.total_effective_mass, 
                               (0.1884770E-07, 0.3499534E-07, 0.3499534E-07, 
                                0.7006253E-08, 0.6125889E-08, 0.7031345E-08))
        
        self.assertEqual(si.axis_reference_direction, (1,0,0))

        sii = si.get_increment_infos()
        self.assertEqual(len(sii), 10)
        sii6 = sii[5]
        self.assertEqual(sii6, dr.get_step_info(1).get_increment_infos(6)[0])
        self.assertEqual(sii6.eigenmode_turning_direction.nodal_diameter, 1)
        self.assertEqual(sii6.eigenmode_turning_direction.direction, 'B')
        self.assertAlmostEqual(sii6.frequencies.eigen_value, 0.4981563E+11)
        self.assertAlmostEqual(sii6.frequencies.omega_real, 0.2231942E+06)
        self.assertAlmostEqual(sii6.frequencies.freq_real, 0.3552245E+05)
        self.assertAlmostEqual(sii6.frequencies.omega_imag, 0)
        self.assertEqual(sii6.frequencies.nodal_diameter, 1)
     
        self.assertAlmostEqual(sii6.participation_factors, 
                               (-0.1775378E-04, -0.1157601E-05, 0.2161940E-05, 
                                0.2036489E-06, 0.4371511E-05, -0.9502998E-05))
               
        self.assertAlmostEqual(sii6.effective_modal_mass, 
                               (0.3151967E-09, 0.1340041E-11, 0.4673983E-11, 
                                0.4147286E-13, 0.1911011E-10, 0.9030697E-10))
              
class Test_beam8b_dat_ref(TestCase):
    def setUp(self) -> None:
        test_data_path = os.path.dirname(os.path.abspath(__file__))
        self.test_data_path = os.path.join(test_data_path, 'test_data')
        self.dat_result = DatResult.from_file(os.path.join(self.test_data_path, 'beam8b.dat.ref'))

    def test_step_infos(self):
        dr = self.dat_result
        si = dr.get_step_info(1)

        sii = si.get_increment_infos()
        self.assertEqual(len(sii), 10)
        sii6 = sii[5]
        self.assertEqual(sii6, dr.get_step_info(1).get_increment_infos(6)[0])
        self.assertEqual(sii6.buckling_factor, 0.1751251E+04)


