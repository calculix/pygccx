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
from dataclasses import dataclass

import numpy as np

from pygccx.model_keywords import PretensionSection
from pygccx.enums import ESurfTypes
from pygccx.protocols import IKeyword

@dataclass()
class SurfaceMock:
    name:str
    type: ESurfTypes
    def write_ccx(self, buffer:list[str]): pass

class TestPretensionSection(TestCase):

    def test_is_IKeyword(self):

        s = SurfaceMock('', ESurfTypes.EL_FACE)
        ps = PretensionSection(1, s)
        self.assertTrue(isinstance(ps, IKeyword))

    def test_from_surface(self):

        s = SurfaceMock('SURF1', ESurfTypes.EL_FACE)
        # w/o normal
        ps = PretensionSection(234, s)
        known = '*PRE-TENSION SECTION,NODE=234,SURFACE=SURF1\n'
        self.assertEqual(str(ps), known)
        # w normal
        normal = np.array([0.7,0.5,0.3])
        normal /= np.linalg.norm(normal)
        ps = PretensionSection(234, s, normal=normal)
        known = '*PRE-TENSION SECTION,NODE=234,SURFACE=SURF1\n'
        known += '7.6834982e-01,5.4882130e-01,3.2929278e-01\n'
        self.assertEqual(str(ps), known)

    def test_from_beam(self):

        # w/o normal
        ps = PretensionSection(234, element=1)
        known = '*PRE-TENSION SECTION,NODE=234,ELEMENT=1\n'
        self.assertEqual(str(ps), known)
        # w normal
        normal = np.array([0.7,0.5,0.3])
        normal /= np.linalg.norm(normal)
        ps = PretensionSection(234, element=1, normal=normal)
        known = '*PRE-TENSION SECTION,NODE=234,ELEMENT=1\n'
        known += '7.6834982e-01,5.4882130e-01,3.2929278e-01\n'
        self.assertEqual(str(ps), known)

    def test_no_surface_or_element(self):

        self.assertRaises(ValueError, PretensionSection, 1)

    def test_surface_and_element(self):

        s = SurfaceMock('SURF1', ESurfTypes.EL_FACE)
        self.assertRaises(ValueError, PretensionSection, 1, surface=s, element=2)

    def test_normal_len_not_3(self):
        self.assertRaises(ValueError, PretensionSection, 1, normal=[1,0], element=2)
        self.assertRaises(ValueError, PretensionSection, 1, normal=[1,0,0,0], element=2)

    def test_normal_mag_not_1(self):
        self.assertRaises(ValueError, PretensionSection, 1, normal=[2,0,0], element=2)

    def test_surface_not_el_face(self):
        s = SurfaceMock('SURF1', ESurfTypes.NODE)
        self.assertRaises(ValueError, PretensionSection, 1, surface=s)

    def test_node_neg(self):
        s = SurfaceMock('SURF1', ESurfTypes.EL_FACE)
        self.assertRaises(ValueError, PretensionSection, 0, surface=s)
        self.assertRaises(ValueError, PretensionSection, -1, surface=s)



