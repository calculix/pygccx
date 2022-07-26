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

from pygccx.step_keywords import TimePoints
from pygccx.protocols import IKeyword

import numpy as np

class TestTimePoints(TestCase):

    def test_is_IKeyword(self):
        tp = TimePoints('TP1', [1,2,3])
        self.assertTrue(isinstance(tp, IKeyword))

    def test_default(self):
        tp = TimePoints('TP1', [1,2,3])
        known = '*TIME POINTS,NAME=TP1\n'
        known += '1.0000000e+00,\n2.0000000e+00,\n3.0000000e+00\n'
        self.assertEqual(str(tp), known)

    def test_range(self):
        tp = TimePoints('TP1', range(1,4))
        known = '*TIME POINTS,NAME=TP1\n'
        known += '1.0000000e+00,\n2.0000000e+00,\n3.0000000e+00\n'
        self.assertEqual(str(tp), known)

    def test_nparray(self):
        tp = TimePoints('TP1', np.linspace(0.2, 1, 5, endpoint=True))
        known = '*TIME POINTS,NAME=TP1\n'
        known += '2.0000000e-01,\n4.0000000e-01,\n6.0000000e-01,\n8.0000000e-01,\n1.0000000e+00\n'
        self.assertEqual(str(tp), known)

    def test_total_time(self):
        tp = TimePoints('TP1', [1,2,3], use_total_time=True)
        known = '*TIME POINTS,NAME=TP1,TIME=TOTAL TIME\n'
        known += '1.0000000e+00,\n2.0000000e+00,\n3.0000000e+00\n'
        self.assertEqual(str(tp), known)