from unittest import TestCase
from dataclasses import dataclass
from model_features import Boundary
from enums import ESetTypes
from protocols import IModelFeature

@dataclass()
class SetMock():
    name:str
    type:ESetTypes
    dim:int
    ids:set[int]

class TestBoundary(TestCase):

    def test_is_IModelFeature(self):
        b = Boundary(1, 1, 3)
        self.assertTrue(isinstance(b, IModelFeature))

    def test_first_dof_and_last_dof(self):

        b = Boundary(1, 1, 3)
        b.add_condition(2,1,2)

        known = '*BOUNDARY\n1,1,3\n2,1,2\n'
        self.assertEqual(str(b), known)

    def test_wo_last_dof(self):

        b = Boundary(1, 2)
        b.add_condition(2,1)

        known = '*BOUNDARY\n1,2\n2,1\n'
        self.assertEqual(str(b), known)

    def test_with_set(self):
        s = SetMock('TestSet', ESetTypes.NODE, 2, set((1,2)))
        b = Boundary(s, 1, 3)

        known = '*BOUNDARY\nTestSet,1,3\n'
        self.assertEqual(str(b), known)

    def test_nid_lower_one(self):
        self.assertRaises(ValueError, Boundary, 0, 1)
        self.assertRaises(ValueError, Boundary, -1, 1)

    def test_first_dof_lower_one(self):
        self.assertRaises(ValueError, Boundary, 1, 0)
        self.assertRaises(ValueError, Boundary, 1, -1)

    def test_last_dof_not_greater_first_dof(self):
        self.assertRaises(ValueError, Boundary, 1, 1, 0)
        self.assertRaises(ValueError, Boundary, 1, 1, 1)






