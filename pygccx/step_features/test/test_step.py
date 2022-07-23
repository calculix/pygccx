from unittest import TestCase
from step_features import Step
from enums import EStepAmplitudes
from protocols import IStep

class TestStep(TestCase):

    def test_is_IStepFeature(self):
        s = Step()
        self.assertTrue(isinstance(s, IStep))

    def test_default(self):
        s = Step()
        known = '*STEP,INC=100,AMPLITUDE=RAMP\n'
        self.assertEqual(str(s), known)

    def test_perturbation(self):
        s = Step(perturbation=True)
        known = '*STEP,PERTURBATION,INC=100,AMPLITUDE=RAMP\n'
        self.assertEqual(str(s), known)

    def test_nlgeom(self):
        s = Step(nlgeom=True)
        known = '*STEP,NLGEOM,INC=100,AMPLITUDE=RAMP\n'
        self.assertEqual(str(s), known)
        s = Step(nlgeom=False)
        known = '*STEP,NLGEOM=NO,INC=100,AMPLITUDE=RAMP\n'
        self.assertEqual(str(s), known)

    def test_inc(self):
        s = Step(inc=50)
        known = '*STEP,INC=50,AMPLITUDE=RAMP\n'
        self.assertEqual(str(s), known)

    def test_amplitude(self):
        s = Step(amplitude=EStepAmplitudes.STEP)
        known = '*STEP,INC=100,AMPLITUDE=STEP\n'
        self.assertEqual(str(s), known)

    def test_inc_to_low(self):
        self.assertRaises(ValueError, Step, inc=0)
        self.assertRaises(ValueError, Step, inc=-1)