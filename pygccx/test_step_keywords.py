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
from step_keywords.test.test_boundary import TestBoundary
from step_keywords.test.test_step import TestStep
from step_keywords.test.test_static import TestStatic
from step_keywords.test.test_cload import TestCload
from step_keywords.test.test_time_points import TestTimePoints
from step_keywords.test.test_contact_file import TestContactFile
from step_keywords.test.test_node_file import TestNodeFile
from step_keywords.test.test_el_file import TestElFile


if __name__ == '__main__':
    unittest.main()