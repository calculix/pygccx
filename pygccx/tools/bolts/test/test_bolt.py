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

import numpy as np
from pygccx.tools import Bolt
from pygccx import enums

@dataclass
class CsysMock:
    type:enums.EOrientationSystems = enums.EOrientationSystems.RECTANGULAR


class TestBolt(unittest.TestCase):

    def setUp(self) -> None:
        self.kwargs = dict(name='', csys=CsysMock(), d_n=10, l_c=10, d_w=15, k=8, p=2, material=(210000, 0.3))

    def test_happy_case(self):
        Bolt(**self.kwargs)
        self.kwargs['shaft_sections'] = []
        Bolt(**self.kwargs)
        self.kwargs['shaft_sections'] = [[10,20]]
        Bolt(**self.kwargs)
        self.kwargs['shaft_sections'] = [[10,20],[9,10]]
        Bolt(**self.kwargs)

    def test_valid_csys(self):
        self.kwargs['csys'] = CsysMock(enums.EOrientationSystems.CYLINDRICAL)
        self.assertRaises(ValueError, Bolt, **self.kwargs)

    def test_valid_d_n(self):
        self.kwargs['d_n'] = 0
        self.assertRaises(ValueError, Bolt, **self.kwargs)
        self.kwargs['d_n'] = -1
        self.assertRaises(ValueError, Bolt, **self.kwargs)

    def test_valid_l_c(self):
        self.kwargs['l_c'] = 0
        self.assertRaises(ValueError, Bolt, **self.kwargs)
        self.kwargs['l_c'] = -1
        self.assertRaises(ValueError, Bolt, **self.kwargs)

    def test_valid_d_w(self):
        self.kwargs['d_w'] = self.kwargs['d_n']
        self.assertRaises(ValueError, Bolt, **self.kwargs)
        self.kwargs['d_w'] = self.kwargs['d_n'] -1
        self.assertRaises(ValueError, Bolt, **self.kwargs)

    def test_valid_k(self):
        self.kwargs['k'] = 0
        self.assertRaises(ValueError, Bolt, **self.kwargs)
        self.kwargs['k'] = -1
        self.assertRaises(ValueError, Bolt, **self.kwargs)

    def test_valid_p(self):
        self.kwargs['p'] = 0
        self.assertRaises(ValueError, Bolt, **self.kwargs)
        self.kwargs['p'] = -1
        self.assertRaises(ValueError, Bolt, **self.kwargs)

    def test_valid_material(self):
        self.kwargs['material'] = (0, 0.3)
        self.assertRaises(ValueError, Bolt, **self.kwargs)
        self.kwargs['material'] = (-1, 0.3)
        self.assertRaises(ValueError, Bolt, **self.kwargs)
        self.kwargs['material'] = (210000, 0)
        self.assertRaises(ValueError, Bolt, **self.kwargs)
        self.kwargs['material'] = (210000, -1)
        self.assertRaises(ValueError, Bolt, **self.kwargs)
        self.kwargs['material'] = (210000, 0.5)
        self.assertRaises(ValueError, Bolt, **self.kwargs)
        self.kwargs['material'] = (210000, 0.51)
        self.assertRaises(ValueError, Bolt, **self.kwargs)

    def test_valid_shaft_sections(self):
        self.kwargs['shaft_sections'] = [[10, 10, 10]]
        self.assertRaises(ValueError, Bolt, **self.kwargs)
        self.kwargs['shaft_sections'] = [[10]]
        self.assertRaises(ValueError, Bolt, **self.kwargs)

        self.kwargs['shaft_sections'] = [[0, 10]]
        self.assertRaises(ValueError, Bolt, **self.kwargs)
        self.kwargs['shaft_sections'] = [[-1, 10]]
        self.assertRaises(ValueError, Bolt, **self.kwargs)
        self.kwargs['shaft_sections'] = [[10, 0]]
        self.assertRaises(ValueError, Bolt, **self.kwargs)
        self.kwargs['shaft_sections'] = [[10, -1]]
        self.assertRaises(ValueError, Bolt, **self.kwargs)
        self.kwargs['shaft_sections'] = [[self.kwargs['d_w'], 10]]
        self.assertRaises(ValueError, Bolt, **self.kwargs)
        self.kwargs['shaft_sections'] = [[self.kwargs['d_w']+1, 10]]
        self.assertRaises(ValueError, Bolt, **self.kwargs)



if __name__ == '__main__':
    unittest.main()