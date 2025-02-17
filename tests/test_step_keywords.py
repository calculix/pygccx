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
from tests.tests_step_keywords.test_boundary import TestBoundary
from tests.tests_step_keywords.test_step import TestStep
from tests.tests_step_keywords.test_static import TestStatic
from tests.tests_step_keywords.test_cload import TestCload
from tests.tests_step_keywords.test_time_points import TestTimePoints
from tests.tests_step_keywords.test_contact_file import TestContactFile
from tests.tests_step_keywords.test_contact_print import TestContactPrint
from tests.tests_step_keywords.test_node_file import TestNodeFile
from tests.tests_step_keywords.test_node_print import TestNodePrint
from tests.tests_step_keywords.test_el_file import TestElFile
from tests.tests_step_keywords.test_el_print import TestElPrint
from tests.tests_step_keywords.test_green import TestGreen
from tests.tests_step_keywords.test_no_analysis import TestNoAnalysis
from tests.tests_step_keywords.test_visco import TestVisco
from tests.tests_step_keywords.test_buckle import TestBuckle
from tests.tests_step_keywords.test_frequency import TestFrequency


if __name__ == '__main__':
    unittest.main()