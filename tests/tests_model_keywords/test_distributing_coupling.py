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

from pygccx.model_keywords import DistribuitingCoupling
from pygccx.enums import ESetTypes
from pygccx.protocols import IKeyword

@dataclass()
class SetMock():
    name:str
    type:ESetTypes
    dim:int
    ids:set[int]

class TestDistribuitingCoupling(TestCase):

    def setUp(self) -> None:
        self.nset = SetMock('S1', ESetTypes.NODE, 1, set([1,2,3,4]))
        self.elset = SetMock('S1', ESetTypes.ELEMENT, 1, set([1]))
        self.elset2 = SetMock('S2', ESetTypes.ELEMENT, 1, set([1,2]))

    def test_is_IKeyword(self):
        dc = DistribuitingCoupling(self.elset, 1)
        self.assertTrue(isinstance(dc, IKeyword))

    def test_default(self):
        dc = DistribuitingCoupling(self.elset, 1)
        known = '*DISTRIBUTING COUPLING,ELSET=S1\n'
        known += '1,1.0000000e+00\n'
        self.assertEqual(str(dc), known)

    def test_weight(self):
        dc = DistribuitingCoupling(self.elset, 1, 3)
        known = '*DISTRIBUTING COUPLING,ELSET=S1\n'
        known += '1,3.0000000e+00\n'
        self.assertEqual(str(dc), known)

    def test_nset(self):
        dc = DistribuitingCoupling(self.elset, self.nset)
        known = '*DISTRIBUTING COUPLING,ELSET=S1\n'
        known += 'S1,1.0000000e+00\n'
        self.assertEqual(str(dc), known)

    def test_add_condition(self):
        dc = DistribuitingCoupling(self.elset, self.nset)
        dc.add_condition(10,3)
        known = '*DISTRIBUTING COUPLING,ELSET=S1\n'
        known += 'S1,1.0000000e+00\n'
        known += '10,3.0000000e+00\n'
        self.assertEqual(str(dc), known)

    def test_elset_wrong_type(self):
        self.assertRaises(ValueError, DistribuitingCoupling, elset=self.nset, nid_or_set=1)

    def test_nset_wrong_type(self):
        self.assertRaises(ValueError, DistribuitingCoupling, elset=self.elset, nid_or_set=self.elset)

    def test_nid_too_low(self):
        self.assertRaises(ValueError, DistribuitingCoupling, elset=self.elset, nid_or_set=0)
        self.assertRaises(ValueError, DistribuitingCoupling, elset=self.elset, nid_or_set=-1)

    def test_to_many_eids_in_elset(self):
        self.assertRaises(ValueError, DistribuitingCoupling, elset=self.elset2, nid_or_set=1)

