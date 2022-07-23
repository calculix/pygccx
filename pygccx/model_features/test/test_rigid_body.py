from unittest import TestCase
from dataclasses import dataclass
from model_features import RigidBody
from enums import ESetTypes
from protocols import IModelFeature

@dataclass()
class SetMock():
    name:str
    type:ESetTypes
    dim:int
    ids:set[int]


class TestRigidBody(TestCase):

    def setUp(self) -> None:
        self.nset = SetMock('TestSet', ESetTypes.NODE, 2, set((1, 2)))
        self.eset = SetMock('TestSet', ESetTypes.ELEMENT, 2, set((1, 2)))

    def test_is_IModelFeature(self):
        rb = RigidBody(self.nset, 1, 2)
        self.assertTrue(isinstance(rb, IModelFeature))

    def test_node_set_and_ref_node_and_rot_node(self):
      
        rb = RigidBody(self.nset, 1, 2)

        known = '*RIGID BODY,NSET=TestSet,REF NODE=1,ROT NODE=2\n'
        self.assertEqual(str(rb), known)

    def test_element_set_and_ref_node_and_rot_node(self):

        rb = RigidBody(self.eset, 1, 2)

        known = '*RIGID BODY,ELSET=TestSet,REF NODE=1,ROT NODE=2\n'
        self.assertEqual(str(rb), known)

    def test_wo_rot_node(self):

        rb = RigidBody(self.nset,1)

        known = '*RIGID BODY,NSET=TestSet,REF NODE=1\n'
        self.assertEqual(str(rb), known)

    def test_ref_node_lower_0(self):
        self.assertRaises(ValueError, RigidBody, self.nset, -1, 2)

    def test_rot_node_lower_0(self):
        self.assertRaises(ValueError, RigidBody, self.nset, 1, -2)





