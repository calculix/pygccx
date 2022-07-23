from unittest import TestCase
from model_features import Amplitude
from protocols import IModelFeature

class TestAmplitude(TestCase):

    def test_is_IModelFeature(self):
        a = Amplitude('TestAmp', times = [0.,.1,.2,.3], amps=[0,1,-1,3])
        self.assertTrue(isinstance(a, IModelFeature))

    def test_only_mandatory_params(self):
        a = Amplitude('TestAmp', times = [0.,.1,.2,.3], amps=[0,1,-1,3])
        known = '*AMPLITUDE,NAME=TestAmp\n'
        known += '  0.0000000e+00,  0.0000000e+00\n'
        known += '  1.0000000e-01,  1.0000000e+00\n'
        known += '  2.0000000e-01, -1.0000000e+00\n'
        known += '  3.0000000e-01,  3.0000000e+00\n'
        self.assertEqual(str(a), known)

    def test_total_time(self):
        a = Amplitude('TestAmp', times = [0.,.1,.2,.3], amps=[0,1,-1,3], use_total_time=True)
        known = '*AMPLITUDE,NAME=TestAmp,TIME=TOTAL TIME\n'
        known += '  0.0000000e+00,  0.0000000e+00\n'
        known += '  1.0000000e-01,  1.0000000e+00\n'
        known += '  2.0000000e-01, -1.0000000e+00\n'
        known += '  3.0000000e-01,  3.0000000e+00\n'
        self.assertEqual(str(a), known)

    def test_shift_x(self):
        a = Amplitude('TestAmp', times = [0.,.1,.2,.3], amps=[0,1,-1,3], shift_x=0.5)
        known = '*AMPLITUDE,NAME=TestAmp,SHIFTX=0.5\n'
        known += '  0.0000000e+00,  0.0000000e+00\n'
        known += '  1.0000000e-01,  1.0000000e+00\n'
        known += '  2.0000000e-01, -1.0000000e+00\n'
        known += '  3.0000000e-01,  3.0000000e+00\n'
        self.assertEqual(str(a), known)

    def test_shift_y(self):
        a = Amplitude('TestAmp', times = [0.,.1,.2,.3], amps=[0,1,-1,3], shift_y=0.5)
        known = '*AMPLITUDE,NAME=TestAmp,SHIFTY=0.5\n'
        known += '  0.0000000e+00,  0.0000000e+00\n'
        known += '  1.0000000e-01,  1.0000000e+00\n'
        known += '  2.0000000e-01, -1.0000000e+00\n'
        known += '  3.0000000e-01,  3.0000000e+00\n'
        self.assertEqual(str(a), known)

    def test_total_time_shift_x_shift_y(self):
        a = Amplitude('TestAmp', times = [0.,.1,.2,.3], amps=[0,1,-1,3], use_total_time=True, shift_x=0.25, shift_y=0.5)
        known = '*AMPLITUDE,NAME=TestAmp,TIME=TOTAL TIME,SHIFTX=0.25,SHIFTY=0.5\n'
        known += '  0.0000000e+00,  0.0000000e+00\n'
        known += '  1.0000000e-01,  1.0000000e+00\n'
        known += '  2.0000000e-01, -1.0000000e+00\n'
        known += '  3.0000000e-01,  3.0000000e+00\n'
        self.assertEqual(str(a), known)

    def test_times_and_amps_defferent_length(self):
        self.assertRaises(ValueError, Amplitude, 'TestAmp', [0.,.1,.2], [0,1,-1,3])