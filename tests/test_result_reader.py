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
from tests.tests_result_reader.test_frd_result import (TestFrdResult, Test_beam_buckling_frd,
                                                       Test_beam_buckling_perturbation_frd,
                                                       Test_beam_modal_frd,
                                                       Test_beam_modal_perturbation_frd)
from tests.tests_result_reader.test_dat_result import (TestDatResult, Test_achtel2_dat_ref, 
                                                       Test_beam8f_dat_ref, Test_segmenttestsms_dat_ref,
                                                       Test_beam8b_dat_ref)


if __name__ == '__main__':
    unittest.main()