from unittest import TestCase
from dataclasses import dataclass
from model_features import Coupling
from enums import ESurfTypes, ECouplingTypes
from protocols import IModelFeature

@dataclass
class SurfaceMock:
    name:str
    type: ESurfTypes
    def write_ccx(self, buffer:list[str]): pass

@dataclass
class OrientationMock:
    name:str
    desc:str = ''

class TestCoupling(TestCase):

    def setUp(self) -> None:
        self.surf = SurfaceMock('S1', ESurfTypes.EL_FACE)
        self.ori = OrientationMock('O1')

    def test_is_IModelFeature(self):
        c = Coupling(ECouplingTypes.DISTRIBUTING,
                        ref_node=1, surface=self.surf,
                        name='C1', first_dof=1)
        self.assertTrue(isinstance(c, IModelFeature))

    def test_default(self):
        c = Coupling(ECouplingTypes.DISTRIBUTING,
                        ref_node=1, surface=self.surf,
                        name='C1', first_dof=1)

        known = '*COUPLING,CONSTRAINT NAME=C1,REF NODE=1,SURFACE=S1\n'
        known += '*DISTRIBUTING\n'
        known += '1\n'

        self.assertEqual(str(c), known)

    def test_default_kinematic(self):
        c = Coupling(ECouplingTypes.KINEMATIC,
                        ref_node=1, surface=self.surf,
                        name='C1', first_dof=1)

        known = '*COUPLING,CONSTRAINT NAME=C1,REF NODE=1,SURFACE=S1\n'
        known += '*KINEMATIC\n'
        known += '1\n'

        self.assertEqual(str(c), known)

    def test_last_dof(self):
        c = Coupling(ECouplingTypes.DISTRIBUTING,
                        ref_node=1, surface=self.surf,
                        name='C1', first_dof=1, last_dof=4)

        known = '*COUPLING,CONSTRAINT NAME=C1,REF NODE=1,SURFACE=S1\n'
        known += '*DISTRIBUTING\n'
        known += '1,4\n'

        self.assertEqual(str(c), known)

    def test_orientation(self):
        c = Coupling(ECouplingTypes.DISTRIBUTING,
                        ref_node=1, surface=self.surf,
                        name='C1', first_dof=1,
                        orientation=self.ori)

        known = '*COUPLING,CONSTRAINT NAME=C1,REF NODE=1,SURFACE=S1,ORIENTATION=O1\n'
        known += '*DISTRIBUTING\n'
        known += '1\n'

        self.assertEqual(str(c), known)