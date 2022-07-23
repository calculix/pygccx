from unittest import TestCase
from dataclasses import dataclass
from model_features import SolidSection
from enums import ESetTypes
from protocols import IModelFeature

@dataclass()
class SetMock():
    name:str
    type:ESetTypes
    dim:int
    ids:set[int]

@dataclass
class FeatureMock():
    name:str
    desc:str = ''

class TestSolidSection(TestCase):

    def setUp(self) -> None:
        self.s = SetMock('SET1', ESetTypes.ELEMENT, 2, set((1,2,3,4)))
        self.mat = FeatureMock('MAT1')
        self.ori = FeatureMock('OR1')

    def test_is_IModelFeature(self):
        sos = SolidSection(self.s, self.mat)
        self.assertTrue(isinstance(sos, IModelFeature))
    
    def test_wo_orientation(self):
        sos = SolidSection(self.s, self.mat)
        known = '*SOLID SECTION,MATERIAL=MAT1,ELSET=SET1\n'
        self.assertEqual(str(sos), known)

    def test_w_orientation(self):
        sos = SolidSection(self.s, self.mat, self.ori)
        known = '*SOLID SECTION,MATERIAL=MAT1,ELSET=SET1,ORIENTATION=OR1\n'
        self.assertEqual(str(sos), known)

    def test_false_set_type(self):
        s = SetMock('SET1', ESetTypes.NODE, 2, set((1,2,3,4)))
        mat = FeatureMock('MAT1')
        self.assertRaises(ValueError, SolidSection, s, mat)