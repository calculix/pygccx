from unittest import TestCase
from dataclasses import dataclass
from model_features import Clearance
from enums import ESurfTypes
from protocols import IModelFeature

@dataclass
class SurfaceMock:
    name:str
    type: ESurfTypes
    def write_ccx(self, buffer:list[str]): pass

class TestClearance(TestCase):

    def setUp(self) -> None:
        self.s1 = SurfaceMock('S1', ESurfTypes.EL_FACE)
        self.s2 = SurfaceMock('S2', ESurfTypes.EL_FACE)

    def test_is_IModelFeature(self):
        c = Clearance(self.s1, self.s2, 0.1)
        self.assertTrue(isinstance(c, IModelFeature))

    def test_default(self):
        c = Clearance(self.s1, self.s2, 0.1)
        known = '*CLEARANCE,MASTER=S1,SLAVE=S2,VALUE=0.1\n'
        self.assertEqual(str(c), known)